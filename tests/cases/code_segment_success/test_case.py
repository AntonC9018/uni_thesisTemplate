from tests.lib.assertions import assert_build_succeeded, assert_pdf_contains, assert_pdf_not_contains, normalized_code_lines
from tests.lib.snapshots import assert_snapshot


def test_code_segment_success_inserts_only_segment_body(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "Codul 1.1.")
    assert_pdf_contains(build, "pub fn test_func")
    assert_pdf_contains(build, "return 12")
    assert_pdf_not_contains(build, "Segment example begin")
    assert_pdf_not_contains(build, "Segment example end")
    assert_snapshot(normalized_code_lines(build), build.case_dir / "snapshots" / "code_text.txt")
