from tests.lib.assertions import assert_build_succeeded, assert_log_contains, assert_pdf_contains


def test_multiple_reference_warnings_survive_one_build(build):
    assert_build_succeeded(build)
    expected = (
        ("Float", "unreferenced_main_image"),
        ("Float", "unreferenced_main_table"),
        ("Appendix", "appendix:uncovered"),
        ("Appendix", "uncovered_appendix_image"),
        ("Appendix", "uncovered_appendix_table"),
    )
    for warning_kind, label in expected:
        assert_pdf_contains(build, label)
        assert_log_contains(build, f"Package config Warning: {warning_kind} label '{label}' is not referenced")
