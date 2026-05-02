import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
#  APP CONFIGURATION & GLOBAL THEME
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RetailOps | Logistics Intelligence",
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="expanded",
)

PLOTLY_THEME = "plotly_dark"
ACCENT   = "#00FFB2"   # neon mint
ACCENT2  = "#FF4C60"   # coral red
ACCENT3  = "#A78BFA"   # violet
BG_DARK  = "#0D1117"
CARD_BG  = "#161B22"

# ─── Custom CSS ───────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Space Grotesk', sans-serif;
    background-color: {BG_DARK};
    color: #E6EDF3;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: {CARD_BG} !important;
    border-right: 1px solid #30363D;
}}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stFileUploader label {{
    color: {ACCENT} !important;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}

/* ── Header banner ── */
.hero-banner {{
    background: linear-gradient(135deg, #0d1117 0%, #1a2332 50%, #0d1117 100%);
    border: 1px solid #30363D;
    border-left: 4px solid {ACCENT};
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}}
.hero-banner::before {{
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 80% 50%, rgba(0,255,178,0.06) 0%, transparent 60%);
    pointer-events: none;
}}
.hero-title {{
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, {ACCENT}, #7FFFD4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 6px;
}}
.hero-sub {{
    color: #8B949E;
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}}

/* ── KPI Cards ── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
}}
.kpi-card {{
    background: {CARD_BG};
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 18px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color .2s;
}}
.kpi-card:hover {{ border-color: {ACCENT}; }}
.kpi-card::after {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, {ACCENT}, {ACCENT3});
}}
.kpi-label {{
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8B949E;
    margin-bottom: 8px;
}}
.kpi-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.65rem;
    font-weight: 700;
    color: {ACCENT};
    line-height: 1;
}}
.kpi-delta {{
    font-size: 0.75rem;
    margin-top: 6px;
    color: #3FB950;
}}
.kpi-delta.neg {{ color: {ACCENT2}; }}

/* ── Section headers ── */
.section-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 36px 0 18px;
    padding-bottom: 10px;
    border-bottom: 1px solid #30363D;
}}
.section-icon {{
    width: 36px; height: 36px;
    background: linear-gradient(135deg, {ACCENT}22, {ACCENT}44);
    border: 1px solid {ACCENT}44;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}}
.section-title {{
    font-size: 1.15rem;
    font-weight: 600;
    color: #E6EDF3;
    letter-spacing: -0.01em;
    margin: 0;
}}
.section-badge {{
    margin-left: auto;
    background: {ACCENT}22;
    border: 1px solid {ACCENT}44;
    color: {ACCENT};
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
}}

/* ── Chart containers ── */
.chart-card {{
    background: {CARD_BG};
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 16px;
    height: 100%;
}}
.chart-title {{
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #8B949E;
    margin-bottom: 10px;
}}

/* ── Sidebar section titles ── */
.sb-section {{
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {ACCENT};
    padding: 12px 0 4px;
    border-top: 1px solid #30363D;
    margin-top: 6px;
}}

/* ── Expander ── */
details summary {{
    color: {ACCENT} !important;
    font-size: 0.82rem;
    font-weight: 600;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {CARD_BG};
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #30363D;
}}
.stTabs [data-baseweb="tab"] {{
    color: #8B949E;
    font-size: 0.82rem;
    font-weight: 600;
    border-radius: 6px;
}}
.stTabs [aria-selected="true"] {{
    background: {ACCENT}22 !important;
    color: {ACCENT} !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {BG_DARK}; }}
