from pathlib import Path
import unicodedata
import pandas as pd
from dbfread import DBF

PROJECT_ROOT = Path.cwd().resolve()
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed"


def load_excel(file_name, sheet_name=0):
    """Load an Excel file."""

    file_path = RAW_DATA_PATH / file_name

    return pd.read_excel(file_path, sheet_name=sheet_name)


def load_dbf(file_name):
    """Load a DBF file."""

    file_path = RAW_DATA_PATH / "enigh_2022" / file_name

    table = DBF(
        str(file_path),
        load=True,
        char_decode_errors="replace"
    )

    return pd.DataFrame(iter(table))


def normalize_state_name(state):
    """Standardize state names."""

    if pd.isna(state):
        return None

    state = str(state).strip().upper()

    state = unicodedata.normalize(
        "NFKD", state
    ).encode("ASCII", "ignore").decode("ASCII")

    state = " ".join(state.split())

    return state


def save_processed_data(df, file_name):
    """Save a processed DataFrame as CSV."""

    PROCESSED_DATA_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = PROCESSED_DATA_PATH / file_name

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"File saved: {output_path}")
