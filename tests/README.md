# Thesis Template Regression Tests

Run the manual regression suite from the repository root:

```bash
python3 -m pytest tests
```

The wrapper script is equivalent:

```bash
tests/run.sh
```

Install Python dependencies with:

```bash
python3 -m pip install -r tests/requirements.txt
```

Each case in `tests/cases/` is staged into a temporary `thesis/` directory together with
the template runtime files. Generated PDFs, logs, auxiliary files, and minted output stay
under pytest temporary directories.

Snapshots are text-only. To intentionally refresh them:

```bash
UPDATE_SNAPSHOTS=1 python3 -m pytest tests
```
