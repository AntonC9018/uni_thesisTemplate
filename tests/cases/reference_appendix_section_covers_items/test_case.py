from tests.lib.assertions import assert_build_succeeded, assert_log_not_contains, assert_pdf_not_contains


def test_appendix_section_reference_covers_numbered_items(build):
    assert_build_succeeded(build)
    for label in ("appendix:covered", "covered_appendix_image", "covered_appendix_table"):
        assert_pdf_not_contains(build, label)
        assert_log_not_contains(build, f"'{label}' is not referenced")
