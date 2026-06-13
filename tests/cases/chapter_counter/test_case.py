from tests.lib.assertions import assert_build_succeeded, assert_pdf_contains


def test_chapter_counter_counts_numbered_chapters(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "Chapter counter marker: 3.")
