from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import shutil
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_THESIS_DIR = REPO_ROOT / "thesis"
SOURCE_FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
TEXLIVE_BIN = Path("/usr/local/texlive/2025/bin/x86_64-linux")


@dataclass
class LatexBuildResult:
    case_name: str
    case_dir: Path
    build_dir: Path
    thesis_dir: Path
    pdf_path: Path
    log_path: Path
    returncode: int
    stdout: str
    stderr: str

    @property
    def log_text(self) -> str:
        if not self.log_path.exists():
            return ""
        return self.log_path.read_text(encoding="utf-8", errors="replace")

    def artifact_text(self, suffix: str) -> str:
        path = self.thesis_dir / f"{self.pdf_path.stem}{suffix}"
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8", errors="replace")


def _build_env(render_venv: Path | None = None) -> dict[str, str]:
    env = os.environ.copy()
    current_path = env.get("PATH", "")
    if TEXLIVE_BIN.is_dir():
        env["PATH"] = f"{current_path}{os.pathsep}{TEXLIVE_BIN}"
    if render_venv is not None:
        env["THESIS_RENDER_VENV"] = str(render_venv)
    return env


def _preflight(env: dict[str, str]) -> None:
    for command in ("latexmk", "xelatex", "biber"):
        if shutil.which(command, path=env.get("PATH")) is None:
            raise AssertionError(
                f"LaTeX preflight failed: missing command '{command}'. "
                "Install the LaTeX tooling required by thesis/render.sh."
            )


def _copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def _copy_case_files(case_dir: Path, thesis_dir: Path) -> None:
    for source in case_dir.iterdir():
        if source.name == "__pycache__":
            continue
        destination = thesis_dir / source.name
        if source.is_dir():
            _copy_tree(source, destination)
        else:
            shutil.copy2(source, destination)


def build_latex_case(case_dir: Path, tmp_path: Path, input_file: str = "main.tex") -> LatexBuildResult:
    env = _build_env(tmp_path.parent / ".render-venv")
    _preflight(env)
    input_stem = Path(input_file).stem

    thesis_dir = tmp_path / "thesis"
    thesis_dir.mkdir()

    for name in (
        "config.sty",
        "render.sh",
        "render-requirements.txt",
        "findSegment.py",
        "bibliography.bib",
    ):
        shutil.copy2(SOURCE_THESIS_DIR / name, thesis_dir / name)

    for name in ("parts", "images"):
        _copy_tree(SOURCE_THESIS_DIR / name, thesis_dir / name)

    if SOURCE_FIXTURES_DIR.exists():
        _copy_tree(SOURCE_FIXTURES_DIR, thesis_dir / "fixtures")

    _copy_case_files(case_dir, thesis_dir)

    process = subprocess.run(
        ["./render.sh", f"--input={input_file}"],
        cwd=thesis_dir,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )

    return LatexBuildResult(
        case_name=case_dir.name,
        case_dir=case_dir,
        build_dir=thesis_dir,
        thesis_dir=thesis_dir,
        pdf_path=thesis_dir / f"{input_stem}.pdf",
        log_path=thesis_dir / f"{input_stem}.log",
        returncode=process.returncode,
        stdout=process.stdout,
        stderr=process.stderr,
    )
