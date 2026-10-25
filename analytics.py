from __future__ import annotations
import pandas as pd

def filter_data(df: pd.DataFrame, start_date=None, end_date=None, regions=None, categories=None, channels=None) -> pd.DataFrame:
    out = df.copy()
    if start_date is not None: out = out[out["order_date"].dt.date >= start_date]
    if end_date is not None: out = out[out["order_date"].dt.date <= end_date]
    if regions: out = out[out["region"].isin(regions)]
    if categories: out = out[out["category"].isin(categories)]
    if channels and "sales_channel" in out: out = out[out["sales_channel"].isin(channels)]
    return out

def calculate_kpis(df: pd.DataFrame) -> dict:
    revenue = float(df["revenue"].sum()) if not df.empty else 0.0
    cost = float(df["cost"].sum()) if not df.empty else 0.0
    profit = float(df["profit"].sum()) if not df.empty else 0.0
    orders = int(df["order_id"].nunique()) if not df.empty else 0
    customers = int(df["customer_id"].nunique()) if not df.empty else 0
    units = int(df["quantity"].sum()) if not df.empty else 0
    return {"revenue": revenue, "cost": cost, "profit": profit, "orders": orders, "customers": customers, "units": units, "profit_margin_pct": (profit / revenue * 100) if revenue else 0.0, "average_order_value": (revenue / orders) if orders else 0.0}

def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return pd.DataFrame(columns=["month", "revenue", "profit", "orders"])
    out = df.copy(); out["month"] = out["order_date"].dt.to_period("M").dt.to_timestamp()
    return out.groupby("month", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")).sort_values("month")

def top_products(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    if df.empty: return pd.DataFrame(columns=["product", "revenue", "profit", "quantity"])
    return df.groupby("product", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), quantity=("quantity", "sum")).sort_values("revenue", ascending=False).head(limit)

def executive_summary(df: pd.DataFrame) -> str:
    k = calculate_kpis(df)
    if df.empty: return "No records match the selected filters. Broaden the date range or remove a filter to generate insights."
    best_region = df.groupby("region")["revenue"].sum().idxmax()
    best_product = df.groupby("product")["revenue"].sum().idxmax()
    return (f"The selected dataset contains {k['orders']:,} orders across {k['customers']:,} customers, "
            f"generating {k['revenue']:,.2f} in revenue and {k['profit']:,.2f} in profit. "
            f"Overall profit margin is {k['profit_margin_pct']:.1f}%. The strongest region by revenue is {best_region}, "
            f"while {best_product} is the top product by revenue. Average order value is {k['average_order_value']:,.2f}.")
