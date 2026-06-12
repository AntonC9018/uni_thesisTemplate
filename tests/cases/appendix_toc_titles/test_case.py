from tests.lib import pdf
from tests.lib.assertions import (
    assert_build_succeeded,
    assert_pdf_contains,
    assert_pdf_not_contains,
    assert_toc_row_links_to_text,
)


def _page_with_text(pages: list[str], text: str) -> int:
    for index, page in enumerate(pages):
        if text in page:
            return index
    raise AssertionError(f"Could not find {text!r} in PDF pages")


def test_appendix_toc_entries_use_full_titles_and_keep_ref_numbers(build):
    assert_build_succeeded(build)

    toc = build.artifact_text(".toc")
    assert r"\contentsline {section}{\numberline {Anexa{} 1}First Appendix Target}" in toc
    assert r"\contentsline {section}{\numberline {Anexa{} 2}Second Appendix Target}" in toc
    assert r"\contentsline {section}{\numberline {1}First Appendix Target}" not in toc
    assert r"\contentsline {section}{\numberline {2}Second Appendix Target}" not in toc

    assert_pdf_contains(build, "anexa 1")
    assert_pdf_contains(build, "anexa 2")
    assert_pdf_not_contains(build, "anexa Anexa")


def test_appendix_toc_entries_link_to_their_appendix_pages(build):
    assert_build_succeeded(build)

    assert_toc_row_links_to_text(build, "Anexa 1", "First appendix body marker")
    assert_toc_row_links_to_text(build, "Anexa 2", "Second appendix body marker")

    pages = pdf.page_texts(build.pdf_path)
    first_page = _page_with_text(pages, "First appendix body marker")
    second_page = _page_with_text(pages, "Second appendix body marker")
    assert "ANEXE" in pages[first_page]
    assert first_page != second_page
