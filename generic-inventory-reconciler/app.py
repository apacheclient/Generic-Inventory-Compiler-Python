import streamlit as st
from src.reconciler import InventoryReconciler

st.set_page_config(page_title="Inventory Reconciler", page_icon="📦", layout="wide")
st.title("📦 Inventory Reconciler")
st.caption("System of Record vs Physical Count")

min_severity = st.sidebar.selectbox("Minimum Severity", ["CRITICAL", "HIGH", "MEDIUM", "LOW"], index=3)

reconciler = InventoryReconciler("data/system_inventory.csv", "data/physical_count.csv")
results = reconciler.reconcile()
summary = reconciler.summary()
discrepancies = reconciler.get_discrepancies(min_severity=min_severity)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total SKUs", summary["total_skus"])
c2.metric("Match Rate", f"{summary['match_rate_pct']}%")
c3.metric("Shortages", summary["shortages"])
c4.metric("Critical", summary["critical_count"])
c5.metric("Net Variance", f"${summary['net_variance_dollars']:,.2f}")

st.divider()
st.subheader("Discrepancies")
if discrepancies.empty:
    st.success("No discrepancies found!")
else:
    st.dataframe(discrepancies, use_container_width=True, height=400)

st.download_button(
    "Download CSV",
    data=discrepancies.to_csv(index=False).encode("utf-8"),
    file_name="discrepancies.csv",
    mime="text/csv"
)
