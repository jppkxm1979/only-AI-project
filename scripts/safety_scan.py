#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "automation" / "autonomy.json"


def run(command):
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "command failed")
    return completed.stdout


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


def changed_files():
    output = run(["git", "diff", "--name-only"])
    files = [line.strip() for line in output.splitlines() if line.strip()]
    return files


def ensure_allowed_suffixes(files, config):
    blocked_suffixes = tuple(config["blocked_filename_suffixes"])
    for relative in files:
        path = Path(relative)
        lower_name = path.name.lower()
        if lower_name.endswith(blocked_suffixes):
            raise RuntimeError(f"blocked executable-like file detected: {relative}")


def ensure_blocked_content_absent(files, config):
    patterns = [pattern.lower() for pattern in config["blocked_content_patterns"]]
    for relative in files:
        path = REPO_ROOT / relative
        if not path.exists() or not path.is_file():
            continue
        content = path.read_text(encoding="utf-8").lower()
        for pattern in patterns:
            if pattern in content:
                raise RuntimeError(f"blocked content pattern '{pattern}' detected in {relative}")


def ensure_files_small(files):
    for relative in files:
        path = REPO_ROOT / relative
        if not path.exists() or not path.is_file():
            continue
        if path.stat().st_size > 50_000:
            raise RuntimeError(f"file too large for high-trust zone: {relative}")


def ensure_control_plane_unchanged(files):
    blocked_prefixes = (
        ".github/",
        "automation/",
        "scripts/",
        ".autonomy/",
        ".git/",
    )
    for relative in files:
        normalized = relative.replace("\\", "/")
        if normalized.startswith(blocked_prefixes):
            raise RuntimeError(f"control-plane change detected: {relative}")


def main():
    config = load_config()
    files = changed_files()
    if not files:
        return 0
    ensure_control_plane_unchanged(files)
    ensure_allowed_suffixes(files, config)
    ensure_blocked_content_absent(files, config)
    ensure_files_small(files)
    return 0


if __name__ == "__main__":
    sys.exit(main())
