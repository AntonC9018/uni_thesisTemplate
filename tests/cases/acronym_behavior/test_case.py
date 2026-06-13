from tests.lib import pdf
from tests.lib.assertions import assert_build_succeeded, assert_pdf_contains, assert_pdf_not_contains


def test_acronym_behavior_beyond_row_layout(build):
    assert_build_succeeded(build)
    text = pdf.pdf_text(build.pdf_path)

    assert_pdf_contains(build, "USED")
    assert_pdf_contains(build, "Used Long Form")
    assert_pdf_contains(build, "Alias Long Form (ALIAS)")
    assert_pdf_contains(build, "Alias short marker: ALIAS")
    assert_pdf_contains(build, "Application Programming Interfaces (APIs)")
    assert_pdf_contains(build, "Plural short marker: APIs")
    assert_pdf_contains(build, "Plural long marker: Application Programming Interfaces")
    assert text.count("Reset Long Form (RESET)") >= 2
    assert_pdf_not_contains(build, "Unused Long Form")
