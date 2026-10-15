from pathlib import Path
import pandas as pd

SAMPLE_DIR = Path(__file__).resolve().parent

data_a = {
    "ID_Factura": ["FACT-001", "FACT-002", "FACT-003", "FACT-004", "FACT-005", "FACT-006"],
    "Cliente": ["Alfa Corp", "Beta S.L.", "Gamma Tech", "Delta Logistics", "Epsilon Labs", "Zeta Global"],
    "Monto": [1200.50, 450.00, 890.00, 3200.00, 150.00, 990.00],
    "Moneda": ["EUR", "EUR", "EUR", "EUR", "EUR", "EUR"],
    "Estado": ["Pagado", "Pagado", "Pendiente", "Pagado", "Pagado", "Pagado"],
}

data_b = {
    "ID_Factura": ["FACT-001", "FACT-002", "FACT-003", "FACT-004", "FACT-007", "FACT-008"],
    "Cliente": ["Alfa Corp", "Beta S.L.", "Gamma Tech", "Delta Logistics", "Theta Media", "Iota Digital"],
    "Monto": [1200.50, 450.00, 850.00, 3200.00, 600.00, 430.00],
    "Moneda": ["EUR", "EUR", "EUR", "EUR", "EUR", "EUR"],
    "Estado": ["Pagado", "Pagado", "Pendiente", "Pendiente", "Pagado", "Pagado"],
}

def generate_sample_excels():
    df_a = pd.DataFrame(data_a)
    df_b = pd.DataFrame(data_b)

    path_a = SAMPLE_DIR / "tabla_a.xlsx"
    path_b = SAMPLE_DIR / "tabla_b.xlsx"

    df_a.to_excel(path_a, index=False, sheet_name="Facturacion_Interna")
    df_b.to_excel(path_b, index=False, sheet_name="Extracto_Bancario")

    print(f"Creado: {path_a} ({len(df_a)} filas)")
    print(f"Creado: {path_b} ({len(df_b)} filas)")

if __name__ == "__main__":
    generate_sample_excels()
