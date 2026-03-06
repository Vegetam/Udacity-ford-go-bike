from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "notebooks"

jobs = [
    ("Part_I_exploration.ipynb", "Part_I_exploration"),
    ("Part_II_explanatory.ipynb", "Part_II_explanatory"),
]

# remove old exports from repo root so reruns overwrite cleanly
for stem in ("Part_I_exploration", "Part_II_explanatory"):
    for ext in (".html", ".pdf"):
        path = ROOT / f"{stem}{ext}"
        if path.exists():
            path.unlink()

for nb_name, out_name in jobs:
    nb_path = NOTEBOOKS / nb_name

    # execute notebook in place
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

    # export HTML to repo root
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

    # export PDF to repo root
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

print("Created:")
for name in [
    "Part_I_exploration.html",
    "Part_I_exploration.pdf",
    "Part_II_explanatory.html",
    "Part_II_explanatory.pdf",
]:
    print((ROOT / name).resolve())