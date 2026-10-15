from dataclasses import dataclass, field
from typing import Any, Optional
import numpy as np
import pandas as pd


@dataclass
class DiscrepancyItem:
    key: Any
    type: str  # 'MISSING_IN_B', 'MISSING_IN_A', 'VALUE_MISMATCH'
    column: Optional[str] = None
    value_a: Any = None
    value_b: Any = None
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": str(self.key),
            "type": self.type,
            "column": self.column or "-",
            "value_a": "-" if self.value_a is None or (isinstance(self.value_a, float) and np.isnan(self.value_a)) else str(self.value_a),
            "value_b": "-" if self.value_b is None or (isinstance(self.value_b, float) and np.isnan(self.value_b)) else str(self.value_b),
            "description": self.description,
        }


@dataclass
class ReconciliationResult:
    total_a: int
    total_b: int
    total_unique_keys: int
    fully_matched_count: int
    missing_in_b_count: int
    missing_in_a_count: int
    value_mismatch_count: int
    match_percentage: float
    has_discrepancies: bool
    compared_columns: list[str]
    discrepancies: list[DiscrepancyItem] = field(default_factory=list)
    discrepancies_by_column: dict[str, int] = field(default_factory=dict)
    financial_impact: float = 0.0

    @property
    def total_discrepancies(self) -> int:
        return len(self.discrepancies)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_a": self.total_a,
            "total_b": self.total_b,
            "total_unique_keys": self.total_unique_keys,
            "fully_matched_count": self.fully_matched_count,
            "missing_in_b_count": self.missing_in_b_count,
            "missing_in_a_count": self.missing_in_a_count,
            "value_mismatch_count": self.value_mismatch_count,
            "total_discrepancies": len(self.discrepancies),
            "match_percentage": round(self.match_percentage, 2),
            "has_discrepancies": self.has_discrepancies,
            "compared_columns": self.compared_columns,
            "discrepancies_by_column": self.discrepancies_by_column,
            "financial_impact": round(self.financial_impact, 2),
            "discrepancies": [d.to_dict() for d in self.discrepancies],
        }


def _are_values_equal(val_a: Any, val_b: Any, tolerance: float = 0.001) -> bool:
    """Compara dos valores con soporte para nulos, números flotantes y cadenas."""
    # Ambos NaN o None
    a_is_null = pd.isna(val_a) or val_a is None or str(val_a).strip() == ""
    b_is_null = pd.isna(val_b) or val_b is None or str(val_b).strip() == ""
    if a_is_null and b_is_null:
        return True
    if a_is_null or b_is_null:
        return False

    # Comparación numérica si es posible
    try:
        num_a = float(val_a)
        num_b = float(val_b)
        return abs(num_a - num_b) <= tolerance
    except (ValueError, TypeError):
        pass

    # Comparación como texto limpio
    return str(val_a).strip() == str(val_b).strip()


