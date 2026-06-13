import pytest

from tests.lib.assertions import (
    assert_build_failed,
    assert_build_succeeded,
    assert_log_contains,
    assert_log_not_contains,
    assert_pdf_contains,
    assert_pdf_not_contains,
)
from tests.lib.latex import build_latex_case


@pytest.mark.parametrize(
    ("input_file", "package_error", "message_fragment"),
    [
        ("main.tex", "Package insertImage Error", "only allowed in appendices"),
        ("main_starred_table.tex", "Package insertTable Error", "only allowed in appendices"),
        ("main_starred_code.tex", "Package insertCodeFile Error", "only allowed in appendices"),
        ("main_starred_insert_code.tex", "Package insertCode Error", "only allowed in appendices"),
        ("main_starred_image_with_label.tex", "Package insertImage Error", "bad_starred_label"),
        ("main_unstarred_table_missing_label.tex", "Package insertTable Error", "No label given"),
        ("main_unstarred_code_missing_label.tex", "Package code Error", "No label given"),
        ("main_unstarred_insert_code_missing_label.tex", "Package insertCode Error", "No label given"),
    ],
)
def test_float_macro_api_errors(case_dir, tmp_path, input_file, package_error, message_fragment):
    result = build_latex_case(case_dir, tmp_path, input_file)

    assert_build_failed(result)
    assert_log_contains(result, package_error)
    assert_log_contains(result, message_fragment)


def test_starred_floats_are_allowed_in_appendices(case_dir, tmp_path):
    result = build_latex_case(case_dir, tmp_path, "main_starred_appendix_allowed.tex")

    assert_build_succeeded(result)
    assert_pdf_contains(result, "Appendix starred image caption")
    assert_pdf_contains(result, "Appendix starred table caption")
    assert_pdf_contains(result, "file helper code")
    assert_pdf_contains(result, "segment helper code")
    assert_pdf_contains(result, "direct starred appendix code")
    assert_pdf_not_contains(result, "Codul")
    assert_log_not_contains(result, "only allowed in appendices")


def test_unstarred_image_uses_filename_fallback_label(case_dir, tmp_path):
    result = build_latex_case(case_dir, tmp_path, "main_image_fallback_label.tex")

    assert_build_succeeded(result)
    assert_pdf_contains(result, "Fallback image reference marker: 1.1.")
