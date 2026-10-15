import pandas as pd
from reconciliation.engine import reconcile_tables
from notifications.mailer import render_alert_html, trigger_alert_if_discrepancies


def test_render_alert_html():
    df_a = pd.DataFrame({"ID": ["A1"], "Monto": [100.0]})
    df_b = pd.DataFrame({"ID": ["A1"], "Monto": [150.0]})
    result = reconcile_tables(df_a, df_b, key_a="ID", key_b="ID")

    html = render_alert_html(result)
    assert "Alerta de Discrepancias Detectadas" in html
    assert "A1" in html
    assert "100.0" in html
    assert "150.0" in html


def test_no_alert_when_no_discrepancies():
    df_a = pd.DataFrame({"ID": ["A1"], "Monto": [100.0]})
    df_b = pd.DataFrame({"ID": ["A1"], "Monto": [100.0]})
    result = reconcile_tables(df_a, df_b, key_a="ID", key_b="ID")

    status = trigger_alert_if_discrepancies(result)
    assert status["alert_triggered"] is False


def test_alert_triggered_safely_when_discrepancies():
    df_a = pd.DataFrame({"ID": ["A1", "A2"], "Monto": [100.0, 200.0]})
    df_b = pd.DataFrame({"ID": ["A1"], "Monto": [100.0]})
    result = reconcile_tables(df_a, df_b, key_a="ID", key_b="ID")

    # Debe disparar la alerta y manejar el resultado de red de forma segura sin romper la ejecución
    status = trigger_alert_if_discrepancies(result)
    assert status["alert_triggered"] is True
    # Dado que es localhost sin un servidor SMTP real corriendo en test, success reporta el estado
    assert "message" in status
