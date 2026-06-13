from tests.lib.assertions import assert_build_succeeded, assert_log_not_contains, assert_pdf_contains


def test_code_file_helper_accepts_minted_options_and_numbers_listing(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "Full file helper reference: 1.1.")
    assert_pdf_contains(build, "Options helper reference: 1.2.")
    assert_pdf_contains(build, "Codul 1.1.")
    assert_pdf_contains(build, "Codul 1.2.")
    assert_pdf_contains(build, "file helper first line")
    assert_pdf_contains(build, "file helper second line")
    assert_log_not_contains(build, "Package config Warning")
