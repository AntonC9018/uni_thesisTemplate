from tests.lib import pdf
from tests.lib.assertions import assert_build_succeeded


def test_chapter_names_are_capitalized(build):
    assert_build_succeeded(build)
    text = pdf.pdf_text(build.pdf_path)
    assert "MIXED CASE CHAPTER NAME" in text
    assert "Mixed Case Chapter Name" not in text
