import random
from datetime import datetime, timedelta
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "ejemplos_excel"
OUTPUT_DIR.mkdir(exist_ok=True)

# Fijar semilla para reproducibilidad exacta
random.seed(42)

EMPRESAS = [
    "Amazon Web Services Spain", "Microsoft Ireland Operations", "Google Cloud EMEA",
    "Telefónica de España S.A.U.", "Iberdrola Clientes S.A.", "Endesa Energía",
    "Indra Sistemas S.A.", "Accenture S.L.", "Deloitte Advisory",
    "PwC Tax & Legal", "KPMG Auditores", "Mercadona S.A.",
    "Logista Freight", "DHL Express Spain", "Seur GeoPost",
    "Vodafone España", "Orange Espagne", "Salesforce Spain",
    "Oracle Ibérica", "SAP España", "HubSpot Ireland",
    "CrowdStrike Security", "Cisco Systems Spain", "Apple Distribution",
    "Cabify Logística", "Repsol Petróleo", "Cepsa Comercial"
]

DEPARTAMENTOS = ["Tecnología e IT", "Marketing y Ventas", "Operaciones", "Finanzas y Legal", "Recursos Humanos"]
CATEGORIAS = ["Infraestructura Cloud", "Consultoría y Auditoría", "Software & Licencias", "Hardware y Redes", "Transporte y Logística", "Publicidad y Medios"]
SEDES = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga"]
METODOS = ["Transferencia Bancaria", "Tarjeta Corporativa", "Remesa SEPA B2B", "Pasarela Stripe"]
ESTADOS = ["Pagado", "Pagado", "Pagado", "Pendiente", "En Revisión"]

HEADER_FONT = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
REGULAR_FONT = Font(name="Segoe UI", size=10)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
ALIGN_LEFT = Alignment(horizontal="left", vertical="center")
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")

THIN_BORDER = Border(
    left=Side(style="thin", color="E2E8F0"),
    right=Side(style="thin", color="E2E8F0"),
    top=Side(style="thin", color="E2E8F0"),
    bottom=Side(style="thin", color="E2E8F0"),
)


def generate_enterprise_excels():
    start_date = datetime(2026, 1, 15)
    total_records = 120

    data_a = []
    data_b = []

    for i in range(1, total_records + 1):
        trx_id = f"TRX-2026-{i:04d}"
        fecha = (start_date + timedelta(days=int(i * 1.8))).strftime("%Y-%m-%d")
        empresa = random.choice(EMPRESAS)
        depto = random.choice(DEPARTAMENTOS)
        categoria = random.choice(CATEGORIAS)
        sede = random.choice(SEDES)
        metodo = random.choice(METODOS)
        
        base = round(random.uniform(250.0, 18500.0), 2)
        total = round(base * 1.21, 2)
        estado = random.choice(ESTADOS)

        # Regla de simulación de discrepancias:
        # Caso 1 (80 registros): Coincidencia exacta 100%
        # Caso 2 (12 registros): Diferencia de importe en Banco (comisión o retención)
        # Caso 3 (8 registros): Diferencia de Estado (ERP Pagado vs Banco Pendiente/Rechazado)
        # Caso 4 (6 registros): Diferencia de Departamento o Categoría (descuadre analítico)
        # Caso 5 (7 registros): Falta en Banco (Factura emitida en A pero sin cobro en B)
        # Caso 6 (7 registros): Falta en ERP (Movimiento bancario no registrado en A)

        if i <= 80:
            # Match 100%
            row_a = [trx_id, fecha, empresa, depto, categoria, sede, metodo, total, estado]
            row_b = [trx_id, fecha, empresa, depto, categoria, sede, metodo, total, estado]
            data_a.append(row_a)
            data_b.append(row_b)

        elif i <= 92:
            # Descuadre en Importe_Total (ej. comisiones o retenciones)
            comision = round(random.uniform(15.0, 120.0), 2)
            total_banco = round(total - comision, 2)
            row_a = [trx_id, fecha, empresa, depto, categoria, sede, metodo, total, "Pagado"]
            row_b = [trx_id, fecha, empresa, depto, categoria, sede, metodo, total_banco, "Pagado"]
            data_a.append(row_a)
            data_b.append(row_b)

        elif i <= 100:
            # Descuadre en Estado
            row_a = [trx_id, fecha, empresa, depto, categoria, sede, metodo, total, "Pagado"]
            row_b = [trx_id, fecha, empresa, depto, categoria, sede, metodo, total, "En Revisión"]
            data_a.append(row_a)
            data_b.append(row_b)

        elif i <= 106:
            # Descuadre en Departamento / Categoría
            depto_b = random.choice([d for d in DEPARTAMENTOS if d != depto])
            row_a = [trx_id, fecha, empresa, depto, categoria, sede, metodo, total, estado]
            row_b = [trx_id, fecha, empresa, depto_b, categoria, sede, metodo, total, estado]
            data_a.append(row_a)
            data_b.append(row_b)

        elif i <= 113:
            # Presente en ERP (A), faltante en Banco (B)
            row_a = [trx_id, fecha, empresa, depto, categoria, sede, metodo, total, "Pendiente"]
            data_a.append(row_a)

        else:
            # Presente en Banco (B), faltante en ERP (A)
            row_b = [trx_id, fecha, empresa, depto, categoria, sede, metodo, total, "Pagado"]
            data_b.append(row_b)

    headers = [
        "ID_Transaccion", "Fecha_Operacion", "Cliente_Proveedor",
        "Departamento", "Categoria_Gasto", "Sede_Fiscal",
        "Metodo_Pago", "Importe_Total", "Estado"
    ]

    # Guardar Tabla A (Facturación y Contabilidad ERP)
    save_styled_excel(
        OUTPUT_DIR / "Dataset_Empresarial_ERP_Tabla_A.xlsx",
        "ERP_Contabilidad",
        "3B82F6", # Blue 500
        headers,
        data_a
    )

    # Guardar Tabla B (Extracto Bancario y Pasarelas)
    save_styled_excel(
        OUTPUT_DIR / "Dataset_Empresarial_Banco_Tabla_B.xlsx",
        "Extracto_Bancario",
        "10B981", # Emerald 500
        headers,
        data_b
    )

    print(f"Creado: Dataset_Empresarial_ERP_Tabla_A.xlsx ({len(data_a)} filas)")
    print(f"Creado: Dataset_Empresarial_Banco_Tabla_B.xlsx ({len(data_b)} filas)")


def save_styled_excel(filepath, sheet_name, header_hex, headers, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name
    ws.views.sheetView[0].showGridLines = True

    header_fill = PatternFill(start_color=header_hex, end_color=header_hex, fill_type="solid")

    # Encabezados
    ws.row_dimensions[1].height = 28
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.font = HEADER_FONT
        cell.fill = header_fill
        cell.alignment = ALIGN_CENTER
        cell.border = THIN_BORDER

    # Filas
    for row_idx, row in enumerate(rows, 2):
        ws.row_dimensions[row_idx].height = 20
        for col_idx, val in enumerate(row, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER

            if isinstance(val, (int, float)):
                cell.number_format = "#,##0.00 €"
                cell.alignment = ALIGN_RIGHT
            elif isinstance(val, str) and (val.startswith("TRX-") or val.startswith("2026-")):
                cell.alignment = ALIGN_CENTER
            else:
                cell.alignment = ALIGN_LEFT

    # Auto ancho de columnas
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 14)

    wb.save(filepath)


if __name__ == "__main__":
    generate_enterprise_excels()
