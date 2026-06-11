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

Replace the previous PDFs only when the output change is intentional and reviewed.
