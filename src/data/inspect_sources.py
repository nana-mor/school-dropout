from pathlib import Path
import pandas as pd
from dbfread import DBF

PROJECT_ROOT = Path.cwd().resolve()
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"


def inspect_excel(file_path):
    """Display the structure of every sheet in an Excel file."""
    print(f"\n{'=' * 60}")
    print(f"FILE: {file_path}")
    print("=" * 60)

    try:
        # nrows=5 evita cargar archivos gigantes en RAM si solo quieres ver el head()
        sheets = pd.read_excel(file_path, sheet_name=None, nrows=5)
    except Exception as e:
        print(f"[AVISO] No se pudo leer como Excel nativo ({type(e).__name__}: {e})")
        
        # Respaldo: muchos sistemas exportan tablas HTML con extensión .xls
        try:
            tables = pd.read_html(file_path)
            sheets = {f"Tabla_HTML_{i+1}": df.head(5) for i, df in enumerate(tables)}
            print("[INFO] Archivo leído exitosamente como tabla HTML disfrazada de Excel.")
        except Exception as e_html:
            print(f"[ERROR] Imposible abrir {file_path.name}: {e_html}")
            return

    for sheet_name, df in sheets.items():
        print(f"\nSHEET: {sheet_name}")
        print(f"Shape (muestra): {df.shape}")

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nData types:")
        print(df.dtypes)

        print("\nFirst records:")
        print(df.head())


def inspect_dbf(file_path):
    """Display the structure of a DBF file."""

    print(f"\n{'=' * 60}")
    print(f"FILE: {file_path.name}")
    print("=" * 60)

    table = DBF(str(file_path), load=False)

    print(f"Number of records: {len(table)}")
    print("\nColumns:")
    print(table.field_names)

    records = []

    for index, record in enumerate(table):
        records.append(record)

        if index == 4:
            break

    df = pd.DataFrame(records)

    print("\nFirst records:")
    print(df)


def inspect_directory(directory):
    """Inspect all supported files in a directory."""


    files = [p for p in directory.rglob("*") if p.is_file()]
    
    files.sort(key=lambda p: (len(p.parts), str(p).lower()))


    for file_path in files:
        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        if extension in [".xlsx", ".xls"]:
            inspect_excel(file_path)
            

        elif extension == ".dbf":
            inspect_dbf(file_path)

if __name__ == "__main__":
    inspect_directory(RAW_DATA_PATH)

