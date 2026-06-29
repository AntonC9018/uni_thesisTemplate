from pathlib import Path

import fitz

from tests.lib import pdf
from tests.lib.assertions import (
    assert_build_succeeded,
    assert_log_not_contains,
    assert_pdf_contains,
)
from tests.lib.latex import build_latex_case


def _word_rects(page: fitz.Page, word_prefix: str) -> list[fitz.Rect]:
    return [
        fitz.Rect(word[:4])
        for word in page.get_text("words")
        if word[4].startswith(word_prefix)
    ]


def _first_word_rect(doc: fitz.Document, word_prefix: str) -> tuple[int, fitz.Rect]:
    for page_index, page in enumerate(doc):
        rects = _word_rects(page, word_prefix)
        if rects:
            return page_index, min(rects, key=lambda rect: rect.y0)
    raise AssertionError(f"Missing word starting with {word_prefix!r}")


def _last_word_rect(doc: fitz.Document, word_prefix: str) -> tuple[int, fitz.Rect]:
    for page_index in reversed(range(len(doc))):
        rects = _word_rects(doc[page_index], word_prefix)
        if rects:
            return page_index, max(rects, key=lambda rect: rect.y1)
    raise AssertionError(f"Missing word starting with {word_prefix!r}")


def _vertical_gap_between_words(
    doc: fitz.Document,
    upper_word_prefix: str,
    lower_word_prefix: str,
) -> float:
    upper_page, upper_rect = _last_word_rect(doc, upper_word_prefix)
    lower_page, lower_rect = _first_word_rect(doc, lower_word_prefix)
    assert upper_page == lower_page
    return lower_rect.y0 - upper_rect.y1


def _assert_separated_by_gap_or_page_break(
    doc: fitz.Document,
    upper_word_prefix: str,
    lower_word_prefix: str,
    min_gap: float,
) -> None:
    upper_page, upper_rect = _last_word_rect(doc, upper_word_prefix)
    lower_page, lower_rect = _first_word_rect(doc, lower_word_prefix)
    assert lower_page >= upper_page
    if lower_page == upper_page:
        assert lower_rect.y0 - upper_rect.y1 >= min_gap


def test_oversized_code_blocks_break_before_footer(tmp_path: Path):
    case_dir = tmp_path / "case"
    case_dir.mkdir()
    build_dir = tmp_path / "build"
    build_dir.mkdir()

    (case_dir / "long-source.txt").write_text(
        "\n".join(f"file-code-line-{line:03d}" for line in range(1, 141)) + "\n",
        encoding="utf-8",
    )
    direct_code = "\n".join(f"direct-code-line-{line:03d}" for line in range(1, 141))
    (case_dir / "main.tex").write_text(
        f"""\\documentclass[a4paper,12pt]{{report}}
\\usepackage[romanian,custom]{{config}}

\\begin{{document}}
\\chapter{{Long Code}}
Long file code reference: \\ref{{code:long-file}}.
Long direct code reference: \\ref{{code:long-direct}}.

LongFileBefore.

\\insertCodeFile[code:long-file][linenos=false]{{text}}{{long-source.txt}}{{LongFileListing}}

LongFileAfter.

LongDirectBefore.

\\begin{{code}}[code:long-direct][linenos=false]{{text}}{{LongDirectListing}}
{direct_code}
\\end{{code}}
LongDirectAfter.
\\end{{document}}
""",
        encoding="utf-8",
    )

    result = build_latex_case(case_dir, build_dir)

    assert_build_succeeded(result)
    assert_pdf_contains(result, "Long file code reference: 1.1.")
    assert_pdf_contains(result, "Long direct code reference: 1.2.")
    assert_pdf_contains(result, "file-code-line-001")
    assert_pdf_contains(result, "file-code-line-140")
    assert_pdf_contains(result, "direct-code-line-001")
    assert_pdf_contains(result, "direct-code-line-140")
    assert_pdf_contains(result, "LongDirectAfter.")
    assert_log_not_contains(result, "Float too large")

    code_line_pages_by_prefix = {"file-code-line-": set(), "direct-code-line-": set()}
    text_bottom_tolerance = 5
    min_listing_separation = 10
    with fitz.open(result.pdf_path) as doc:
        for page_index, page in enumerate(doc):
            text_bottom = page.rect.height - 20 * 72 / 25.4 + text_bottom_tolerance
            for word in page.get_text("words"):
                matching_prefix = next(
                    (
                        prefix
                        for prefix in code_line_pages_by_prefix
                        if word[4].startswith(prefix)
                    ),
                    None,
                )
                if matching_prefix is None:
                    continue
                code_line_pages_by_prefix[matching_prefix].add(page_index)
                assert fitz.Rect(word[:4]).y1 <= text_bottom

        long_file_before_gap = _vertical_gap_between_words(
            doc, "LongFileBefore", "LongFileListing"
        )
        assert long_file_before_gap >= min_listing_separation

        _assert_separated_by_gap_or_page_break(
            doc, "file-code-line-140", "LongFileAfter", min_listing_separation
        )

        _assert_separated_by_gap_or_page_break(
            doc, "direct-code-line-140", "LongDirectAfter", min_listing_separation
        )

    assert pdf.page_count(result.pdf_path) > 1
    assert all(len(pages) > 1 for pages in code_line_pages_by_prefix.values())
