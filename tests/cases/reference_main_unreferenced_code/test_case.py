from tests.lib.assertions import assert_build_succeeded, assert_log_contains, assert_pdf_contains


def test_unreferenced_main_code_produces_visible_and_log_warning(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "ATENȚIE: această imagine, acest tabel sau acest bloc de cod nu este referit în text")
    assert_pdf_contains(build, "unreferenced_main_code")
    assert_log_contains(build, "Package config Warning: Float label 'unreferenced_main_code' is not referenced")
