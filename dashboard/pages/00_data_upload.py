import streamlit as st

st.header("Data Upload & Pipeline")
st.caption("Upload transaction files and ODDD rewards data to run the analysis pipeline")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Transaction Files")
    st.file_uploader("Upload CSV/TXT transaction files", type=['csv', 'txt'],
                     accept_multiple_files=True, key='txn_files')
    st.caption("Expected: monthly transaction extracts with 13 columns")

with col2:
    st.subheader("ODDD Rewards File")
    st.file_uploader("Upload ODDD Excel file", type=['xlsx', 'xls'], key='oddd_file')
    st.caption("Expected: rewards/demographics with 235+ columns")

st.divider()

st.subheader("Client Configuration")
c1, c2, c3 = st.columns(3)
c1.selectbox("Client ID", ['1776 - CoastHills', '1234 - Sample CU', '5678 - Demo CU'])
c2.number_input("Recent Months", value=13, min_value=3, max_value=24)
c3.selectbox("File Extension", ['txt', 'csv'])

st.divider()

if st.button("Run Pipeline", type="primary", use_container_width=True):
    import time
    bar = st.progress(0, text="Initializing...")
    steps = [
        (10, "Loading transaction files..."),
        (25, "Combining monthly extracts..."),
        (40, "Consolidating merchant names..."),
        (55, "Loading ODDD rewards data..."),
        (65, "Merging account demographics..."),
        (75, "Splitting business/personal..."),
        (85, "Computing engagement tiers..."),
        (95, "Building analysis DataFrames..."),
        (100, "Pipeline complete!"),
    ]
    for pct, msg in steps:
        bar.progress(pct, text=msg)
        time.sleep(0.4)
    st.success("Loaded 5,885,334 transactions across 33,205 accounts (Jan25-Jan26)")
    st.info("Data cached -- subsequent page loads will be instant")

st.divider()
st.subheader("Data Quality Summary")
st.markdown("*Available after pipeline run*")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Transaction Rows", "5,885,334")
c2.metric("ODDD Accounts", "33,205")
c3.metric("Date Range", "Jan25-Jan26")
c4.metric("Missing Values", "0.2%")
