from tests.lib import pdf
from tests.lib.assertions import assert_build_succeeded, assert_pdf_contains


def _span_containing(spans, text):
    for span in spans:
        if text in span["text"]:
            return span
    raise AssertionError(f"No PDF text span contains {text!r}")


def test_long_ai_usage_explanation_wraps_above_signature_block(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "DECLARAȚIE PRIVIND CONTRIBUȚIA PERSONALĂ")
    assert_pdf_contains(build, "Long AI start marker")
    assert_pdf_contains(build, "Long AI middle marker")
    assert_pdf_contains(build, "Long AI end marker")
    assert_pdf_contains(build, "Data:")
    assert_pdf_contains(build, "Semnătura autorului / autoarei")

    spans = pdf.text_spans(build.pdf_path)
    end_marker = _span_containing(spans, "Long AI end marker")
    signature_date = _span_containing(spans, "Data:")

    assert end_marker["page"] == signature_date["page"]
    assert end_marker["bbox"].y1 < signature_date["bbox"].y0
