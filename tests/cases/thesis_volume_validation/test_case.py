from pathlib import Path

from tests.lib import pdf
from tests.lib.assertions import (
    assert_build_failed,
    assert_build_succeeded,
    assert_log_contains,
    assert_log_not_contains,
    assert_pdf_contains,
    assert_pdf_not_contains,
)
from tests.lib.latex import build_latex_case


VISIBLE_WARNING = "ATENȚIE:"


def assert_red_warning(result):
    assert_pdf_contains(result, VISIBLE_WARNING)
    spans = pdf.text_spans(result.pdf_path)
    assert any(VISIBLE_WARNING in span["text"] and span.get("color") == 0xFF0000 for span in spans)


def build_input(case_dir, tmp_path, input_file):
    build_dir = tmp_path / Path(input_file).stem
    build_dir.mkdir()
    return build_latex_case(case_dir, build_dir, input_file)


def test_under_minimum_introduction_and_main_chapters_warn(build):
    assert_build_failed(build)
    assert_red_warning(build)
    assert_log_contains(build, "introducerea has")
    assert_log_contains(build, "capitolele principale has")


def test_over_maximum_conclusion_warns(case_dir, tmp_path):
    result = build_input(case_dir, tmp_path, "main_conclusion_over.tex")

    assert_build_failed(result)
    assert_red_warning(result)
    assert_log_contains(result, "concluziile finale has")


def test_master_annotation_under_minimum_warns(case_dir, tmp_path):
    result = build_input(case_dir, tmp_path, "main_master_annotation_under.tex")

    assert_build_failed(result)
    assert_red_warning(result)
    assert_log_contains(result, "adnotările has")


def test_bibliography_under_minimum_warns(case_dir, tmp_path):
    result = build_input(case_dir, tmp_path, "main_bibliography_under.tex")

    assert_build_failed(result)
    assert_red_warning(result)
    assert_log_contains(result, "bibliografia has")


def test_bibliography_has_no_maximum(case_dir, tmp_path):
    result = build_input(case_dir, tmp_path, "main_bibliography_over_old_max.tex")

    assert_build_succeeded(result)
    assert_pdf_not_contains(result, VISIBLE_WARNING)
    assert_log_not_contains(result, "CONFIG_VISIBLE_WARNING")


def test_plain_unnumbered_chapter_is_not_volume_validated(case_dir, tmp_path):
    result = build_input(case_dir, tmp_path, "main_unnumbered_unvalidated.tex")

    assert_build_succeeded(result)
    assert_pdf_not_contains(result, VISIBLE_WARNING)
    assert_log_not_contains(result, "CONFIG_VISIBLE_WARNING")


def test_custom_and_practice_document_types_do_not_get_volume_validation(case_dir, tmp_path):
    for input_file in ("main_custom_unvalidated.tex", "main_practice_unvalidated.tex"):
        result = build_input(case_dir, tmp_path, input_file)

        assert_build_succeeded(result)
        assert_pdf_not_contains(result, VISIBLE_WARNING)
        assert_log_not_contains(result, "CONFIG_VISIBLE_WARNING")
