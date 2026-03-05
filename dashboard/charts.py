"""Reusable chart builders -- dark executive theme."""

import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import pandas as pd
from config import GEN_COLORS

# -- Global Plotly template for dark mode --
_FONT = 'DM Sans, Outfit, system-ui, sans-serif'
_BG = 'rgba(0,0,0,0)'
_GRID = 'rgba(148,163,184,0.08)'
_TEXT = '#CBD5E1'

pio.templates['txn_dark'] = go.layout.Template(
    layout=go.Layout(
        font=dict(family=_FONT, color=_TEXT, size=13),
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        title=dict(font=dict(size=15, color='#E2E8F0'), x=0, xanchor='left'),
        xaxis=dict(
            gridcolor=_GRID, zerolinecolor=_GRID,
            tickfont=dict(size=11, color='#94A3B8'),
        ),
        yaxis=dict(
            gridcolor=_GRID, zerolinecolor=_GRID,
            tickfont=dict(size=11, color='#94A3B8'),
        ),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02,
            font=dict(size=11, color='#94A3B8'),
            bgcolor='rgba(0,0,0,0)',
        ),
        margin=dict(l=50, r=20, t=40, b=40),
        colorway=[
            '#6EE7B7', '#60A5FA', '#FBBF24', '#F87171',
            '#A78BFA', '#38BDF8', '#FB923C', '#2DD4BF',
            '#818CF8', '#34D399',
        ],
    )
)
pio.templates.default = 'txn_dark'


def bar_chart(labels, values, title='', color=None, horizontal=False,
              text_fmt=None, height=380, show_values=True):
    if color is None:
        color = GEN_COLORS['primary']
    texts = None
    if text_fmt:
        texts = [text_fmt(v) for v in values]
    elif show_values:
        texts = [f'{v:,.0f}' if isinstance(v, (int, float, np.integer, np.floating)) else str(v) for v in values]

    if horizontal:
        fig = go.Figure(data=[go.Bar(
            y=labels, x=values, orientation='h',
            marker_color=color, text=texts,
            textposition='outside', textfont=dict(size=12, color='#CBD5E1'),
        )])
    else:
        fig = go.Figure(data=[go.Bar(
            x=labels, y=values,
            marker_color=color, text=texts,
            textposition='outside', textfont=dict(size=12, color='#CBD5E1'),
            marker=dict(
                color=color,
                line=dict(width=0),
            ),
        )])
    fig.update_layout(title=title, height=height)
    if horizontal:
        fig.update_layout(margin=dict(l=120))
    return fig


def donut_chart(labels, values, colors=None, title='', height=350):
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.6,
        marker_colors=colors,
        textinfo='label+percent', textfont_size=12,
        textfont_color='#CBD5E1',
    )])
    fig.update_layout(title=title, height=height, showlegend=False,
                      margin=dict(l=20, r=20, t=40, b=20))
    return fig


def trend_line(x, y, title='', y_title='', color=None, height=350, fill=False):
    if color is None:
        color = GEN_COLORS['primary']
    fig = go.Figure()
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines+markers',
        line=dict(color=color, width=2.5), marker=dict(size=5),
        fill='tozeroy' if fill else None,
        fillcolor=f'rgba({r},{g},{b},0.08)' if fill else None,
    ))
    fig.update_layout(title=title, height=height,
                      yaxis=dict(title=y_title))
    return fig


