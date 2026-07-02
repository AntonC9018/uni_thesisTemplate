from __future__ import annotations

import importlib.util
from pathlib import Path


def load_find_segment_module():
    path = Path(__file__).resolve().parents[1] / "thesis" / "findSegment.py"
    spec = importlib.util.spec_from_file_location("findSegment", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_minted_language_resolves_supported_aliases_and_filenames():
    find_segment = load_find_segment_module()

    assert find_segment.minted_language_for_file("source.sql") == ("sql", "sql")
    assert find_segment.minted_language_for_file("source.hpp") == ("cpp", "hpp")
    assert find_segment.minted_language_for_file("Makefile") == ("make", "make")
    assert find_segment.minted_language_for_file("source.notminted") == (None, "notminted")


def test_minted_language_prefers_latex_safe_aliases():
    find_segment = load_find_segment_module()

    assert find_segment.minted_language_for_file("source.c#") == ("csharp", "c#")
