from tests.lib.assertions import (
    assert_build_succeeded,
    assert_log_not_contains,
    assert_pdf_contains,
    assert_pdf_not_contains,
)


def test_sql_code_segment_uses_minted_language_support(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "Codul 1.1.")
    assert_pdf_contains(build, "select 1 as value")
    assert_pdf_not_contains(build, "Segment example begin")
    assert_pdf_not_contains(build, "Segment example end")
    assert_log_not_contains(build, "Code segment language 'sql' is not supported")
