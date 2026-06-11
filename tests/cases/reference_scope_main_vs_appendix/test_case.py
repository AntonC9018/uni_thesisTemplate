from tests.lib.assertions import assert_build_succeeded, assert_log_contains, assert_pdf_contains


def test_appendix_references_do_not_satisfy_main_float_validation(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "main_only_from_appendix")
    assert_log_contains(build, "Package config Warning: Float label 'main_only_from_appendix' is not referenced")
