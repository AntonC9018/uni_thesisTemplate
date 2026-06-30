from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import shutil
import sys
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tests.lib.latex import build_latex_case  # noqa: E402


@dataclass(frozen=True)
class CodeSpacingCase:
    name: str
    title: str
    line_count: int
    in_appendix: bool = False
    expected_returncode: int = 0


CASES = (
    CodeSpacingCase("short_not_large", "Short not-large code block", 6),
    CodeSpacingCase("medium_not_large", "Medium not-large code block", 28),
    CodeSpacingCase(
        "large_main_text",
        "Large main-text code block",
        140,
        expected_returncode=4,
    ),
    CodeSpacingCase(
        "large_appendix",
        "Large appendix code block",
        140,
        in_appendix=True,
    ),
)


def _code_lines(case: CodeSpacingCase) -> str:
    return "\n".join(
        f"{case.name}-line-{line:03d}: spacing sample content"
        for line in range(1, case.line_count + 1)
    )


def _main_text_case(case: CodeSpacingCase) -> str:
    label = f"code:{case.name}"
    return rf"""\documentclass[a4paper,12pt]{{report}}
\usepackage[romanian,custom]{{config}}

\begin{{document}}
\chapter{{Spacing Visual Sample}}
Reference to the listing, so ordinary reference validation is satisfied: \ref{{{label}}}.

BEFORE {case.title.upper()} MARKER.

\begin{{code}}[{label}][linenos=false]{{text}}{{{case.title}}}
{_code_lines(case)}
\end{{code}}
AFTER {case.title.upper()} MARKER.
\end{{document}}
"""


def _appendix_case(case: CodeSpacingCase) -> str:
    return rf"""\documentclass[a4paper,12pt]{{report}}
\usepackage[romanian,custom]{{config}}

\begin{{document}}
\chapter{{Spacing Visual Sample}}
This PDF shows a large code listing placed in an appendix, where no red appendix suggestion should be emitted.

\appendixChapter
\section{{{case.title}}}
BEFORE {case.title.upper()} MARKER.

\begin{{codeWithoutLabel}}[linenos=false]{{text}}
{_code_lines(case)}
\end{{codeWithoutLabel}}
AFTER {case.title.upper()} MARKER.
\end{{document}}
"""


def _case_tex(case: CodeSpacingCase) -> str:
    if case.in_appendix:
        return _appendix_case(case)
    return _main_text_case(case)


def render_cases(output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    with tempfile.TemporaryDirectory(prefix="uni_thesisTemplate_code_spacing_") as tmp:
        tmp_root = Path(tmp)
        for case in CASES:
            case_dir = tmp_root / "cases" / case.name
            build_dir = tmp_root / "builds" / case.name
            case_dir.mkdir(parents=True)
            build_dir.mkdir(parents=True)
            (case_dir / "main.tex").write_text(_case_tex(case), encoding="utf-8")

            result = build_latex_case(case_dir, build_dir)
            if result.returncode != case.expected_returncode:
                raise RuntimeError(
                    f"{case.name} exited with {result.returncode}, "
                    f"expected {case.expected_returncode}"
                )
            if not result.pdf_path.exists():
                raise RuntimeError(f"{case.name} did not produce {result.pdf_path}")

            destination = output_dir / f"{case.name}.pdf"
            shutil.copy2(result.pdf_path, destination)
            print(f"{case.name}: {destination}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render manual visual baselines for code-block spacing."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "tests" / "reference-output" / "current" / "code-spacing",
        help="Directory where generated PDFs will be written.",
    )
    args = parser.parse_args()

    render_cases(args.output)


if __name__ == "__main__":
    main()
