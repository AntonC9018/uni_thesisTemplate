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


def build_input(case_dir, tmp_path, input_file):
    build_dir = tmp_path / Path(input_file).stem
    build_dir.mkdir()
    return build_latex_case(case_dir, build_dir, input_file)


def test_unreferenced_bibliography_entries_are_not_listed(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "Referenced Regression Source")
    assert_pdf_not_contains(build, "Unreferenced Regression Source")
    assert_log_not_contains(build, "Bibliography source(s)")
    assert "unreferenced_source" not in build.artifact_text(".bbl")


def test_nocite_for_cited_source_does_not_warn(case_dir, tmp_path):
    result = build_input(case_dir, tmp_path, "main_cite_and_nocite.tex")

    assert_build_succeeded(result)
    assert_pdf_contains(result, "Referenced Regression Source")
    assert_log_not_contains(result, "Bibliography source(s)")


def test_nocite_produces_visible_and_log_warning(case_dir, tmp_path):
    result = build_input(case_dir, tmp_path, "main_nocite.tex")

    assert_build_failed(result)
    assert_pdf_contains(result, "ATENȚIE: aceste surse nu sunt citate în text")
    assert_pdf_contains(result, "unreferenced_source")
    assert_pdf_contains(result, "Unreferenced Regression Source")
    assert_log_contains(
        result,
        "Package config Warning: Bibliography source(s) 'unreferenced_source' inserted with \\nocite but not cited",
    )
    spans = pdf.text_spans(result.pdf_path)
    assert any("ATENȚIE:" in span["text"] and span.get("color") == 0xFF0000 for span in spans)
