#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".md", ".py", ".rs", ".toml", ".txt"}
BLOCKED_PREFIXES = (".github/", "automation/", "scripts/", ".autonomy/", ".git/")


def run(command):
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}")
    return completed


def verify_readable_text_files():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(REPO_ROOT).as_posix()
        if relative.startswith(BLOCKED_PREFIXES):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        path.read_text(encoding="utf-8")


def verify_json_files():
    for path in REPO_ROOT.rglob("*.json"):
        relative = path.relative_to(REPO_ROOT).as_posix()
        if relative.startswith(BLOCKED_PREFIXES):
            continue
        json.loads(path.read_text(encoding="utf-8"))


def verify_python_files():
    py_files = []
    for path in REPO_ROOT.rglob("*.py"):
        relative = path.relative_to(REPO_ROOT).as_posix()
        if relative.startswith(BLOCKED_PREFIXES):
            continue
        py_files.append(str(path))
    if py_files:
        run([sys.executable, "-m", "py_compile", *py_files])


def verify_safety_scan():
    run([sys.executable, str(REPO_ROOT / "scripts" / "safety_scan.py")])


def verify_node_files():
    package_json = REPO_ROOT / "package.json"
    package_lock = REPO_ROOT / "package-lock.json"
    if not package_json.exists() or not package_lock.exists():
        return

    package_data = json.loads(package_json.read_text(encoding="utf-8"))
    run(["npm", "ci"])
    scripts = package_data.get("scripts", {})
    if "lint" in scripts:
        run(["npm", "run", "lint"])
    if "test" in scripts:
        run(["npm", "test", "--", "--runInBand"])


def verify_rust_files():
    cargo_toml = REPO_ROOT / "Cargo.toml"
    if not cargo_toml.exists():
        return

    run(["cargo", "fmt", "--all", "--check"])
    run(["cargo", "check"])
    run(["cargo", "test", "--all-targets"])


def main():
    verify_safety_scan()
    verify_readable_text_files()
    verify_json_files()
    verify_python_files()
    verify_node_files()
    verify_rust_files()
    return 0


if __name__ == "__main__":
    sys.exit(main())
