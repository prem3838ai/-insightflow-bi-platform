from __future__ import annotations
from io import BytesIO, StringIO
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"order_date", "region", "product", "category", "quantity", "revenue", "cost"}
NUMERIC_COLUMNS = ["quantity", "unit_price", "discount_pct", "revenue", "cost", "profit"]

def load_csv(source) -> pd.DataFrame:
    """Load a CSV path, bytes, or file-like object and normalize its schema."""
    if isinstance(source, (str, Path)):
        df = pd.read_csv(source)
    elif isinstance(source, bytes):
        df = pd.read_csv(BytesIO(source))
    else:
        df = pd.read_csv(source)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        raise ValueError("CSV is missing required columns: " + ", ".join(missing))
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    if df["order_date"].isna().all():
        raise ValueError("No valid dates found in order_date.")
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "profit" not in df.columns:
        df["profit"] = df["revenue"] - df["cost"]
    df["quantity"] = df["quantity"].fillna(0)
    df["revenue"] = df["revenue"].fillna(0)
    df["cost"] = df["cost"].fillna(0)
    df["profit"] = df["profit"].fillna(df["revenue"] - df["cost"])
    for col in ["region", "product", "category"]:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()
    if "sales_channel" not in df.columns: df["sales_channel"] = "Unknown"
    if "customer_id" not in df.columns: df["customer_id"] = "Unknown"
    if "order_id" not in df.columns: df["order_id"] = [f"ROW-{i+1}" for i in range(len(df))]
    df = df.dropna(subset=["order_date"]).copy()
    if df.empty: raise ValueError("No usable rows remain after validating order_date.")
    df["margin_pct"] = (df["profit"] / df["revenue"].replace(0, pd.NA) * 100).fillna(0)
    return df

def sample_data_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "sample" / "sales_data.csv"
