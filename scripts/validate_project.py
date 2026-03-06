from pathlib import Path
import pandas as pd


def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> None:
    repo_root = resolve_repo_root()
    data_file = repo_root / "data" / "fordgobike_2019_02.csv"
    notebooks = [
        repo_root / "notebooks" / "Part_I_exploration.ipynb",
        repo_root / "notebooks" / "Part_II_explanatory.ipynb",
    ]

    assert data_file.exists(), f"Missing dataset: {data_file}"
    for notebook in notebooks:
        assert notebook.exists(), f"Missing notebook: {notebook}"

    sample = pd.read_csv(data_file, nrows=500)
    required_columns = {
        "duration_sec", "start_time", "end_time", "user_type",
        "member_birth_year", "member_gender"
    }
    missing = required_columns.difference(sample.columns)
    assert not missing, f"Missing required columns: {sorted(missing)}"

    print("Project smoke test passed.")


if __name__ == "__main__":
    main()
