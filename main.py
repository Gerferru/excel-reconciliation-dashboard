import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from reconciliation.reader import load_excel, inspect_excel
from reconciliation.engine import reconcile_tables
from notifications.mailer import trigger_alert_if_discrepancies

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("excel_reconciler")

app = FastAPI(
    title="Excel Reconciliation & Auditor",
    description="API y Dashboard para reconciliación de tablas Excel y alertas por correo",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renderiza la vista principal del Dashboard interactivo."""
    return templates.TemplateResponse(request=request, name="dashboard.html")


@app.get("/api/health")
async def health():
    """Endpoint de comprobación de estado."""
    return {"status": "ok", "app": "Excel Reconciliation & Auditor"}


@app.get("/api/view-email", response_class=HTMLResponse)
async def view_last_email():
    """Devuelve la última plantilla HTML de correo generada para previsualización."""
    email_path = BASE_DIR / "emails_enviados" / "ultima_alerta.html"
    if not email_path.exists():
        raise HTTPException(status_code=404, detail="No se ha generado ningún correo de alerta todavía.")
    return HTMLResponse(content=email_path.read_text(encoding="utf-8"))


@app.post("/api/inspect")
async def inspect_file(file: UploadFile = File(...)):
    """Inspecciona las hojas y columnas de un archivo Excel subido."""
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
        raise HTTPException(status_code=400, detail="Formato no soportado. Sube un archivo .xlsx o .xls")

    try:
        content = await file.read()
        metadata = inspect_excel(content)
        return metadata
    except Exception as exc:
        logger.error(f"Error al inspeccionar archivo: {exc}")
        raise HTTPException(status_code=400, detail=f"No se pudo leer el archivo Excel: {str(exc)}")


@app.post("/api/reconcile")
async def reconcile_endpoint(
    background_tasks: BackgroundTasks,
    file_a: UploadFile = File(...),
    file_b: UploadFile = File(...),
    key_a: str = Form(...),
    key_b: str = Form(...),
    send_email: bool = Form(True),
):
    """
    Carga dos tablas de Excel, efectúa la reconciliación y dispara la alerta por correo si hay desacuerdos.
    """
    for f in (file_a, file_b):
        if not (f.filename.endswith(".xlsx") or f.filename.endswith(".xls")):
            raise HTTPException(
                status_code=400,
                detail=f"El archivo '{f.filename}' no tiene extensión válida (.xlsx, .xls)",
            )

    try:
        bytes_a = await file_a.read()
        bytes_b = await file_b.read()

        df_a = load_excel(bytes_a)
        df_b = load_excel(bytes_b)

        key_a_clean = key_a.strip()
        key_b_clean = key_b.strip()

        result = reconcile_tables(df_a, df_b, key_a=key_a_clean, key_b=key_b_clean)

        email_status = None
        if send_email and result.has_discrepancies:
            # Enviamos o programamos la tarea de correo
            email_status = trigger_alert_if_discrepancies(result)

        response_data = result.to_dict()
        response_data["email_status"] = email_status
        return JSONResponse(content=response_data)

    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as exc:
        logger.exception("Error durante la conciliación:")
        raise HTTPException(status_code=500, detail=f"Error al procesar las tablas: {str(exc)}")


@app.get("/api/reconcile-sample")
async def reconcile_sample(send_email: bool = False):
    """Ejecuta la conciliación con el dataset empresarial enriquecido."""
    ejemplos_dir = BASE_DIR / "ejemplos_excel"
    path_a = ejemplos_dir / "Dataset_Empresarial_ERP_Tabla_A.xlsx"
    path_b = ejemplos_dir / "Dataset_Empresarial_Banco_Tabla_B.xlsx"

    if path_a.exists() and path_b.exists():
        key = "ID_Transaccion"
    else:
        sample_dir = BASE_DIR / "sample_data"
        path_a = sample_dir / "tabla_a.xlsx"
        path_b = sample_dir / "tabla_b.xlsx"
        key = "ID_Factura"

    if not (path_a.exists() and path_b.exists()):
        raise HTTPException(status_code=404, detail="Archivos de muestra no encontrados.")

    df_a = load_excel(path_a)
    df_b = load_excel(path_b)

    result = reconcile_tables(df_a, df_b, key_a=key, key_b=key)

    email_status = None
    if send_email and result.has_discrepancies:
        email_status = trigger_alert_if_discrepancies(result)

    response_data = result.to_dict()
    response_data["email_status"] = email_status
    return JSONResponse(content=response_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
