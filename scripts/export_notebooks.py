from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "notebooks"

jobs = [
    ("Part_I_exploration.ipynb", "Part_I_exploration"),
    ("Part_II_explanatory.ipynb", "Part_II_explanatory"),
]

def run_cmd(cmd):
    print("Running:", " ".join(map(str, cmd)))
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)

# remove old exports from repo root
for stem in ("Part_I_exploration", "Part_II_explanatory"):
    for ext in (".html", ".pdf"):
        path = ROOT / f"{stem}{ext}"
        if path.exists():
            path.unlink()

pdf_failures = []

for nb_name, out_name in jobs:
    nb_path = NOTEBOOKS / nb_name

    # Execute notebook
    result = run_cmd([
        "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=1200",
        str(nb_path),
    ])
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(f"Notebook execution failed for {nb_name}")

    # Export HTML to repo root
    result = run_cmd([
        "jupyter", "nbconvert",
        "--to", "html",
        "--output", out_name,
        "--output-dir", str(ROOT),
        str(nb_path),
    ])
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(f"HTML export failed for {nb_name}")

    # Export PDF to repo root, but do not stop everything if it fails
    result = run_cmd([
        "jupyter", "nbconvert",
        "--to", "pdf",
        "--output", out_name,
        "--output-dir", str(ROOT),
        str(nb_path),
    ])
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        pdf_failures.append(nb_name)

print("Created files in repo root:")
for name in [
    "Part_I_exploration.html",
    "Part_I_exploration.pdf",
    "Part_II_explanatory.html",
    "Part_II_explanatory.pdf",
]:
    path = ROOT / name
    print(f"{name}: {'OK' if path.exists() else 'MISSING'}")

if pdf_failures:
    raise RuntimeError(f"PDF export failed for: {', '.join(pdf_failures)}")