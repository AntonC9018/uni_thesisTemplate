from __future__ import annotations

from pathlib import Path
import re

import fitz

from tests.lib import pdf
from tests.lib.latex import LatexBuildResult


def assert_build_succeeded(result: LatexBuildResult) -> None:
    if result.returncode != 0:
        raise AssertionError(
            f"LaTeX case '{result.case_name}' failed with exit code {result.returncode}\n"
            f"stdout tail:\n{result.stdout[-4000:]}\n"
            f"stderr tail:\n{result.stderr[-4000:]}\n"
            f"log tail:\n{result.log_text[-4000:]}"
        )
    assert result.pdf_path.exists(), f"{result.case_name} did not produce main.pdf"


def assert_pdf_contains(result: LatexBuildResult, expected: str) -> None:
    text = pdf.pdf_text(result.pdf_path)
    assert expected in text, f"PDF text does not contain {expected!r}\n{text}"


def assert_pdf_not_contains(result: LatexBuildResult, unexpected: str) -> None:
    text = pdf.pdf_text(result.pdf_path)
    assert unexpected not in text, f"PDF text unexpectedly contains {unexpected!r}"


def assert_log_contains(result: LatexBuildResult, expected: str) -> None:
    compact_log = re.sub(r"\n\s*", "", result.log_text)
    assert expected in result.log_text or expected in compact_log, f"Log does not contain {expected!r}"


def assert_log_not_contains(result: LatexBuildResult, unexpected: str) -> None:
    assert unexpected not in result.log_text, f"Log unexpectedly contains {unexpected!r}"


def assert_no_latex_error_markers(result: LatexBuildResult) -> None:
    text = pdf.pdf_text(result.pdf_path)
    markers = (
        "Package biblatex Error",
        "LaTeX Error",
        "Undefined control sequence",
        "Biber error",
        "Traceback (most recent call last)",
    )
    for marker in markers:
        assert marker not in result.log_text
        assert marker not in text


def bibliography_text(result: LatexBuildResult) -> str:
    text = pdf.pdf_text(result.pdf_path)
    for heading in ("Bibliografie", "Библиография"):
        if heading in text:
            return text[text.index(heading) :]
    return text


def assert_toc_row_links_to_text(result: LatexBuildResult, toc_text: str, target_text: str) -> None:
    destination_page = pdf.find_link_destination_for_text(result.pdf_path, toc_text)
    assert destination_page is not None, f"No internal TOC link found for row {toc_text!r}"

    pages = pdf.page_texts(result.pdf_path)
    assert target_text in pages[destination_page], (
        f"TOC row {toc_text!r} links to page {destination_page + 1}, "
        f"which does not contain {target_text!r}"
    )


def assert_footer_page_number(pdf_path: Path, page_index: int, number: str, expected: bool) -> None:
    with fitz.open(pdf_path) as doc:
        page = doc[page_index]
        bottom = fitz.Rect(0, page.rect.height * 0.86, page.rect.width, page.rect.height)
        center_min = page.rect.width * 0.35
        center_max = page.rect.width * 0.65
        matches = []
        for word in page.get_text("words"):
            rect = fitz.Rect(word[:4])
            if word[4] == number and bottom.intersects(rect) and center_min <= rect.x0 <= center_max:
                matches.append(word)

    if expected:
        assert matches, f"Expected footer page number {number!r} on PDF page {page_index + 1}"
    else:
        assert not matches, f"Unexpected footer page number {number!r} on PDF page {page_index + 1}"


def normalized_code_lines(result: LatexBuildResult) -> str:
    lines = []
    for line in pdf.pdf_text(result.pdf_path).splitlines():
        cleaned = re.sub(r"^\s*\d+\s+", "", line).strip()
        if "pub fn test_func" in cleaned or "return 12" in cleaned:
            lines.append(cleaned)
    return "\n".join(lines)
