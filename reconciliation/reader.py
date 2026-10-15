from io import BytesIO
from pathlib import Path
from typing import Union, Optional, Any
import pandas as pd


def load_excel(
    file_source: Union[str, Path, bytes, BytesIO],
    sheet_name: Optional[Union[str, int]] = 0,
) -> pd.DataFrame:
    """
    Carga un archivo Excel y devuelve un DataFrame limpio.
    """
    if isinstance(file_source, bytes):
        file_source = BytesIO(file_source)

    df = pd.read_excel(file_source, sheet_name=sheet_name, engine="openpyxl")
    # Normalizar nombres de columnas (strip de espacios y convertir a string)
    df.columns = [str(col).strip() for col in df.columns]
    return df


def inspect_excel(
    file_source: Union[str, Path, bytes, BytesIO]
) -> dict[str, Any]:
    """
    Inspecciona un archivo Excel y devuelve metadatos como hojas, columnas y vista previa.
    """
    if isinstance(file_source, bytes):
        file_source = BytesIO(file_source)

    excel_file = pd.ExcelFile(file_source, engine="openpyxl")
    sheet_names = excel_file.sheet_names

    first_sheet = sheet_names[0] if sheet_names else 0
    df = pd.read_excel(excel_file, sheet_name=first_sheet)
    df.columns = [str(col).strip() for col in df.columns]

    preview_rows = df.head(5).fillna("").to_dict(orient="records")

    return {
        "sheet_names": sheet_names,
        "selected_sheet": first_sheet,
        "columns": list(df.columns),
        "total_rows": len(df),
        "preview": preview_rows,
    }
