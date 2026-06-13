from tests.lib.assertions import assert_build_succeeded, assert_footer_page_number, assert_pdf_contains
from tests.lib.latex import build_latex_case


def test_romanian_title_page_counts_but_is_not_numbered(build):
    assert_build_succeeded(build)
    assert_footer_page_number(build.pdf_path, 0, "1", expected=False)
    assert_footer_page_number(build.pdf_path, 1, "2", expected=True)
    assert_pdf_contains(build, "Teză de licență")
    assert_pdf_contains(build, "absolvent din grupa TST")
    assert_pdf_contains(build, "0613.5 INFORMATICĂ APLICATĂ")


def test_romanian_master_title_page_derives_metadata(case_dir, tmp_path):
    result = build_latex_case(case_dir, tmp_path, "main_master.tex")

    assert_build_succeeded(result)
    assert_pdf_contains(result, "Teză de master")
    assert_pdf_contains(result, "masterand din grupa TST")
    assert_pdf_contains(result, "INFORMATICĂ APLICATĂ")
