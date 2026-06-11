from tests.lib.assertions import assert_build_succeeded, assert_log_not_contains, assert_pdf_contains


def test_user_visible_counter_macros_in_annotation_sentence(build):
    assert_build_succeeded(build)

    assert_pdf_contains(build, "chapters=2")
    assert_pdf_contains(build, "bibliography=2")
    assert_pdf_contains(build, "appendices=2")
    assert_pdf_contains(build, "useful=2")
    assert_log_not_contains(build, "Package config Warning")
