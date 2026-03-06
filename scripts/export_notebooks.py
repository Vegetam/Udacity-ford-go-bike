from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "notebooks"

jobs = [
    ("Part_I_exploration.ipynb", "Part_I_exploration"),
    ("Part_II_explanatory.ipynb", "Part_II_explanatory"),
]

def run(cmd):
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result

# Remove old exports from repo root
for stem in ("Part_I_exploration", "Part_II_explanatory"):
    for ext in (".html", ".pdf"):
        p = ROOT / f"{stem}{ext}"
        if p.exists():
            p.unlink()

# 1) Execute notebooks
for nb_name, _ in jobs:
    nb_path = NOTEBOOKS / nb_name
    r = run([
        "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=1200",
        str(nb_path),
    ])
    if r.returncode != 0:
        raise RuntimeError(f"Notebook execution failed: {nb_name}")

# 2) Export ALL HTML first
for nb_name, out_name in jobs:
    nb_path = NOTEBOOKS / nb_name
    r = run([
        "jupyter", "nbconvert",
        "--to", "html",
        "--output", out_name,
        "--output-dir", str(ROOT),
        str(nb_path),
    ])
    if r.returncode != 0:
        raise RuntimeError(f"HTML export failed: {nb_name}")

# 3) Export PDFs, but do both attempts before failing
pdf_failures = []
for nb_name, out_name in jobs:
    nb_path = NOTEBOOKS / nb_name
    r = run([
        "jupyter", "nbconvert",
        "--to", "pdf",
        "--output", out_name,
        "--output-dir", str(ROOT),
        str(nb_path),
    ])
    if r.returncode != 0:
        pdf_failures.append(nb_name)

print("Repo root contents:")
for name in [
    "Part_I_exploration.html",
    "Part_I_exploration.pdf",
    "Part_II_explanatory.html",
    "Part_II_explanatory.pdf",
]:
    p = ROOT / name
    print(f"{name}: {'OK' if p.exists() else 'MISSING'}")

if pdf_failures:
    raise RuntimeError("PDF export failed for: " + ", ".join(pdf_failures))