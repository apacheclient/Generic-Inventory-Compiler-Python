from __future__ import annotations
import pandas as pd
from pathlib import Path

class InventoryReconciler:
    def __init__(self, system_csv: str | Path, physical_csv: str | Path):
        self.system_path = Path(system_csv)
        self.physical_path = Path(physical_csv)
        self.system_df = None
        self.physical_df = None
        self.results_df = None

    def load_data(self) -> None:
        self.system_df = pd.read_csv(self.system_path)
        self.physical_df = pd.read_csv(self.physical_path)

    def reconcile(self) -> pd.DataFrame:
        if self.system_df is None or self.physical_df is None:
            self.load_data()

        merged = pd.merge(
            self.system_df,
            self.physical_df[["sku", "physical_qty", "counted_by", "count_date"]],
            on="sku",
            how="left"
        )

        merged["physical_qty"] = merged["physical_qty"].fillna(0).astype(int)
        merged["system_qty"] = merged["system_qty"].astype(int)
        merged["variance_qty"] = merged["physical_qty"] - merged["system_qty"]
        merged["variance_value"] = (merged["variance_qty"] * merged["unit_cost"]).round(2)
        merged["abs_variance_value"] = merged["variance_value"].abs()

        def classify_severity(row):
            abs_val = abs(row["variance_value"])
            abs_qty = abs(row["variance_qty"])
            if abs_qty == 0:
                return "MATCH"
            if abs_val >= 50 or abs_qty >= 20:
                return "CRITICAL"
            if abs_val >= 20 or abs_qty >= 10:
                return "HIGH"
            if abs_val >= 5 or abs_qty >= 4:
                return "MEDIUM"
            return "LOW"

        merged["severity"] = merged.apply(classify_severity, axis=1)
        merged["status"] = merged["variance_qty"].apply(
            lambda x: "SHORT" if x < 0 else ("OVER" if x > 0 else "MATCH")
        )

        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "MATCH": 4}
        merged["_sev_rank"] = merged["severity"].map(severity_order)
        merged = merged.sort_values(
            by=["_sev_rank", "abs_variance_value"],
            ascending=[True, False]
        ).reset_index(drop=True)

        cols = [
            "sku", "product_name", "category", "unit_cost",
            "system_qty", "physical_qty", "variance_qty",
            "variance_value", "severity", "status",
            "counted_by", "count_date"
        ]
        self.results_df = merged[cols]
        return self.results_df

    def summary(self) -> dict:
        if self.results_df is None:
            self.reconcile()
        df = self.results_df
        total = len(df)
        matched = len(df[df["status"] == "MATCH"])
        return {
            "total_skus": total,
            "matched": matched,
            "shortages": len(df[df["status"] == "SHORT"]),
            "overages": len(df[df["status"] == "OVER"]),
            "match_rate_pct": round((matched / total) * 100, 1) if total else 0,
            "total_shrink_dollars": round(df[df["variance_value"] < 0]["variance_value"].sum(), 2),
            "total_overage_dollars": round(df[df["variance_value"] > 0]["variance_value"].sum(), 2),
            "net_variance_dollars": round(df["variance_value"].sum(), 2),
            "critical_count": len(df[df["severity"] == "CRITICAL"]),
            "high_count": len(df[df["severity"] == "HIGH"]),
        }

    def get_discrepancies(self, min_severity: str = "LOW") -> pd.DataFrame:
        if self.results_df is None:
            self.reconcile()
        order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "MATCH": 4}
        min_level = order.get(min_severity.upper(), 3)
        mask = self.results_df["severity"].map(order) <= min_level
        return self.results_df[mask & (self.results_df["status"] != "MATCH")].copy()

    def export_report(self, output_path: str, only_discrepancies: bool = True):
        if self.results_df is None:
            self.reconcile()
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df = self.get_discrepancies() if only_discrepancies else self.results_df
        if path.suffix.lower() in [".xlsx", ".xls"]:
            df.to_excel(path, index=False)
        else:
            df.to_csv(path, index=False)
        return path
