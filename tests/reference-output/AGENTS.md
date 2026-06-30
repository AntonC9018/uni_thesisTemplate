These PDFs are committed manual baselines from the previous template output.

Automated tests do not compare against these PDFs.

After any template behavior or layout change, render `bare_main_ro.tex` and
`bare_main_ru.tex` manually from `thesis/`:

```bash
cd thesis
./render.sh --force --input=bare_main_ro.tex
./render.sh --force --input=bare_main_ru.tex
```

Manually compare the newly generated PDFs against
`tests/reference-output/previous/*.pdf`.

For code-block spacing visual checks, render the dedicated spacing PDFs:

```bash
python3 tests/reference-output/render_code_spacing.py
```

Manually compare the generated `tests/reference-output/current/code-spacing/*.pdf`
files against `tests/reference-output/previous/code-spacing/*.pdf`.

Replace the previous PDFs only when the output change is intentional and reviewed.
