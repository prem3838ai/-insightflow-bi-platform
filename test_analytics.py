import sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from bi_platform.analytics import calculate_kpis, filter_data, monthly_summary, top_products, executive_summary
from bi_platform.data import load_csv

def sample():
    return load_csv(pd.DataFrame({"order_date":["2025-01-01","2025-01-15","2025-02-02"],"region":["North","South","North"],"product":["A","B","A"],"category":["X","Y","X"],"quantity":[2,1,3],"revenue":[100,50,150],"cost":[60,30,90],"order_id":["1","2","3"],"customer_id":["c1","c2","c1"],"sales_channel":["Online","Retail","Online"]}).to_csv(index=False).encode())

def test_kpis_calculated():
    k=calculate_kpis(sample()); assert k["revenue"]==300; assert k["profit"]==120; assert k["orders"]==3; assert round(k["profit_margin_pct"],2)==40

def test_filter_by_region():
    df=filter_data(sample(),regions=["North"]); assert len(df)==2; assert set(df.region)=={"North"}

def test_monthly_summary():
    m=monthly_summary(sample()); assert len(m)==2; assert list(m.revenue)==[150,150]

def test_top_products():
    t=top_products(sample(),1); assert t.iloc[0]["product"]=="A"

def test_summary_handles_empty():
    df=sample().iloc[0:0]; assert "No records" in executive_summary(df)
