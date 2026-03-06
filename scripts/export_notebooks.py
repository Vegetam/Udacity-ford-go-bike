"""
export_notebooks.py
Execute both Jupyter notebooks and export them to HTML and PDF.
Runs in GitHub Actions CI (Ubuntu with pandoc + texlive) and locally.
PDF generation is optional — the script will NOT crash if PDFs fail.
"""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "notebooks"

JOBS = [
    ("Part_I_exploration.ipynb", "Part_I_exploration"),
    ("Part_II_explanatory.ipynb", "Part_II_explanatory"),
]


def run(cmd, label=""):
    """Run a subprocess, stream output, return the CompletedProcess."""
    print(f"\n{'='*60}")
    print(f"  {label or ' '.join(cmd)}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    print(f"  -> exit code {result.returncode}")
    return result


def has_tool(name):
    """Return True if *name* is on the PATH."""
    return shutil.which(name) is not None


# ── Clean old exports ──────────────────────────────────────────────────────
for stem in ("Part_I_exploration", "Part_II_explanatory"):
    for ext in (".html", ".pdf"):
        p = ROOT / f"{stem}{ext}"
        if p.exists():
            p.unlink()
            print(f"Removed old {p.name}")

# ── 1) Execute notebooks in-place ─────────────────────────────────────────
for nb_name, _ in JOBS:
    nb_path = NOTEBOOKS / nb_name
    r = run([
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=1200",
        str(nb_path),
    ], label=f"Execute {nb_name}")
    if r.returncode != 0:
        raise RuntimeError(f"Notebook execution failed: {nb_name}")

# ── 2) Export HTML (must succeed) ──────────────────────────────────────────
for nb_name, out_name in JOBS:
    nb_path = NOTEBOOKS / nb_name
    r = run([
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "html",
        "--output", out_name,
        "--output-dir", str(ROOT),
        str(nb_path),
    ], label=f"HTML export {nb_name}")
    if r.returncode != 0:
        raise RuntimeError(f"HTML export failed: {nb_name}")

# ── 3) Export PDFs (best-effort) ───────────────────────────────────────────
#   Strategy: try LaTeX-based PDF first (needs pandoc + xelatex).
#   If that is unavailable, try webpdf (needs playwright + chromium).
#   If nothing works, warn but do NOT fail the build — HTML is sufficient.
pdf_ok = []
pdf_fail = []

# Decide which PDF backend to attempt
use_latex = has_tool("pandoc") and has_tool("xelatex")
use_webpdf = not use_latex  # fallback

if use_latex:
    print("\n>> PDF backend: LaTeX (pandoc + xelatex detected)")
elif use_webpdf:
    print("\n>> PDF backend: webpdf (pandoc/xelatex not found, trying headless browser)")
else:
    print("\n>> PDF backend: none available")

for nb_name, out_name in JOBS:
    nb_path = NOTEBOOKS / nb_name
    generated = False

    if use_latex:
        r = run([
            sys.executable, "-m", "jupyter", "nbconvert",
            "--to", "pdf",
            "--output", out_name,
            "--output-dir", str(ROOT),
            str(nb_path),
        ], label=f"PDF (LaTeX) {nb_name}")
        if r.returncode == 0:
            generated = True

    if not generated and use_webpdf:
        r = run([
            sys.executable, "-m", "jupyter", "nbconvert",
            "--to", "webpdf",
            "--allow-chromium-download",
            "--output", out_name,
            "--output-dir", str(ROOT),
            str(nb_path),
        ], label=f"PDF (webpdf) {nb_name}")
        if r.returncode == 0:
            generated = True

    if generated:
        pdf_ok.append(nb_name)
    else:
        pdf_fail.append(nb_name)

# ── Summary ────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  EXPORT SUMMARY")
print("="*60)
for name in [
    "Part_I_exploration.html",
    "Part_I_exploration.pdf",
    "Part_II_explanatory.html",
    "Part_II_explanatory.pdf",
]:
    p = ROOT / name
    status = f"OK ({p.stat().st_size / 1024:.0f} KB)" if p.exists() else "MISSING"
    print(f"  {name}: {status}")

if pdf_fail:
    print(f"\n⚠  PDF export failed for: {', '.join(pdf_fail)}")
    print("   HTML exports are available. PDFs require pandoc+xelatex or playwright.")
    print("   The GitHub Actions CI will generate PDFs automatically on push.")
else:
    print("\n✓  All exports generated successfully.")