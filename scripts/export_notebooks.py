from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "notebooks"

jobs = [
    ("Part_I_exploration.ipynb", "Part_I_exploration"),
    ("Part_II_explanatory.ipynb", "Part_II_explanatory"),
]

# remove old exports from repo root
for stem in ("Part_I_exploration", "Part_II_explanatory"):
    for ext in (".html", ".pdf"):
        path = ROOT / f"{stem}{ext}"
        if path.exists():
            path.unlink()

for nb_name, out_name in jobs:
    nb_path = NOTEBOOKS / nb_name

    # Execute notebook in place
    subprocess.run(
        [
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            "--ExecutePreprocessor.timeout=1200",
            str(nb_path),
        ],
        check=True,
        cwd=ROOT,
    )

    # Export HTML to repo root
    subprocess.run(
        [
            "jupyter", "nbconvert",
            "--to", "html",
            "--output", out_name,
            "--output-dir", str(ROOT),
            str(nb_path),
        ],
        check=True,
        cwd=ROOT,
    )

    # Export PDF to repo root
    subprocess.run(
        [
            "jupyter", "nbconvert",
            "--to", "pdf",
            "--output", out_name,
            "--output-dir", str(ROOT),
            str(nb_path),
        ],
        check=True,
        cwd=ROOT,
    )