::-webkit-scrollbar-thumb {{ background: #30363D; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {ACCENT}66; }}

/* ── Buttons ── */
.stDownloadButton > button {{
    background: {ACCENT}22 !important;
    border: 1px solid {ACCENT}66 !important;
    color: {ACCENT} !important;
    font-size: 0.8rem;
    font-weight: 600;
    border-radius: 6px;
}}
.stDownloadButton > button:hover {{
    background: {ACCENT}44 !important;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <p class="hero-title">📦 RetailOps Intelligence</p>
  <p class="hero-sub">
    Upload any Retail / Logistics CSV → map your columns → get 16 interactive charts, 
    KPI cards, geospatial maps, correlation matrices &amp; export tools — instantly.
  </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def section(icon, title, badge=None):
    badge_html = f'<span class="section-badge">{badge}</span>' if badge else ''
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">{icon}</div>
        <p class="section-title">{title}</p>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

def chart_card(label, fig, height=380):
    st.markdown(f'<div class="chart-title">{label}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "displaylogo": False})

def fmt_num(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:.0f}"

def apply_dark_layout(fig, title=""):
    fig.update_layout(
        template=PLOTLY_THEME,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", size=11, color="#8B949E"),
        margin=dict(l=20, r=20, t=40 if title else 20, b=20),
        title=dict(text=title, font=dict(size=13, color="#E6EDF3"), pad=dict(b=10)) if title else None,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#30363D", borderwidth=1, font_size=10),
        xaxis=dict(gridcolor="#1C2128", zerolinecolor="#30363D"),
        yaxis=dict(gridcolor="#1C2128", zerolinecolor="#30363D"),
    )
    return fig

PALETTE = [ACCENT, ACCENT2, ACCENT3, "#FBBF24", "#38BDF8", "#FB923C",
           "#34D399", "#F472B6", "#60A5FA", "#A3E635"]

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:12px 0 6px;">
        <span style="font-size:2rem;">📦</span>
        <p style="color:#00FFB2;font-weight:700;font-size:1rem;margin:4px 0 0;letter-spacing:-0.01em;">RetailOps</p>
        <p style="color:#8B949E;font-size:0.72rem;margin:0;">Logistics Intelligence v2.0</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">📁 Data Upload</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

    if uploaded_file:
        st.markdown('<div class="sb-section">🗂️ Column Mapping</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN LOGIC
# ─────────────────────────────────────────────
if uploaded_file is None:
    # ── Landing placeholder ──
    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1, "📈", "16 Chart Types", "Time-series, proportions, stats & geospatial in one click"),
        (c2, "🗺️", "Live Maps",      "Circle, cluster, heatmap & severity choropleth maps"),
        (c3, "⚡", "Zero-Config",    "Smart column detection, KPI cards & CSV export built-in"),
    ]:
        col.markdown(f"""
        <div class="kpi-card" style="text-align:center;padding:28px 20px;">
            <div style="font-size:2rem;margin-bottom:10px;">{icon}</div>
            <div style="font-size:0.95rem;font-weight:600;color:#E6EDF3;margin-bottom:6px;">{title}</div>
            <div style="font-size:0.8rem;color:#8B949E;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.info("👈  Upload a CSV file in the sidebar to begin.")
    st.stop()

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
df = pd.read_csv(uploaded_file)
all_cols = df.columns.tolist()

with st.sidebar:
    st.selectbox("", ["──────────────────────"], key="_div1", label_visibility="collapsed")

    date_col   = st.selectbox("📅 Date Column",              ["None"] + all_cols)
    metric_col = st.selectbox("📊 Primary Metric",           ["None"] + all_cols)
    cat_col    = st.selectbox("🏷️  Primary Category",        ["None"] + all_cols)
    subcat_col = st.selectbox("🔖 Sub-Category (Sunburst)",  ["None"] + all_cols)
    lat_col    = st.selectbox("🌐 Latitude Column",           ["None"] + all_cols)
    lon_col    = st.selectbox("🌐 Longitude Column",          ["None"] + all_cols)
    geo_cat_col = st.selectbox("🗺️  Geo Severity Category",   ["None"] + all_cols)

    st.markdown('<div class="sb-section">🎛️ Filters</div>', unsafe_allow_html=True)

# ─── Preprocessing ────────────────────────────
if date_col != "None":
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])

if metric_col != "None":
    df[metric_col] = pd.to_numeric(df[metric_col], errors='coerce').fillna(0)

# ─── Sidebar filters ──────────────────────────
with st.sidebar:
    if cat_col != "None":
        cats = df[cat_col].dropna().unique().tolist()
        sel_cats = st.multiselect("Filter by Category", cats, default=cats[:min(len(cats), 8)])
        if sel_cats:
            df = df[df[cat_col].isin(sel_cats)]

    if date_col != "None":
        try:
            min_d = df[date_col].dropna().min().date()
            max_d = df[date_col].dropna().max().date()
            if min_d and max_d:
                date_range = st.date_input(
                    "Date Range",
                    value=(min_d, max_d),
                    min_value=min_d,
                    max_value=max_d
                )
                if len(date_range) == 2:
                    df = df[
                        (df[date_col].dt.date >= date_range[0]) &
                        (df[date_col].dt.date <= date_range[1])
                    ]
            else:
                st.warning("⚠️ No valid dates found in selected column.")
        except Exception as e:
            st.warning(f"⚠️ Could not parse date range: {e}")

    st.markdown('<div class="sb-section">📥 Export</div>', unsafe_allow_html=True)
    st.download_button(
        "⬇️ Download Filtered CSV",
        data=df.to_csv(index=False).encode(),
        file_name="filtered_data.csv",
        mime="text/csv",
    )

# ─────────────────────────────────────────────
#  DATA PREVIEW + KPIs
# ─────────────────────────────────────────────
with st.expander("🔍  Raw Data Preview  (first 20 rows)", expanded=False):
    st.dataframe(df.head(20), use_container_width=True)

# ── KPI Cards ─────────────────────────────────
if metric_col != "None":
    total    = df[metric_col].sum()
    mean_val = df[metric_col].mean()
    mx       = df[metric_col].max()
    mn       = df[metric_col].min()
    n_rows   = len(df)
    n_cats   = df[cat_col].nunique() if cat_col != "None" else "—"

    kpis = [
        ("Total", fmt_num(total),    "▲ Sum of all records",     False),
        ("Mean",  fmt_num(mean_val), "Average per record",       False),
        ("Max",   fmt_num(mx),       "Highest single value",     False),
        ("Min",   fmt_num(mn),       "Lowest single value",      True),
        ("Rows",  fmt_num(n_rows),   "After filters applied",    False),
        ("Categories", str(n_cats),  "Unique category values",   False),
    ]
    cols_kpi = st.columns(len(kpis))
    for col, (label, val, delta, neg) in zip(cols_kpi, kpis):
        neg_cls = "neg" if neg else ""
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-delta {neg_cls}">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Time-Series",
    "🥧  Proportions",
    "📊  Statistics",
    "🗺️  Geospatial",
])

# ══════════════════════════════════════════════
#  TAB 1 — TIME SERIES
# ══════════════════════════════════════════════
with tab1:
    if date_col == "None" or metric_col == "None":
        st.warning("Please map a **Date** and **Metric** column.")
    else:
        section("📈", "Time-Series Trends", "4 CHARTS")

        df["_date"] = df[date_col].dt.date
        group_cols = ["_date", cat_col] if cat_col != "None" else ["_date"]
        df_time = df.groupby(group_cols, as_index=False)[metric_col].sum()
        df_time.rename(columns={"_date": "Date"}, inplace=True)

        # ── Row 1: Line + Area ─────────────────
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📉 Basic Line Chart — Rolling Trends</div>', unsafe_allow_html=True)
            kw = dict(x="Date", y=metric_col, template=PLOTLY_THEME)
            if cat_col != "None": kw["color"] = cat_col
            fig = px.line(df_time, **kw, color_discrete_sequence=PALETTE)
            apply_dark_layout(fig)
            fig.update_traces(line_width=2)
            st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📐 Filled Area Chart — Stacked Cumulative</div>', unsafe_allow_html=True)
            kw2 = dict(x="Date", y=metric_col, template=PLOTLY_THEME)
            if cat_col != "None": kw2["color"] = cat_col
            fig2 = px.area(df_time, **kw2, color_discrete_sequence=PALETTE)
            apply_dark_layout(fig2)
            st.plotly_chart(fig2, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Row 2: Advanced line + subplot ─────
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🔎 Advanced Line + Range Selector</div>', unsafe_allow_html=True)
            fig3 = go.Figure()
            if cat_col != "None":
                for i, cat in enumerate(df_time[cat_col].unique()[:8]):
                    d = df_time[df_time[cat_col] == cat]
                    fig3.add_trace(go.Scatter(
                        x=d["Date"], y=d[metric_col], mode="lines", name=str(cat),
                        line=dict(color=PALETTE[i % len(PALETTE)], width=2),
                        hovertemplate=f"<b>{cat}</b><br>Date: %{{x}}<br>{metric_col}: %{{y:,.0f}}<extra></extra>"
                    ))
            else:
                fig3.add_trace(go.Scatter(x=df_time["Date"], y=df_time[metric_col],
                                           mode="lines", line=dict(color=ACCENT, width=2)))
            fig3.update_layout(
                template=PLOTLY_THEME,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Space Grotesk", size=11, color="#8B949E"),
                margin=dict(l=20, r=20, t=20, b=80),
                legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#30363D", borderwidth=1),
                xaxis=dict(
                    gridcolor="#1C2128",
                    rangeselector=dict(
                        bgcolor=CARD_BG, bordercolor="#30363D", borderwidth=1,
                        font=dict(color="#E6EDF3", size=10),
                        buttons=[
                            dict(count=7,  label="1W", step="day",   stepmode="backward"),
                            dict(count=1,  label="1M", step="month", stepmode="backward"),
                            dict(count=3,  label="3M", step="month", stepmode="backward"),
                            dict(count=6,  label="6M", step="month", stepmode="backward"),
                            dict(count=1,  label="YTD", step="year", stepmode="todate"),
                            dict(step="all", label="ALL"),
                        ]
                    ),
                    rangeslider=dict(visible=True, bgcolor="#1C2128", bordercolor="#30363D"),
                ),
                yaxis=dict(gridcolor="#1C2128"),
            )
            st.plotly_chart(fig3, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📊 Side-by-Side Bar Subplots (Top 6 Cats)</div>', unsafe_allow_html=True)
            if cat_col != "None":
                top_cats = (df.groupby(cat_col)[metric_col].sum()
                              .nlargest(6).index.tolist())
                df_sub = df_time[df_time[cat_col].isin(top_cats)]
                fig4 = make_subplots(rows=2, cols=3, subplot_titles=[str(c) for c in top_cats],
                                     vertical_spacing=0.15, horizontal_spacing=0.08)
                for idx, cat in enumerate(top_cats):
                    r, c = divmod(idx, 3)
                    d = df_sub[df_sub[cat_col] == cat]
                    fig4.add_trace(
                        go.Bar(x=d["Date"], y=d[metric_col], name=str(cat),
                               marker_color=PALETTE[idx % len(PALETTE)],
                               showlegend=False),
                        row=r+1, col=c+1
                    )
                fig4.update_layout(
                    template=PLOTLY_THEME,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Space Grotesk", size=9, color="#8B949E"),
                    margin=dict(l=10, r=10, t=30, b=10),
                    height=360,
                )
                for ann in fig4.layout.annotations:
                    ann.font.size = 10
                    ann.font.color = "#8B949E"
                st.plotly_chart(fig4, use_container_width=True, config={"displaylogo": False})
            else:
                st.info("Select a Category column to enable this chart.")
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 2 — PROPORTIONS
# ══════════════════════════════════════════════
with tab2:
    if metric_col == "None" or cat_col == "None":
        st.warning("Please map **Metric** and **Category** columns.")
    else:
        section("🥧", "Proportions & Hierarchy", "4 CHARTS")

        df_prop = (df.groupby(cat_col)[metric_col].sum()
                     .reset_index().nlargest(12, metric_col))

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🍕 Basic Pie Chart</div>', unsafe_allow_html=True)
            fig_p = px.pie(df_prop, names=cat_col, values=metric_col,
                           color_discrete_sequence=PALETTE,
                           hole=0, template=PLOTLY_THEME)
            fig_p.update_traces(textposition="inside", textinfo="percent+label",
                                 textfont_size=10, textfont_color="#0D1117",
                                 marker=dict(line=dict(color="#0D1117", width=2)))
            apply_dark_layout(fig_p)
            st.plotly_chart(fig_p, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🍩 Donut Chart</div>', unsafe_allow_html=True)
            fig_d = px.pie(df_prop, names=cat_col, values=metric_col,
                           color_discrete_sequence=PALETTE,
                           hole=0.52, template=PLOTLY_THEME)
            fig_d.update_traces(textposition="outside", textinfo="percent+label",
                                  textfont_size=10,
                                  marker=dict(line=dict(color="#0D1117", width=2)))
            fig_d.add_annotation(
                text=f"<b>{fmt_num(df_prop[metric_col].sum())}</b><br><span style='font-size:9px;'>TOTAL</span>",
                x=0.5, y=0.5, font_size=16, font_color=ACCENT, showarrow=False
            )
            apply_dark_layout(fig_d)
            st.plotly_chart(fig_d, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Treemap + Sunburst ─────────────────
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🌳 Treemap — Proportional Blocks</div>', unsafe_allow_html=True)
            path_cols = [cat_col]
            if subcat_col != "None": path_cols.append(subcat_col)
            df_tree = df.groupby(path_cols)[metric_col].sum().reset_index()
            fig_t = px.treemap(df_tree, path=path_cols, values=metric_col,
                                color=metric_col, color_continuous_scale=["#0D1117", ACCENT],
                                template=PLOTLY_THEME)
            fig_t.update_traces(textinfo="label+value+percent root",
                                  textfont_size=11,
                                  marker=dict(line=dict(color="#0D1117", width=2)))
            apply_dark_layout(fig_t)
            st.plotly_chart(fig_t, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            if subcat_col != "None":
                st.markdown('<div class="chart-title">☀️ Sunburst — Hierarchical Drilldown</div>', unsafe_allow_html=True)
                df_sun = df.groupby([cat_col, subcat_col])[metric_col].sum().reset_index()
                fig_s = px.sunburst(df_sun, path=[cat_col, subcat_col], values=metric_col,
                                     color=metric_col, color_continuous_scale=["#1a2332", ACCENT],
                                     template=PLOTLY_THEME)
                fig_s.update_traces(textfont_size=10,
                                     marker=dict(line=dict(color="#0D1117", width=1.5)))
                apply_dark_layout(fig_s)
                st.plotly_chart(fig_s, use_container_width=True, config={"displaylogo": False})
            else:
                st.markdown('<div class="chart-title">☀️ Sunburst Chart</div>', unsafe_allow_html=True)
                st.info("Select a **Sub-Category** column to enable the Sunburst chart.")
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 3 — STATISTICS
# ══════════════════════════════════════════════
with tab3:
    if metric_col == "None" or cat_col == "None":
        st.warning("Please map **Metric** and **Category** columns.")
    else:
        section("📊", "Statistical Distributions", "4 CHARTS")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📦 Interactive Box Plot — Outlier Detection</div>', unsafe_allow_html=True)
            fig_b = px.box(df, x=cat_col, y=metric_col, color=cat_col, points="outliers",
                            color_discrete_sequence=PALETTE, template=PLOTLY_THEME)
            fig_b.update_traces(marker_size=4, line_width=1.5)
            apply_dark_layout(fig_b)
            st.plotly_chart(fig_b, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🎻 Interactive Violin Plot — Density</div>', unsafe_allow_html=True)
            fig_v = px.violin(df, x=cat_col, y=metric_col, color=cat_col, box=True,
                               color_discrete_sequence=PALETTE, template=PLOTLY_THEME,
                               points="all")
            fig_v.update_traces(marker_size=2, spanmode="soft")
            apply_dark_layout(fig_v)
            st.plotly_chart(fig_v, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Pivot + Correlation ────────────────
        c3, c4 = st.columns(2)

        with c3:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            if date_col != "None":
                st.markdown('<div class="chart-title">📅 Pivot Heatmap — Category × Month</div>', unsafe_allow_html=True)
                df["_month"] = df[date_col].dt.to_period("M").astype(str)
                pivot = df.pivot_table(index=cat_col, columns="_month",
                                       values=metric_col, aggfunc="sum", fill_value=0)
                # Limit to last 18 months
                pivot = pivot.iloc[:, -18:]
                fig_ph = px.imshow(pivot, aspect="auto",
                                    color_continuous_scale=["#0D1117", ACCENT3, ACCENT],
                                    template=PLOTLY_THEME)
                fig_ph.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Space Grotesk", size=9, color="#8B949E"),
                    margin=dict(l=10, r=10, t=10, b=10),
                    coloraxis_colorbar=dict(tickfont_color="#8B949E"),
                )
                st.plotly_chart(fig_ph, use_container_width=True, config={"displaylogo": False})
            else:
                st.markdown('<div class="chart-title">📅 Pivot Heatmap</div>', unsafe_allow_html=True)
                st.info("Map a **Date** column to enable the Pivot Heatmap.")
            st.markdown('</div>', unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🔗 Masked Correlation Heatmap</div>', unsafe_allow_html=True)
            num_df = df.select_dtypes(include=[np.number])
            if len(num_df.columns) > 1:
                corr  = num_df.corr()
                mask  = np.triu(np.ones_like(corr, dtype=bool))
                corr_masked = corr.mask(mask)
                fig_c = px.imshow(corr_masked, text_auto=".2f",
                                   color_continuous_scale="RdBu_r",
                                   zmin=-1, zmax=1,
                                   template=PLOTLY_THEME, aspect="auto")
                fig_c.update_traces(textfont_size=9)
                fig_c.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Space Grotesk", size=9, color="#8B949E"),
                    margin=dict(l=10, r=10, t=10, b=10),
                    coloraxis_colorbar=dict(tickfont_color="#8B949E"),
                )
                st.plotly_chart(fig_c, use_container_width=True, config={"displaylogo": False})
            else:
                st.info("Not enough numeric columns for a correlation heatmap.")
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Distribution histogram ─────────────
        section("📉", "Distribution & Histogram", "BONUS")
        c5, c6 = st.columns(2)
        with c5:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📊 Histogram — Value Distribution</div>', unsafe_allow_html=True)
            kw_h = dict(x=metric_col, template=PLOTLY_THEME, nbins=40,
                         color_discrete_sequence=[ACCENT])
            if cat_col != "None": kw_h["color"] = cat_col; kw_h["color_discrete_sequence"] = PALETTE
            fig_h = px.histogram(df, **kw_h, barmode="overlay", opacity=0.7)
            apply_dark_layout(fig_h)
            st.plotly_chart(fig_h, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with c6:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🧮 ECDF — Cumulative Distribution</div>', unsafe_allow_html=True)
            kw_e = dict(x=metric_col, template=PLOTLY_THEME, color_discrete_sequence=[ACCENT3])
            if cat_col != "None": kw_e["color"] = cat_col; kw_e["color_discrete_sequence"] = PALETTE
            fig_e = px.ecdf(df, **kw_e)
            apply_dark_layout(fig_e)
            st.plotly_chart(fig_e, use_container_width=True, config={"displaylogo": False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Descriptive stats table ────────────
        section("🔢", "Descriptive Statistics Summary", "TABLE")
        desc = df.select_dtypes(include=[np.number]).describe().T.round(2)
        st.dataframe(
            desc.style
                .background_gradient(cmap="YlOrRd", subset=["mean", "std", "max"])
                .format("{:.2f}"),
            use_container_width=True
        )

# ══════════════════════════════════════════════
#  TAB 4 — GEOSPATIAL
# ══════════════════════════════════════════════
with tab4:
    if lat_col == "None" or lon_col == "None":
        st.warning("Please map **Latitude** and **Longitude** columns.")
    else:
        section("🗺️", "Geospatial Analytics", "4 MAP TYPES")

        df_map = df.dropna(subset=[lat_col, lon_col])
        if metric_col != "None":
            df_map = df_map.dropna(subset=[metric_col])
        df_map[lat_col] = pd.to_numeric(df_map[lat_col], errors='coerce')
        df_map[lon_col] = pd.to_numeric(df_map[lon_col], errors='coerce')
        df_map = df_map.dropna(subset=[lat_col, lon_col])

        center_lat = df_map[lat_col].mean()
        center_lon = df_map[lon_col].mean()
        TILES = "CartoDB dark_matter"

        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📍 Basic Marker Map</div>', unsafe_allow_html=True)
            basic_map = folium.Map(location=[center_lat, center_lon], zoom_start=4, tiles=TILES)
            for _, row in df_map.head(400).iterrows():
                tip = str(row[metric_col]) if metric_col != "None" else ""
                folium.Marker(
                    location=[row[lat_col], row[lon_col]],
                    tooltip=tip,
                    icon=folium.Icon(color="green", icon="circle", prefix="fa"),
                ).add_to(basic_map)
            st_folium(basic_map, height=380, width=None, returned_objects=[])
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🔵 Proportional Circle Map</div>', unsafe_allow_html=True)
            circle_map = folium.Map(location=[center_lat, center_lon], zoom_start=4, tiles=TILES)
            if metric_col != "None":
                max_val = df_map[metric_col].max() or 1
                for _, row in df_map.head(500).iterrows():
                    folium.CircleMarker(
                        location=[row[lat_col], row[lon_col]],
                        radius=max(3, (row[metric_col] / max_val) * 22),
                        color=ACCENT2, fill=True, fill_color=ACCENT, fill_opacity=0.55,
                        tooltip=f"{metric_col}: {row[metric_col]:,.2f}",
                    ).add_to(circle_map)
            st_folium(circle_map, height=380, width=None, returned_objects=[])
            st.markdown('</div>', unsafe_allow_html=True)

        c3, c4 = st.columns(2)

        with c3:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🔗 Marker Cluster Map</div>', unsafe_allow_html=True)
            cluster_map = folium.Map(location=[center_lat, center_lon], zoom_start=4, tiles=TILES)
            mc = MarkerCluster()
            for _, row in df_map.head(800).iterrows():
                tip = f"{metric_col}: {row[metric_col]:,.2f}" if metric_col != "None" else ""
                folium.Marker(
                    location=[row[lat_col], row[lon_col]],
                    tooltip=tip,
                ).add_to(mc)
            mc.add_to(cluster_map)
            st_folium(cluster_map, height=380, width=None, returned_objects=[])
            st.markdown('</div>', unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🌡️ Density Heatmap</div>', unsafe_allow_html=True)
            heat_map = folium.Map(location=[center_lat, center_lon], zoom_start=4, tiles=TILES)
            if metric_col != "None":
                heat_data = [[row[lat_col], row[lon_col], row[metric_col]]
                             for _, row in df_map.head(1000).iterrows()]
            else:
                heat_data = [[row[lat_col], row[lon_col]]
                             for _, row in df_map.head(1000).iterrows()]
            HeatMap(heat_data, radius=18, blur=14, max_zoom=1,
                    gradient={"0.2": "#0D1117", "0.5": ACCENT3, "1.0": ACCENT2}).add_to(heat_map)
            st_folium(heat_map, height=380, width=None, returned_objects=[])
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Severity / Choropleth-style scatter ─
        section("⚠️", "Choropleth-Style Severity Map", "SCATTER GEO")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🌍 Severity Scatter-Geo Map (Plotly)</div>', unsafe_allow_html=True)
        df_scatter = df_map.copy().head(2000)
        kw_geo = dict(
            lat=lat_col, lon=lon_col,
            color=metric_col if metric_col != "None" else lat_col,
            color_continuous_scale=[[0, "#0D1117"], [0.3, ACCENT3], [0.7, "#FBBF24"], [1.0, ACCENT2]],
            size=metric_col if metric_col != "None" else None,
            size_max=18,
            template=PLOTLY_THEME,
            mapbox_style="carto-darkmatter",
            zoom=3,
        )
        if geo_cat_col != "None":
            kw_geo["hover_name"] = geo_cat_col
        fig_geo = px.scatter_mapbox(df_scatter, **kw_geo, opacity=0.75)
        fig_geo.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Space Grotesk", size=10, color="#8B949E"),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            coloraxis_colorbar=dict(
                title=metric_col if metric_col != "None" else "",
                tickfont_color="#8B949E",
                title_font_color="#8B949E",
            ),
        )
        st.plotly_chart(fig_geo, use_container_width=True, config={"displaylogo": False})
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:16px 0;color:#8B949E;font-size:0.75rem;">
    <span style="color:#00FFB2;font-weight:700;">RetailOps Intelligence</span> &nbsp;·&nbsp;
    Built with Streamlit + Plotly + Folium &nbsp;·&nbsp;
    16 interactive charts across 4 analysis domains
</div>
""", unsafe_allow_html=True)