def reconcile_tables(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    key_a: str,
    key_b: str,
    columns_to_compare: Optional[list[str]] = None,
    tolerance: float = 0.001,
) -> ReconciliationResult:
    """
    Realiza la conciliación cruzando ambas tablas por su columna clave.
    """
    if key_a not in df_a.columns:
        raise ValueError(f"La clave '{key_a}' no existe en la Tabla A.")
    if key_b not in df_b.columns:
        raise ValueError(f"La clave '{key_b}' no existe en la Tabla B.")

    # Copias de trabajo
    a = df_a.copy()
    b = df_b.copy()

    # Normalizar columna clave a string para emparejar
    a["_KEY_"] = a[key_a].astype(str).str.strip()
    b["_KEY_"] = b[key_b].astype(str).str.strip()

    # Identificar columnas a comparar
    cols_a = set(a.columns) - {key_a, "_KEY_"}
    cols_b = set(b.columns) - {key_b, "_KEY_"}

    if columns_to_compare is not None:
        valid_cols = [c for c in columns_to_compare if c in cols_a and c in cols_b]
    else:
        valid_cols = sorted(list(cols_a.intersection(cols_b)))

    # Realizar outer join
    merged = pd.merge(
        a,
        b,
        on="_KEY_",
        how="outer",
        suffixes=("_A", "_B"),
        indicator=True,
    )

    discrepancies: list[DiscrepancyItem] = []
    discrepancies_by_column: dict[str, int] = {}
    financial_impact: float = 0.0
    missing_in_b = 0
    missing_in_a = 0
    value_mismatches = 0
    fully_matched_keys = set()

    # Identificar posibles columnas monetarias
    amount_cols = [c for c in valid_cols if any(term in c.lower() for term in ("importe", "monto", "total", "precio", "base"))]

    for _, row in merged.iterrows():
        key_val = row["_KEY_"]
        merge_status = row["_merge"]

        if merge_status == "left_only":
            missing_in_b += 1
            for ac in amount_cols:
                try:
                    val = float(row.get(f"{ac}_A", 0))
                    if not pd.isna(val):
                        financial_impact += abs(val)
                except (ValueError, TypeError):
                    pass
            discrepancies.append(
                DiscrepancyItem(
                    key=key_val,
                    type="MISSING_IN_B",
                    description=f"Registro presente en Tabla A pero ausente en Tabla B (Clave: {key_val})",
                )
            )
        elif merge_status == "right_only":
            missing_in_a += 1
            for ac in amount_cols:
                try:
                    val = float(row.get(f"{ac}_B", 0))
                    if not pd.isna(val):
                        financial_impact += abs(val)
                except (ValueError, TypeError):
                    pass
            discrepancies.append(
                DiscrepancyItem(
                    key=key_val,
                    type="MISSING_IN_A",
                    description=f"Registro presente en Tabla B pero ausente en Tabla A (Clave: {key_val})",
                )
            )
        else:
            # Ambas tablas contienen la clave. Verificamos valores de columnas
            row_has_mismatch = False
            for col in valid_cols:
                val_a = row.get(f"{col}_A")
                val_b = row.get(f"{col}_B")

                if not _are_values_equal(val_a, val_b, tolerance):
                    row_has_mismatch = True
                    value_mismatches += 1
                    discrepancies_by_column[col] = discrepancies_by_column.get(col, 0) + 1

                    # Impacto financiero si es columna de importe
                    try:
                        num_a = float(val_a)
                        num_b = float(val_b)
                        if not (pd.isna(num_a) or pd.isna(num_b)):
                            financial_impact += abs(num_a - num_b)
                    except (ValueError, TypeError):
                        pass

                    discrepancies.append(
                        DiscrepancyItem(
                            key=key_val,
                            type="VALUE_MISMATCH",
                            column=col,
                            value_a=val_a,
                            value_b=val_b,
                            description=f"Diferencia en columna '{col}' para la clave {key_val}",
                        )
                    )

            if not row_has_mismatch:
                fully_matched_keys.add(key_val)

    total_unique_keys = len(merged)
    total_fully_matched = len(fully_matched_keys)
    match_percentage = (
        (total_fully_matched / total_unique_keys * 100.0)
        if total_unique_keys > 0
        else 100.0
    )
    has_discrepancies = len(discrepancies) > 0

    return ReconciliationResult(
        total_a=len(df_a),
        total_b=len(df_b),
        total_unique_keys=total_unique_keys,
        fully_matched_count=total_fully_matched,
        missing_in_b_count=missing_in_b,
        missing_in_a_count=missing_in_a,
        value_mismatch_count=value_mismatches,
        match_percentage=match_percentage,
        has_discrepancies=has_discrepancies,
        compared_columns=valid_cols,
        discrepancies=discrepancies,
        discrepancies_by_column=discrepancies_by_column,
        financial_impact=financial_impact,
    )
