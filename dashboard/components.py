"""Narrative UI components for the story-driven dashboard."""

import streamlit as st
from config import GEN_COLORS


def arc_header(title: str, subtitle: str, objection: str, reality: str):
    """Full arc page header: title + objection banner."""
    st.markdown(
        f'<h1 style="margin-bottom:4px; font-family:Outfit,sans-serif; '
        f'font-size:1.8rem; letter-spacing:-0.03em;">{title}</h1>'
        f'<p style="color:#94A3B8; font-size:13px; margin-bottom:20px;">{subtitle}</p>',
        unsafe_allow_html=True,
    )
    objection_banner(objection, reality)


def objection_banner(objection: str, reality: str):
    """Two-row banner: what they say (red) vs what data shows (green)."""
    st.markdown(f"""
<div style="margin-bottom:20px;">
  <div style="
    padding:14px 18px;
    background:rgba(248,113,113,0.06);
    border-left:4px solid #F87171;
    border-radius:8px 8px 0 0;
    font-size:15px;
  ">
    <span style="color:#F87171; font-size:11px; font-weight:700;
      text-transform:uppercase; letter-spacing:0.06em;">What they say</span><br>
    <span style="color:#94A3B8; font-style:italic; font-size:16px;">{objection}</span>
  </div>
  <div style="
    padding:14px 18px;
    background:rgba(52,211,153,0.06);
    border-left:4px solid #34D399;
    border-radius:0 0 8px 8px;
    font-size:15px;
  ">
    <span style="color:#34D399; font-size:11px; font-weight:700;
      text-transform:uppercase; letter-spacing:0.06em;">What the data shows</span><br>
    <span style="color:#E2E8F0; font-weight:600; font-size:16px;">{reality}</span>
  </div>
</div>
""", unsafe_allow_html=True)


def headline_insight(label: str, value: str, subtext: str, severity: str = 'warning'):
    """Single hero metric that breaks the objection. Full-width, large."""
    color_map = {
        'danger': '#F87171', 'warning': '#FBBF24',
        'success': '#34D399', 'info': '#60A5FA',
    }
    color = color_map.get(severity, '#FBBF24')
    glow = f'rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15)'
    st.markdown(f"""
<div style="
  text-align:center; padding:28px 20px; margin:8px 0 20px 0;
  background:linear-gradient(135deg, {glow}, rgba(11,17,32,0.5));
  border:1px solid {color}33;
  border-radius:16px;
">
  <div style="color:#94A3B8; font-size:12px; text-transform:uppercase;
    letter-spacing:0.08em; margin-bottom:6px;">{label}</div>
  <div style="font-family:Outfit,sans-serif; font-size:48px; font-weight:700;
    color:{color}; line-height:1.1;">{value}</div>
  <div style="color:#94A3B8; font-size:14px; margin-top:6px;">{subtext}</div>
</div>
""", unsafe_allow_html=True)


def quick_take(findings: list[dict]):
    """Compressed top-of-page action items (High priority only)."""
    high = [f for f in findings if f.get('priority') == 'High']
    if not high:
        return
    items_html = ''
    for f in high[:4]:
        items_html += (
            f'<div style="padding:8px 12px; margin-bottom:4px; '
            f'border-radius:6px; background:rgba(248,113,113,0.06); '
            f'border-left:3px solid #F87171; font-size:13px;">'
            f'<span style="color:#E2E8F0; font-weight:600;">{f["category"]}</span>'
            f'<span style="color:#94A3B8;"> -- </span>'
            f'<span style="color:#94A3B8;">{f["finding"]}</span></div>'
        )
    st.markdown(
        f'<div style="margin-bottom:16px;">'
        f'<div style="color:#F87171; font-size:11px; font-weight:700; '
        f'text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">'
        f'Quick Take</div>{items_html}</div>',
        unsafe_allow_html=True,
    )


def cross_reference(text: str, target_arc: str):
    """Styled callout linking to a related story arc."""
    st.markdown(f"""
<div style="
  padding:14px 18px; margin:16px 0;
  background:rgba(96,165,250,0.06);
  border:1px solid rgba(96,165,250,0.15);
  border-radius:10px;
  display:flex; align-items:center; gap:12px;
">
  <div style="color:#60A5FA; font-size:20px;">&#8594;</div>
  <div>
    <span style="color:#94A3B8; font-size:13px;">{text}</span><br>
    <span style="color:#60A5FA; font-weight:600; font-size:13px;">
      See: {target_arc}</span>
  </div>
</div>
""", unsafe_allow_html=True)


def impact_box(items: list[dict]):
    """2-column grid of dollar-impact cards."""
    cols = st.columns(min(len(items), 3))
    for col, item in zip(cols * ((len(items) // len(cols)) + 1), items):
        color = item.get('color', '#6EE7B7')
        glow = f'rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.1)'
        col.markdown(f"""
<div style="
  padding:16px; border-radius:12px;
  background:linear-gradient(135deg, {glow}, rgba(11,17,32,0.3));
  border:1px solid {color}22;
  text-align:center; margin-bottom:8px;
">
  <div style="color:{color}; font-family:Outfit,sans-serif;
    font-size:28px; font-weight:700;">{item['value']}</div>
  <div style="color:#94A3B8; font-size:12px; margin-top:4px;">{item['label']}</div>
  <div style="color:#475569; font-size:11px;">{item.get('timeframe', '')}</div>
</div>
""", unsafe_allow_html=True)
