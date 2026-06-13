from tests.lib.assertions import (
    assert_build_failed,
    assert_build_succeeded,
    assert_log_contains,
    assert_log_not_contains,
    assert_pdf_contains,
)
from tests.lib.latex import build_latex_case
from pathlib import Path


def test_annotation_chapter_sets_contextual_quote_styles(build):
    assert_build_succeeded(build)

    assert_pdf_contains(build, "„ro quote”")
    assert_pdf_contains(build, "«ru quote»")
    assert_pdf_contains(build, "“en quote”")
    assert_pdf_contains(build, "„main quote”")
    assert_log_not_contains(build, "Package config Warning")


def test_annotation_chapter_warns_when_document_is_not_master(case_dir, tmp_path):
    result = build_latex_case(case_dir, tmp_path, "main_non_master.tex")

    assert_build_succeeded(result)
    assert_pdf_contains(result, "ATENȚIE: doar pentru teză de master")
    assert_log_contains(
        result,
        "Package config Warning: Annotation chapter 'ro' is intended only for master theses",
    )


def test_annotation_chapter_warns_for_practice_documents(case_dir, tmp_path):
    for input_file in (
        "main_practica_licenta_1.tex",
        "main_practica_licenta_2.tex",
        "main_practica_licenta_3.tex",
        "main_practica_master_2.tex",
    ):
        build_dir = tmp_path / Path(input_file).stem
        build_dir.mkdir()
        result = build_latex_case(case_dir, build_dir, input_file)

        assert_build_succeeded(result)
        assert_pdf_contains(result, "ATENȚIE: doar pentru teză de master")
        assert_log_contains(
            result,
            "Package config Warning: Annotation chapter 'ro' is intended only for master theses",
        )


def test_missing_document_type_fails(case_dir, tmp_path):
    result = build_latex_case(case_dir, tmp_path, "main_missing_document_type.tex")

    assert_build_failed(result)
    assert_log_contains(result, "Expected exactly one document type option")


def test_multiple_document_types_fail(case_dir, tmp_path):
    result = build_latex_case(case_dir, tmp_path, "main_multiple_document_types.tex")

    assert_build_failed(result)
    assert_log_contains(result, "Expected exactly one document type option")


def test_unsupported_master_specialty_fails(case_dir, tmp_path):
    result = build_latex_case(case_dir, tmp_path, "main_unsupported_master_specialty.tex")

    assert_build_failed(result)
    assert_log_contains(result, "Unsupported specialty")


def test_custom_document_type_allows_overrides(case_dir, tmp_path):
    result = build_latex_case(case_dir, tmp_path, "main_custom.tex")

    assert_build_succeeded(result)
    assert_pdf_contains(result, "Custom metadata: raport special true.")
