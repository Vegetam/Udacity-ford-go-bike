from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    (REPO_ROOT / "notebooks" / "Part_I_exploration.ipynb", "Part_I_exploration"),
    (REPO_ROOT / "notebooks" / "Part_II_explanatory.ipynb", "Part_II_explanatory"),
]
OUTPUTS = [
    REPO_ROOT / "Part_I_exploration.html",
    REPO_ROOT / "Part_II_explanatory.html",
    REPO_ROOT / "Part_I_exploration.pdf",
    REPO_ROOT / "Part_II_explanatory.pdf",
]


def run_command(command: list[str]) -> None:
    """Run a command from the repository root."""
    print("Running:", " ".join(command))
    subprocess.run(command, check=True, cwd=REPO_ROOT)


def execute_notebook(notebook_path: Path) -> None:
    """Execute a notebook in place so cell outputs are refreshed."""
    run_command(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--inplace",
            "--ExecutePreprocessor.timeout=1200",
            str(notebook_path),
        ]
    )


def export_html(notebook_path: Path, output_name: str) -> None:
    """Export HTML to the repository root with a stable filename."""
    run_command(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "html",
            "--output",
            output_name,
            "--output-dir",
            str(REPO_ROOT),
            str(notebook_path),
        ]
    )


def export_pdf(notebook_path: Path, output_name: str) -> None:
    """Export PDF to the repository root with a stable filename."""
    if shutil.which("xelatex") is None:
        raise RuntimeError("xelatex is not installed, so PDF export cannot run.")

    run_command(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "pdf",
            "--output",
            output_name,
            "--output-dir",
            str(REPO_ROOT),
            str(notebook_path),
        ]
    )


def remove_stale_outputs() -> None:
    """Delete existing exports so each run overwrites them cleanly."""
    for output_file in OUTPUTS:
        if output_file.exists():
            output_file.unlink()


def main() -> None:
    """Execute notebooks and regenerate HTML/PDF exports."""
    remove_stale_outputs()

    for notebook_path, output_name in NOTEBOOKS:
        if not notebook_path.exists():
            raise FileNotFoundError(f"Missing notebook: {notebook_path}")
        execute_notebook(notebook_path)
        export_html(notebook_path, output_name)
        export_pdf(notebook_path, output_name)

    print("Notebook execution and exports completed successfully.")


if __name__ == "__main__":
    main()
