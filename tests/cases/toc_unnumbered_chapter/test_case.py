from tests.lib import pdf
from tests.lib.assertions import assert_build_succeeded


def test_unnumbered_chapter_is_added_to_toc_without_chapter_number(build):
    assert_build_succeeded(build)
    toc = build.artifact_text(".toc")
    assert "Custom Unnumbered Chapter" in toc

    toc_page = pdf.page_texts(build.pdf_path)[0]
    assert "Custom Unnumbered Chapter" in toc_page
    toc_line = next(line for line in toc_page.splitlines() if "Custom Unnumbered Chapter" in line)
    assert not toc_line.strip().startswith("1.")
