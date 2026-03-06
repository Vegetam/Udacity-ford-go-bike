from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    REPO_ROOT / 'notebooks' / 'Part_I_exploration.ipynb',
    REPO_ROOT / 'notebooks' / 'Part_II_explanatory.ipynb',
]
OUTPUTS = [
    REPO_ROOT / 'Part_I_exploration.html',
    REPO_ROOT / 'Part_II_explanatory.html',
    REPO_ROOT / 'Part_I_exploration.pdf',
    REPO_ROOT / 'Part_II_explanatory.pdf',
]


def run_command(command: list[str]) -> None:
    """Run a command and fail loudly if it exits with a non-zero status."""
    print('Running:', ' '.join(command))
    subprocess.run(command, check=True, cwd=REPO_ROOT)


def execute_notebook(notebook_path: Path) -> None:
    """Execute a notebook in place so outputs and saved figures are refreshed."""
    run_command(
        [
            'jupyter', 'nbconvert',
            '--to', 'notebook',
            '--execute',
            str(notebook_path),
            '--inplace',
            '--ExecutePreprocessor.timeout=900',
        ]
    )


def export_html(notebook_path: Path) -> None:
    """Export a notebook to HTML in the repository root."""
    run_command(
        [
            'jupyter', 'nbconvert',
            '--to', 'html',
            str(notebook_path),
            '--output-dir', str(REPO_ROOT),
        ]
    )


def export_pdf(notebook_path: Path) -> None:
    """Export a notebook to PDF in the repository root when xelatex is available."""
    if shutil.which('xelatex') is None:
        raise RuntimeError('xelatex is not installed, so PDF export cannot run.')

    run_command(
        [
            'jupyter', 'nbconvert',
            '--to', 'pdf',
            str(notebook_path),
            '--output-dir', str(REPO_ROOT),
        ]
    )


def remove_stale_outputs() -> None:
    """Remove old exports before regenerating them."""
    for output_file in OUTPUTS:
        if output_file.exists():
            output_file.unlink()


def main() -> None:
    """Execute notebooks and regenerate HTML/PDF exports."""
    remove_stale_outputs()

    for notebook in NOTEBOOKS:
        if not notebook.exists():
            raise FileNotFoundError(f'Missing notebook: {notebook}')
        execute_notebook(notebook)
        export_html(notebook)
        export_pdf(notebook)

    print('Notebook execution and exports completed successfully.')


if __name__ == '__main__':
    main()