def dual_axis_bar_line(x, bar_y, line_y, bar_name='', line_name='',
                       bar_color=None, line_color=None, height=400):
    if bar_color is None:
        bar_color = 'rgba(110,231,183,0.5)'
    if line_color is None:
        line_color = '#F87171'
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=bar_y, name=bar_name, marker_color=bar_color))
    fig.add_trace(go.Scatter(
        x=x, y=line_y, yaxis='y2', mode='lines+markers', name=line_name,
        line=dict(color=line_color, width=2.5), marker=dict(size=5),
    ))
    fig.update_layout(
        height=height,
        yaxis=dict(title=bar_name),
        yaxis2=dict(title=line_name, overlaying='y', side='right',
                    gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#94A3B8')),
    )
    return fig


def grouped_bar(categories, groups: dict, title='', height=380):
    colors = ['#6EE7B7', '#F87171', '#60A5FA', '#FBBF24', '#A78BFA']
    fig = go.Figure()
    for i, (name, vals) in enumerate(groups.items()):
        fig.add_trace(go.Bar(
            x=categories, y=vals, name=name,
            marker_color=colors[i % len(colors)],
        ))
    fig.update_layout(barmode='group', title=title, height=height)
    return fig


def stacked_bar(categories, groups: dict, title='', height=380):
    colors = ['#34D399', '#FBBF24', '#F87171', '#60A5FA', '#64748B']
    fig = go.Figure()
    for i, (name, vals) in enumerate(groups.items()):
        fig.add_trace(go.Bar(
            x=categories, y=vals, name=name,
            marker_color=colors[i % len(colors)],
        ))
    fig.update_layout(barmode='stack', title=title, height=height)
    return fig


def heatmap(z, x_labels, y_labels, title='', height=400, colorscale=None, text_fmt=None):
    if colorscale is None:
        colorscale = [[0, '#0B1120'], [0.25, '#1E3A5F'], [0.5, '#2563EB'],
                      [0.75, '#38BDF8'], [1, '#6EE7B7']]
    if text_fmt:
        z_text = [[text_fmt(v) for v in row] for row in z]
    else:
        z_text = [[f'{v:.1f}' for v in row] for row in z]
    fig = go.Figure(data=go.Heatmap(
        z=z, x=x_labels, y=y_labels,
        colorscale=colorscale, text=z_text,
        texttemplate='%{text}', textfont=dict(size=11, color='#E2E8F0'),
        showscale=False,
    ))
    fig.update_layout(title=title, height=height,
                      margin=dict(l=80, r=20, t=40, b=60))
    return fig


def scatter_plot(x, y, color_labels=None, color_map=None, title='',
                 x_title='', y_title='', height=400):
    if color_labels is not None and color_map is not None:
        fig = go.Figure()
        for label in sorted(set(color_labels)):
            mask = np.array(color_labels) == label
            fig.add_trace(go.Scatter(
                x=np.array(x)[mask], y=np.array(y)[mask],
                mode='markers', name=label,
                marker=dict(size=6, color=color_map.get(label, GEN_COLORS['muted']), opacity=0.7),
            ))
    else:
        fig = go.Figure(data=go.Scatter(
            x=x, y=y, mode='markers',
            marker=dict(size=6, color=GEN_COLORS['primary'], opacity=0.7),
        ))
    fig.update_layout(title=title, height=height,
                      xaxis=dict(title=x_title), yaxis=dict(title=y_title))
    return fig


def waterfall(labels, values, title='', height=400):
    measures = ['absolute'] + ['relative'] * (len(values) - 2) + ['total']
    fig = go.Figure(data=go.Waterfall(
        x=labels, y=values, measure=measures,
        increasing=dict(marker_color='#34D399'),
        decreasing=dict(marker_color='#F87171'),
        totals=dict(marker_color='#60A5FA'),
        connector=dict(line=dict(color='#334155', width=1)),
        textposition='outside', textfont=dict(size=12, color='#CBD5E1'),
    ))
    fig.update_layout(title=title, height=height)
    return fig


def bubble_chart(x, y, size, labels, title='', x_title='', y_title='', height=420):
    fig = go.Figure(data=go.Scatter(
        x=x, y=y, mode='markers+text',
        marker=dict(size=np.array(size) / max(size) * 60, color='#60A5FA',
                    opacity=0.5, line=dict(width=1, color='rgba(96,165,250,0.3)')),
        text=labels, textposition='top center', textfont=dict(size=10, color='#94A3B8'),
    ))
    fig.update_layout(title=title, height=height,
                      xaxis=dict(title=x_title), yaxis=dict(title=y_title))
    return fig


def funnel_horizontal(labels, values, colors, title='', height=140):
    fig = go.Figure()
    for label, val, col in zip(labels, values, colors):
        fig.add_trace(go.Bar(
            y=['Portfolio'], x=[val], name=label, orientation='h',
            marker_color=col, text=f'{label}: {val:,}',
            textposition='inside', textfont=dict(size=12, color='white'),
        ))
    fig.update_layout(
        barmode='stack', title=title, height=height,
        margin=dict(l=60, r=20, t=40 if title else 10, b=10),
        showlegend=True, xaxis=dict(showticklabels=False),
    )
    return fig


def action_summary(findings: list[dict], st_ref):
    for f in findings:
        color = {'High': '#F87171', 'Medium': '#FBBF24', 'Low': '#34D399'}.get(f['priority'], '#64748B')
        bg = {'High': 'rgba(248,113,113,0.12)', 'Medium': 'rgba(251,191,36,0.12)',
              'Low': 'rgba(52,211,153,0.12)'}.get(f['priority'], 'rgba(100,116,139,0.12)')
        st_ref.markdown(
            f'<div style="padding:10px 14px; margin-bottom:6px; border-radius:8px; '
            f'background:{bg}; border-left:3px solid {color};">'
            f'<span style="color:{color}; font-size:11px; font-weight:700; '
            f'text-transform:uppercase; letter-spacing:0.5px;">{f["priority"]}</span>'
            f'&nbsp;&nbsp;<span style="color:#E2E8F0; font-weight:600;">{f["category"]}</span>'
            f'<br><span style="color:#94A3B8; font-size:13px;">{f["finding"]}</span></div>',
            unsafe_allow_html=True,
        )


def sankey_flow(labels, sources, targets, values, title='', height=400):
    """Sankey diagram for attrition cascade flows."""
    colors = ['#34D399', '#FBBF24', '#FB923C', '#F87171', '#60A5FA',
              '#A78BFA', '#6EE7B7', '#38BDF8']
    node_colors = [colors[i % len(colors)] for i in range(len(labels))]
    link_colors = [f'rgba({int(colors[s % len(colors)][1:3], 16)},'
                   f'{int(colors[s % len(colors)][3:5], 16)},'
                   f'{int(colors[s % len(colors)][5:7], 16)},0.3)'
                   for s in sources]
    fig = go.Figure(data=go.Sankey(
        node=dict(pad=20, thickness=24, line=dict(color='#1E293B', width=1),
                  label=labels, color=node_colors),
        link=dict(source=sources, target=targets, value=values, color=link_colors),
    ))
    fig.update_layout(title=title, height=height)
    return fig


def comparison_metric(categories, your_values, benchmark_values, title='',
                      your_label='You', bench_label='Industry', height=350):
    """Side-by-side bar comparing 'you' vs 'benchmark'."""
    fig = go.Figure()
    fig.add_trace(go.Bar(x=categories, y=your_values, name=your_label,
                         marker_color='#6EE7B7'))
    fig.add_trace(go.Bar(x=categories, y=benchmark_values, name=bench_label,
                         marker_color='#64748B'))
    fig.update_layout(barmode='group', title=title, height=height)
    return fig


def risk_gauge(value, title='Portfolio Health Score', height=280):
    """Gauge/speedometer chart for portfolio health."""
    if value >= 70:
        color = '#34D399'
    elif value >= 50:
        color = '#FBBF24'
    else:
        color = '#F87171'
    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=value,
        title=dict(text=title, font=dict(size=14, color='#94A3B8')),
        number=dict(font=dict(size=42, color=color, family='Outfit, sans-serif')),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1, tickcolor='#334155',
                      tickfont=dict(color='#64748B')),
            bar=dict(color=color, thickness=0.7),
            bgcolor='#1E293B',
            borderwidth=0,
            steps=[
                dict(range=[0, 40], color='rgba(248,113,113,0.08)'),
                dict(range=[40, 70], color='rgba(251,191,36,0.08)'),
                dict(range=[70, 100], color='rgba(52,211,153,0.08)'),
            ],
            threshold=dict(line=dict(color=color, width=3), thickness=0.8, value=value),
        ),
    ))
    fig.update_layout(height=height, margin=dict(l=30, r=30, t=40, b=10))
    return fig


def fmt_dollar(x):
    if abs(x) >= 1_000_000:
        return f'${x / 1_000_000:.1f}M'
    if abs(x) >= 1_000:
        return f'${x / 1_000:.0f}K'
    return f'${x:,.0f}'


def fmt_count(x):
    if x >= 1_000_000:
        return f'{x / 1_000_000:.1f}M'
    if x >= 1_000:
        return f'{x / 1_000:.0f}K'
    return f'{int(x):,}'
