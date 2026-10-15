import io
import pandas as pd
from reconciliation.reader import load_excel, inspect_excel


def test_load_and_inspect_excel():
    # Crear un excel en memoria
    df_sample = pd.DataFrame({
        " ID ": [101, 102, 103],
        "Nombre": ["Producto A", "Producto B", "Producto C"],
        "Precio": [50.0, 75.5, 100.0]
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_sample.to_excel(writer, index=False, sheet_name="Datos")
    excel_bytes = buffer.getvalue()

    # Probar load_excel
    loaded_df = load_excel(excel_bytes)
    assert "ID" in loaded_df.columns
    assert len(loaded_df) == 3

    # Probar inspect_excel
    meta = inspect_excel(excel_bytes)
    assert "Datos" in meta["sheet_names"]
    assert "ID" in meta["columns"]
    assert meta["total_rows"] == 3
    assert len(meta["preview"]) == 3
