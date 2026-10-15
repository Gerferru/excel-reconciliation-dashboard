from pathlib import Path
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def test_e2e_reconciliation_with_samples():
    path_a = SAMPLE_DIR / "tabla_a.xlsx"
    path_b = SAMPLE_DIR / "tabla_b.xlsx"

    assert path_a.exists(), "tabla_a.xlsx debe existir"
    assert path_b.exists(), "tabla_b.xlsx debe existir"

    with open(path_a, "rb") as fa, open(path_b, "rb") as fb:
        files = {
            "file_a": ("tabla_a.xlsx", fa.read(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            "file_b": ("tabla_b.xlsx", fb.read(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        }
        data = {
            "key_a": "ID_Factura",
            "key_b": "ID_Factura",
            "send_email": "true",
        }

        response = client.post("/api/reconcile", files=files, data=data)

    assert response.status_code == 200
    res = response.json()

    # Validar métricas exactas
    assert res["total_a"] == 6
    assert res["total_b"] == 6
    assert res["total_unique_keys"] == 8
    assert res["fully_matched_count"] == 2  # FACT-001 y FACT-002
    assert res["missing_in_b_count"] == 2  # FACT-005 y FACT-006
    assert res["missing_in_a_count"] == 2  # FACT-007 y FACT-008
    assert res["value_mismatch_count"] == 2  # FACT-003 (Monto) y FACT-004 (Estado)
    assert res["total_discrepancies"] == 6
    assert res["match_percentage"] == 25.0
    assert res["has_discrepancies"] is True

    # Validar activación de correo de alerta
    assert res["email_status"] is not None
    assert res["email_status"]["alert_triggered"] is True
