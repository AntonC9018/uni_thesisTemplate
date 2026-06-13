from tests.lib.assertions import assert_build_failed, assert_log_contains, assert_pdf_contains


def test_uncovered_appendix_items_warn_with_exact_labels(build):
    assert_build_failed(build)
    assert_pdf_contains(build, "ATENȚIE: această anexă sau acest element din anexă nu este referit în text")
    for label in (
        "appendix:uncovered",
        "uncovered_appendix_image",
        "uncovered_appendix_table",
        "uncovered_appendix_code",
    ):
        assert_pdf_contains(build, label)
        assert_log_contains(build, f"Package config Warning: Appendix label '{label}' is not referenced")
