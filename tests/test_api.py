import io
import pandas as pd
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home_page_renders_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "Excel Reconciler & Auditor" in response.text
    assert "<form id=\"reconcileForm\"" in response.text


def test_reconcile_api_endpoint():
    # Crear dos Excels en memoria
    df_a = pd.DataFrame({"ID": [1, 2], "Importe": [100.0, 250.0]})
    df_b = pd.DataFrame({"ID": [1, 3], "Importe": [100.0, 300.0]})

    buf_a = io.BytesIO()
    buf_b = io.BytesIO()
    df_a.to_excel(buf_a, index=False)
    df_b.to_excel(buf_b, index=False)

    files = {
        "file_a": ("tabla_a.xlsx", buf_a.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        "file_b": ("tabla_b.xlsx", buf_b.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    }
    data = {
        "key_a": "ID",
        "key_b": "ID",
        "send_email": "false",
    }

    response = client.post("/api/reconcile", files=files, data=data)
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["total_unique_keys"] == 3
    assert res_json["fully_matched_count"] == 1
    assert res_json["missing_in_b_count"] == 1  # ID 2 falta en B
    assert res_json["missing_in_a_count"] == 1  # ID 3 falta en A
    assert res_json["has_discrepancies"] is True
