from tests.lib.assertions import assert_build_succeeded, assert_footer_page_number


def test_russian_title_pages_count_but_are_not_numbered(build):
    assert_build_succeeded(build)
    assert_footer_page_number(build.pdf_path, 0, "1", expected=False)
    assert_footer_page_number(build.pdf_path, 1, "2", expected=False)
    assert_footer_page_number(build.pdf_path, 2, "3", expected=True)
