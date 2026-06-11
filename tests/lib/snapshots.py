from __future__ import annotations

from pathlib import Path
import difflib
import os
import re


TEMP_PATH_RE = re.compile(r"/tmp/pytest-[^\s)>\]}]+")


def normalize_snapshot_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = TEMP_PATH_RE.sub("<BUILD_DIR>", text)
    return "\n".join(line.rstrip() for line in text.split("\n")).strip() + "\n"


def assert_snapshot(actual: str, snapshot_path: Path) -> None:
    normalized = normalize_snapshot_text(actual)
    if os.environ.get("UPDATE_SNAPSHOTS") == "1":
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text(normalized, encoding="utf-8")
        return

    expected = snapshot_path.read_text(encoding="utf-8") if snapshot_path.exists() else ""
    expected = normalize_snapshot_text(expected) if expected else ""
    if normalized != expected:
        diff = "".join(
            difflib.unified_diff(
                expected.splitlines(keepends=True),
                normalized.splitlines(keepends=True),
                fromfile=str(snapshot_path),
                tofile="actual",
            )
        )
        raise AssertionError(f"Snapshot mismatch:\n{diff}")
