from tests.lib.assertions import (
    assert_build_succeeded,
    assert_log_not_contains,
    assert_pdf_contains,
    assert_pdf_not_contains,
)
from tests.lib import pdf


def test_insert_code_command_accepts_direct_braced_body_without_percent(build):
    assert_build_succeeded(build)
    assert_pdf_contains(build, "Direct command reference: 1.1.")
    assert_pdf_contains(build, "Codul 1.1.")
    assert_pdf_contains(build, "#include")
    assert_pdf_contains(build, "std::cout")
    assert_pdf_contains(build, "percent")
    assert_pdf_contains(build, "Regular text")
    assert_pdf_contains(build, "With braces")
    assert_pdf_contains(build, "Hash #")
    assert_pdf_not_contains(build, "Plain command block: Codul")
    assert_log_not_contains(build, "Package config Warning")

    text = pdf.pdf_text(build.pdf_path)
    assert "1\n#include <iostream>\n2\nint main()\n3\n{\n4\nstd::cout" in text
    assert "Regular text\nMultiline\nWith braces { kept }\nHash # and percent % are literal" in text
    assert "Regular text Multiline With braces" not in text
