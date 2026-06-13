from tests.lib.assertions import (
    assert_build_succeeded,
    assert_log_not_contains,
    assert_pdf_contains,
    assert_pdf_not_contains,
)


def test_insert_code_command_accepts_direct_braced_body_without_percent(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "Direct command reference: 1.1.")
    assert_pdf_contains(build, "Codul 1.1.")
    assert_pdf_contains(build, "#include")
    assert_pdf_contains(build, "std::cout")
    assert_pdf_contains(build, "percent")
    assert_pdf_contains(build, "Regular text")
    assert_pdf_contains(build, "With braces")
    assert_pdf_contains(build, "Hash #")
    assert_pdf_not_contains(build, "Plain command block: Codul")
    assert_log_not_contains(build, "Package config Warning")
