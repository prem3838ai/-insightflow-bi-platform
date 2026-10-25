from pathlib import Path
import sys
from datetime import date
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from bi_platform.data import load_csv, sample_data_path
from bi_platform.analytics import filter_data, calculate_kpis, monthly_summary, top_products, executive_summary

st.set_page_config(page_title="InsightFlow | BI Platform", page_icon="📊", layout="wide")
st.markdown("""<style>
.block-container{padding-top:1.7rem;padding-bottom:2rem}.hero{padding:1.4rem 1.6rem;border-radius:16px;background:linear-gradient(120deg,#102a43,#1f6f8b);color:white;margin-bottom:1rem}.hero h1{color:white;margin:0}.hero p{color:#e5f4fa;margin:.35rem 0 0 0}.metric-note{color:#627d98;font-size:.82rem}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>📊 InsightFlow</h1><p>Business Intelligence & Automated Reporting Platform · Explore sales performance, uncover trends, export insights.</p></div>', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_default(): return load_csv(sample_data_path())

with st.sidebar:
    st.header("Data source")
    uploaded = st.file_uploader("Upload a sales CSV", type=["csv"], help="Required: order_date, region, product, category, quantity, revenue, cost")
    try:
        raw = load_csv(uploaded.getvalue()) if uploaded else load_default()
        st.success(f"Loaded {len(raw):,} rows")
    except Exception as exc:
        st.error(str(exc)); st.stop()
    st.divider(); st.header("Filters")
    min_d, max_d = raw.order_date.min().date(), raw.order_date.max().date()
    dates = st.date_input("Order date range", value=(min_d,max_d), min_value=min_d, max_value=max_d)
    if isinstance(dates, (tuple,list)) and len(dates)==2: start_d,end_d=dates
    else: start_d=end_d=dates
    regions = st.multiselect("Region", sorted(raw.region.unique()), default=sorted(raw.region.unique()))
    categories = st.multiselect("Category", sorted(raw.category.unique()), default=sorted(raw.category.unique()))
    channels = st.multiselect("Sales channel", sorted(raw.sales_channel.unique()), default=sorted(raw.sales_channel.unique()))
    st.caption("Demo data is synthetic. Currency values are shown in dataset units.")

df=filter_data(raw,start_d,end_d,regions,categories,channels)
k=calculate_kpis(df)
tab1,tab2,tab3,tab4=st.tabs(["Executive overview","Product & region","Data explorer","Export report"])
with tab1:
    st.subheader("Performance at a glance")
    a,b,c,d=st.columns(4)
    a.metric("Revenue",f"{k['revenue']:,.0f}"); b.metric("Profit",f"{k['profit']:,.0f}"); c.metric("Profit margin",f"{k['profit_margin_pct']:.1f}%"); d.metric("Orders",f"{k['orders']:,}")
    e,f,g=st.columns(3); e.metric("Customers",f"{k['customers']:,}"); f.metric("Units sold",f"{k['units']:,}"); g.metric("Average order value",f"{k['average_order_value']:,.2f}")
    left,right=st.columns([1.5,1])
    with left:
        st.markdown("#### Revenue and profit trend")
        monthly=monthly_summary(df)
        if not monthly.empty: st.plotly_chart(px.line(monthly,x="month",y=["revenue","profit"],markers=True,labels={"month":"Month","value":"Amount","variable":"Metric"}),use_container_width=True)
        else: st.info("No data for the selected filters.")
    with right:
        st.markdown("#### Revenue by region")
        region_df=df.groupby("region",as_index=False).revenue.sum().sort_values("revenue",ascending=False)
        if not region_df.empty: st.plotly_chart(px.pie(region_df,names="region",values="revenue",hole=.48),use_container_width=True)
    st.markdown("#### Auto-generated executive summary")
    st.info(executive_summary(df))
with tab2:
    left,right=st.columns(2)
    with left:
        st.markdown("#### Top products by revenue")
        tp=top_products(df,10)
        if not tp.empty: st.plotly_chart(px.bar(tp.sort_values("revenue"),x="revenue",y="product",orientation="h",color="profit",color_continuous_scale="Tealgrn"),use_container_width=True)
    with right:
        st.markdown("#### Profit by category")
        cat=df.groupby("category",as_index=False).agg(revenue=("revenue","sum"),profit=("profit","sum"))
        if not cat.empty: st.plotly_chart(px.bar(cat,x="category",y=["revenue","profit"],barmode="group"),use_container_width=True)
    st.markdown("#### Region performance")
    reg=df.groupby("region",as_index=False).agg(revenue=("revenue","sum"),profit=("profit","sum"),orders=("order_id","nunique"))
    if not reg.empty: st.dataframe(reg.style.format({"revenue":"{:,.2f}","profit":"{:,.2f}"}),use_container_width=True,hide_index=True)
with tab3:
    st.subheader("Filtered transaction records")
    st.caption(f"Showing {len(df):,} of {len(raw):,} rows")
    search=st.text_input("Search order, product, or customer")
    shown=df
    if search:
        mask=shown.astype(str).apply(lambda col: col.str.contains(search,case=False,na=False)).any(axis=1); shown=shown[mask]
    st.dataframe(shown.sort_values("order_date",ascending=False),use_container_width=True,hide_index=True)
with tab4:
    st.subheader("Export your filtered report")
    st.write("Download the filtered rows, monthly summary, or an executive report in Markdown format.")
    col1,col2,col3=st.columns(3)
    col1.download_button("Download filtered CSV",df.to_csv(index=False).encode("utf-8"),"filtered_sales.csv","text/csv",use_container_width=True)
    col2.download_button("Download monthly summary",monthly_summary(df).to_csv(index=False).encode("utf-8"),"monthly_summary.csv","text/csv",use_container_width=True)
    report=f"# InsightFlow Executive Report\n\nGenerated on: {date.today().isoformat()}\n\n## Summary\n\n{executive_summary(df)}\n\n## KPIs\n\n| Metric | Value |\n|---|---:|\n| Revenue | {k['revenue']:,.2f} |\n| Cost | {k['cost']:,.2f} |\n| Profit | {k['profit']:,.2f} |\n| Profit margin | {k['profit_margin_pct']:.2f}% |\n| Orders | {k['orders']} |\n| Customers | {k['customers']} |\n| Units sold | {k['units']} |\n| Average order value | {k['average_order_value']:,.2f} |\n"
    col3.download_button("Download executive report",report.encode("utf-8"),"executive_report.md","text/markdown",use_container_width=True)
    st.caption("Tip: Export filtered CSV to continue analysis in Excel, Power BI, or Python.")
st.divider(); st.caption("InsightFlow Portfolio Project · Built with Python, Streamlit, Pandas and Plotly")
