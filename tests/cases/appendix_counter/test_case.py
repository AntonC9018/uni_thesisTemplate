from tests.lib.assertions import assert_build_succeeded, assert_pdf_contains


def test_appendix_counter_counts_appendix_sections(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "Appendix counter marker: 2.")
