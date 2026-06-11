import re

from tests.lib import pdf
from tests.lib.assertions import assert_build_succeeded, assert_log_not_contains, assert_pdf_contains


def test_user_visible_counter_macros_in_annotation_sentence(build):
    assert_build_succeeded(build)
    text = pdf.pdf_text(build.pdf_path)

    assert_pdf_contains(build, "chapters=2")
    assert_pdf_contains(build, "bibliography=2")
    assert_pdf_contains(build, "appendices=2")
    assert re.search(r"useful=[1-9][0-9]*", text)
    assert_log_not_contains(build, "Package config Warning")
