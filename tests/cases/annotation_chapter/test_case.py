from tests.lib.assertions import (
    assert_build_succeeded,
    assert_log_contains,
    assert_log_not_contains,
    assert_pdf_contains,
)
from tests.lib.latex import build_latex_case


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
