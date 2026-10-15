import pandas as pd
from reconciliation.engine import reconcile_tables


def test_reconciliation_exact_match():
    df_a = pd.DataFrame({"ID": ["001", "002"], "Monto": [100.0, 200.0]})
    df_b = pd.DataFrame({"ID": ["001", "002"], "Monto": [100.0, 200.0]})

    result = reconcile_tables(df_a, df_b, key_a="ID", key_b="ID")
    assert result.has_discrepancies is False
    assert result.match_percentage == 100.0
    assert result.fully_matched_count == 2
    assert len(result.discrepancies) == 0


def test_reconciliation_missing_and_mismatch():
    # A tiene 001, 002, 003
    df_a = pd.DataFrame({
        "ID": ["001", "002", "003"],
        "Descripcion": ["A", "B", "C"],
        "Total": [10.0, 20.0, 30.0]
    })
    # B tiene 001 (con monto diferente), 002 (exacto), 004 (falta en A)
    df_b = pd.DataFrame({
        "ID": ["001", "002", "004"],
        "Descripcion": ["A", "B", "D"],
        "Total": [15.0, 20.0, 40.0]
    })

    result = reconcile_tables(df_a, df_b, key_a="ID", key_b="ID")
    assert result.has_discrepancies is True
    assert result.fully_matched_count == 1  # Solo 002 es exacto
    assert result.missing_in_b_count == 1  # 003 falta en B
    assert result.missing_in_a_count == 1  # 004 falta en A
    assert result.value_mismatch_count == 1  # 001 tiene Total 10 vs 15

    types = [d.type for d in result.discrepancies]
    assert "MISSING_IN_B" in types
    assert "MISSING_IN_A" in types
    assert "VALUE_MISMATCH" in types
