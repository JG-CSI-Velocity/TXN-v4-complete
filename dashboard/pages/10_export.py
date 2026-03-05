import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

st.markdown(
    '<h1 style="font-family:Outfit,sans-serif; font-size:1.8rem; '
    'letter-spacing:-0.03em; margin-bottom:2px;">Export Deck</h1>'
    '<p style="color:#64748B; font-size:13px; margin-bottom:24px;">'
    'Generate conference-quality PPTX from analysis results</p>',
    unsafe_allow_html=True,
)

st.divider()

ARC_SECTIONS = {
    "Executive": ["The Bottom Line"],
    "Story Arcs": [
        "Portfolio Illusions",
        "Where the Money Goes",
        "The Loyalty Myth",
        "The Revenue You're Missing",
        "The Attrition Cascade",
        "Deepening or Decline",
    ],
    "Operations": ["Branch Performance", "Campaign Effectiveness"],
}

st.subheader("Select Sections to Include")

col1, col2 = st.columns(2)
selected = {}

with col1:
    for group in ["Executive", "Story Arcs"]:
        st.markdown(f"**{group}**")
        for section in ARC_SECTIONS[group]:
            selected[section] = st.checkbox(section, value=True, key=section)

with col2:
    for group in ["Operations"]:
        st.markdown(f"**{group}**")
        for section in ARC_SECTIONS[group]:
            selected[section] = st.checkbox(section, value=True, key=section)

n_selected = sum(selected.values())
st.markdown(f"**{n_selected} sections selected** -- estimated {n_selected * 4 + 2} slides")

st.divider()

st.subheader("Export Options")
c1, c2 = st.columns(2)
with c1:
    st.selectbox("Template", ["Conference (Dark)", "Executive Brief (Light)", "Board Report"])
    st.checkbox("Include speaker notes", value=True)
    st.checkbox("Include data appendix", value=False)
with c2:
    st.selectbox("Chart style", ["Plotly (interactive PDF)", "Matplotlib (static high-res)"])
    st.checkbox("Include action roadmap slide", value=True)
    st.checkbox("Include raw data tables (CSV)", value=False)

st.divider()

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    if st.button("Generate Deck", type="primary", use_container_width=True):
        with st.spinner("Building slides..."):
            import time
            bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                bar.progress(i + 1)
            st.success(f"Deck generated: {n_selected * 4 + 2} slides")
            st.balloons()

with c2:
    st.download_button(
        "Download PPTX",
        data=b"placeholder",
        file_name="TXN_Analysis_CoastHills_2026.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        use_container_width=True,
        disabled=True,
        help="Available after generating deck",
    )

with c3:
    st.download_button(
        "Download CSV Data",
        data=b"placeholder",
        file_name="TXN_Data_Export_CoastHills_2026.csv",
        mime="text/csv",
        use_container_width=True,
        disabled=True,
        help="Available after generating deck",
    )

st.divider()
st.subheader("Slide Preview")
st.info("Slide thumbnails will appear here after deck generation. "
        "Each arc produces 3-4 slides: objection banner, primary evidence, supporting charts, and action roadmap.")

cols = st.columns(4)
for i, col in enumerate(cols):
    with col:
        st.markdown(
            f'<div style="background:rgba(30,41,59,0.5); border:1px solid #1E293B; '
            f'border-radius:8px; height:120px; display:flex; align-items:center; '
            f'justify-content:center; color:#475569; font-size:13px;">Slide {i+1}</div>',
            unsafe_allow_html=True,
        )
