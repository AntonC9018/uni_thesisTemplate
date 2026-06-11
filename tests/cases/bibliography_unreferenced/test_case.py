from tests.lib.assertions import assert_build_succeeded, assert_pdf_contains, assert_pdf_not_contains


def test_unreferenced_bibliography_entries_are_not_listed(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "Referenced Regression Source")
    assert_pdf_not_contains(build, "Unreferenced Regression Source")
    assert "unreferenced_source" not in build.artifact_text(".bbl")
