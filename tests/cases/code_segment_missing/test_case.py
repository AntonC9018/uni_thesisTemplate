from tests.lib.assertions import assert_build_failed, assert_log_contains, assert_pdf_contains, assert_pdf_not_contains


def test_missing_code_segment_warns_in_log_and_document(build):
    assert_build_failed(build)
    assert_pdf_contains(build, "ATENȚIE: segmentul de cod nu a fost găsit")
    assert_pdf_contains(build, "missing")
    assert_pdf_contains(build, "source.zig")
    assert_log_contains(build, "Package config Warning: Code segment 'missing' was not found in 'source.zig'")
    assert_pdf_not_contains(build, "Traceback (most recent call last)")
