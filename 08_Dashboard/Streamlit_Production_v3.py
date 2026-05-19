import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="MBT‑Biosecurity‑Engine – Investor Scenario Explorer",
    layout="wide"
)

# -----------------------------
# LANGUAGE PACK
# -----------------------------
LANG = {
    "EN": {
        "app_title": "MBT‑Biosecurity‑Engine – Investor Scenario Explorer",
        "app_desc": "Interactive model to compare Baseline (No MBT55) vs With MBT55 across 12 biosecurity KPIs, PBPE Value, ROI, and PBPE Credits.",
        "lang_label": "Language",
        "sidebar_title": "Scenario Controls",
        "crop": "Crop Type",
        "region": "Region",
        "climate": "Climate Scenario",
        "mbt55_level": "MBT55 Application Level",
        "disease_pressure": "Disease Pressure",
        "soil_carbon": "Soil Carbon Baseline (tC/ha)",
        "post_harvest": "Post-Harvest Loss (%)",
        "market_vol": "Market Volatility (0–1)",
        "area": "Area (ha)",
        "input_cost": "Input Cost (USD/ha)",
        "baseline": "Baseline",
        "with_mbt": "With MBT55",
        "pbpe_value": "PBPE Value (USD)",
        "roi": "ROI (%)",
        "ghg": "GHG Reduction (tCO₂e)",
        "delta_c": "ΔC (tC)",
        "kpi_title": "12 PBPE Biosecurity KPIs",
        "credit_title": "PBPE Credits",
        "yield_title": "Total Yield (t)",
        "revenue_title": "Revenue (USD)",
        "cost_title": "Total Cost (USD)",
        "raw_tables": "Show Raw Tables",
        "kpi_table": "KPI Table",
        "credit_table": "Credit Table",
        "mbt_section_title": "What is MBT55?",
        "mbt_section_body": (
            "MBT55 is a microbiome-based biosecurity intervention that improves plant health, "
            "reduces disease losses, enhances quality, and increases soil carbon and GHG reductions. "
            "This model shows how MBT55 changes yield, losses, costs, and PBPE Value under different scenarios."
        ),
        "formula_title": "PBPE Value – Transparent Calculation",
        "formula_desc": "The following formulas are used to compute PBPE Value and ROI:",
        "formula_rev": "Revenue = Total Yield (t) × Price (USD/t)",
        "formula_cost": "Cost = Input Cost (USD/ha) × Area (ha)",
        "formula_pbpe": "PBPE Value = Revenue – Cost",
        "formula_roi": "ROI = (PBPE Value – Baseline Cost) / Baseline Cost",
        "credits_expl_title": "PBPE Credits – Definitions",
        "credits_expl": {
            "Biosecurity Credits": "Value of reduced disease losses and improved biosecurity.",
            "Carbon Credits (tCO₂)": "Value of ΔC and GHG reductions converted to carbon-equivalent units.",
            "Food Loss Credits (t)": "Value of reduced post-harvest and spoilage losses.",
            "Quality Credits Score": "Value of quality premium (price uplift) from MBT55.",
            "Price Stability Credits Score": "Value of reduced market volatility and improved price stability."
        },
        "csv_title": "Download Scenario Data (CSV)",
        "csv_kpi": "Download KPI Table",
        "csv_credits": "Download Credits Table",
        "csv_summary": "Download Summary Table",
    },
    "JP": {
        "app_title": "MBT‑Biosecurity‑Engine – 投資家向けシナリオ体験モデル",
        "app_desc": "MBT55 なし（Baseline）と MBT55 あり（With MBT55）を比較し、12 指標・PBPE 価値・ROI・PBPE クレジットを可視化します。",
        "lang_label": "言語",
        "sidebar_title": "シナリオ設定",
        "crop": "作物",
        "region": "地域",
        "climate": "気候シナリオ",
        "mbt55_level": "MBT55 投与レベル",
        "disease_pressure": "病害圧",
        "soil_carbon": "土壌炭素量（tC/ha）",
        "post_harvest": "収穫後損失（%）",
        "market_vol": "市場ボラティリティ（0–1）",
        "area": "面積（ha）",
        "input_cost": "投入コスト（USD/ha）",
        "baseline": "MBT55 なし",
        "with_mbt": "MBT55 あり",
        "pbpe_value": "PBPE 価値（USD）",
        "roi": "投資利益率（%）",
        "ghg": "GHG 削減量（tCO₂e）",
        "delta_c": "ΔC（tC）",
        "kpi_title": "12 PBPE バイオセキュリティ指標",
        "credit_title": "PBPE クレジット",
        "yield_title": "総収量（t）",
        "revenue_title": "収益（USD）",
        "cost_title": "総コスト（USD）",
        "raw_tables": "詳細テーブルを表示",
        "kpi_table": "KPI テーブル",
        "credit_table": "クレジット テーブル",
        "mbt_section_title": "MBT55 とは？",
        "mbt_section_body": (
            "MBT55 は、作物のマイクロバイオームを改善し、病害損失を減らし、品質を高め、"
            "土壌炭素と温室効果ガス削減を向上させるバイオセキュリティ介入です。"
            "このモデルでは、MBT55 が収量・損失・コスト・PBPE 価値に与える影響をシナリオ別に示します。"
        ),
        "formula_title": "PBPE 価値の計算式（透明化）",
        "formula_desc": "PBPE 価値と ROI は、以下の式で計算されています：",
        "formula_rev": "収益 = 総収量（t） × 価格（USD/t）",
        "formula_cost": "コスト = 投入コスト（USD/ha） × 面積（ha）",
        "formula_pbpe": "PBPE 価値 = 収益 – コスト",
        "formula_roi": "ROI = (PBPE 価値 – ベースラインコスト) / ベースラインコスト",
        "credits_expl_title": "PBPE クレジットの定義",
        "credits_expl": {
            "Biosecurity Credits": "病害損失削減とバイオセキュリティ向上の価値。",
            "Carbon Credits (tCO₂)": "ΔC と GHG 削減を炭素換算した価値。",
            "Food Loss Credits (t)": "収穫後・腐敗損失の削減価値。",
            "Quality Credits Score": "MBT55 による品質プレミアム（価格上昇）の価値。",
            "Price Stability Credits Score": "市場ボラティリティ低減と価格安定性向上の価値。"
        },
        "csv_title": "シナリオデータのダウンロード（CSV）",
        "csv_kpi": "KPI テーブルをダウンロード",
        "csv_credits": "クレジット テーブルをダウンロード",
        "csv_summary": "サマリー テーブルをダウンロード",
    }
}

# -----------------------------
# LANGUAGE SWITCH (TOP RIGHT)
# -----------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"

top_col1, top_col2 = st.columns([8, 2])
with top_col1:
    st.title(LANG[st.session_state["lang"]]["app_title"])
with top_col2:
    lang_choice = st.selectbox(
        LANG[st.session_state["lang"]]["lang_label"],
        ["EN", "JP"],
        index=0 if st.session_state["lang"] == "EN" else 1,
        key="lang_select"
    )
    st.session_state["lang"] = lang_choice

T = LANG[st.session_state["lang"]]

st.markdown(T["app_desc"])

# -----------------------------
# SIMPLE CSS FOR CARD-LIKE UI
# -----------------------------
st.markdown(
    """
    <style>
    .metric-card {
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        background-color: #0e1117;
        border: 1px solid #31333F;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #BBBBBB;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 1.3rem;
        font-weight: 600;
    }
    .metric-delta-pos {
        color: #00C853;
        font-size: 0.9rem;
    }
    .metric-delta-neg {
        color: #FF5252;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# CONSTANTS
# -----------------------------
CROP_OPTIONS = ["Coffee", "Citrus", "Rice", "Wheat", "Maize"]
REGION_OPTIONS = ["LATAM", "Africa", "Asia"]
CLIMATE_OPTIONS = ["Normal", "Drought", "Wet"]
MBT55_LEVELS = ["None", "Low", "Medium", "High"]
DISEASE_LEVELS = ["Low", "Medium", "High"]

CROP_YIELD_BASE = {"Coffee": 1.5, "Citrus": 20.0, "Rice": 5.0, "Wheat": 4.0, "Maize": 6.0}
CROP_PRICE_PER_TON = {"Coffee": 3500, "Citrus": 300, "Rice": 400, "Wheat": 300, "Maize": 250}
REGION_RISK_MULTIPLIER = {"LATAM": 1.0, "Africa": 1.1, "Asia": 0.95}
CLIMATE_YIELD_FACTOR = {"Normal": 1.0, "Drought": 0.8, "Wet": 0.9}
MBT55_YIELD_GAIN = {"None": 0.00, "Low": 0.05, "Medium": 0.10, "High": 0.15}
MBT55_DISEASE_REDUCTION = {"None": 0.00, "Low": 0.30, "Medium": 0.50, "High": 0.70}
DISEASE_LOSS_BASE = {"Low": 0.05, "Medium": 0.15, "High": 0.30}
MBT55_QUALITY_PREMIUM = {"None": 0.00, "Low": 0.02, "Medium": 0.05, "High": 0.08}
MBT55_SPOILAGE_REDUCTION = {"None": 0.00, "Low": 0.10, "Medium": 0.25, "High": 0.40}
MBT55_COST_REDUCTION = {"None": 0.00, "Low": 0.05, "Medium": 0.10, "High": 0.15}
MBT55_DELTA_C_TC = {"None": 0.0, "Low": 0.3, "Medium": 0.6, "High": 1.0}
MBT55_GHG_REDUCTION_TCO2E = {"None": 0.0, "Low": 0.5, "Medium": 1.0, "High": 1.5}
MBT55_PRICE_STABILITY = {"None": 0.0, "Low": 0.1, "Medium": 0.25, "High": 0.4}

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.title(T["sidebar_title"])

crop = st.sidebar.selectbox(T["crop"], CROP_OPTIONS)
region = st.sidebar.selectbox(T["region"], REGION_OPTIONS)
climate = st.sidebar.selectbox(T["climate"], CLIMATE_OPTIONS)
mbt55_level = st.sidebar.selectbox(T["mbt55_level"], MBT55_LEVELS, index=2)
disease_pressure = st.sidebar.selectbox(T["disease_pressure"], DISEASE_LEVELS, index=1)

soil_carbon_baseline = st.sidebar.slider(T["soil_carbon"], 10.0, 80.0, 40.0, 1.0)
post_harvest_loss_baseline = st.sidebar.slider(T["post_harvest"], 5, 40, 20, 1)
market_volatility = st.sidebar.slider(T["market_vol"], 0.0, 1.0, 0.4, 0.05)
area_ha = st.sidebar.slider(T["area"], 10, 1000, 100, 10)
input_cost_baseline = st.sidebar.slider(T["input_cost"], 200, 1500, 600, 50)

# -----------------------------
# MBT55 EXPLANATION SECTION
# -----------------------------
st.markdown(f"### {T['mbt_section_title']}")
st.markdown(T["mbt_section_body"])
st.markdown("---")

# -----------------------------
# CALCULATION FUNCTION
# -----------------------------
def compute_scenario(mbt55_level: str):
    base_yield = CROP_YIELD_BASE[crop]
    climate_factor = CLIMATE_YIELD_FACTOR[climate]
    region_factor = REGION_RISK_MULTIPLIER[region]

    base_disease_loss = DISEASE_LOSS_BASE[disease_pressure]
    disease_reduction = MBT55_DISEASE_REDUCTION[mbt55_level]
    effective_disease_loss = base_disease_loss * (1 - disease_reduction)

    mbt55_yield_gain = MBT55_YIELD_GAIN[mbt55_level]
    yield_factor = climate_factor * region_factor * (1 - effective_disease_loss) * (1 + mbt55_yield_gain)
    yield_t_per_ha = base_yield * yield_factor
    total_yield_t = yield_t_per_ha * area_ha

    price_per_ton = CROP_PRICE_PER_TON[crop]
    quality_premium = MBT55_QUALITY_PREMIUM[mbt55_level]
    effective_price = price_per_ton * (1 + quality_premium)
    revenue_usd = total_yield_t * effective_price

    spoilage_reduction = MBT55_SPOILAGE_REDUCTION[mbt55_level]
    effective_ph_loss = post_harvest_loss_baseline * (1 - spoilage_reduction)
    food_loss_reduction_t = (post_harvest_loss_baseline - effective_ph_loss) / 100 * total_yield_t

    cost_reduction = MBT55_COST_REDUCTION[mbt55_level]
    effective_cost_per_ha = input_cost_baseline * (1 - cost_reduction)
    total_cost_usd = effective_cost_per_ha * area_ha

    pbpe_value_usd = revenue_usd - total_cost_usd

    delta_c_tc = MBT55_DELTA_C_TC[mbt55_level] * area_ha
    ghg_reduction_tco2e = MBT55_GHG_REDUCTION_TCO2E[mbt55_level] * area_ha

    price_stability_index = max(0.0, min(1.0, MBT55_PRICE_STABILITY[mbt55_level] + (1 - market_volatility)))

    biosecurity_credits = disease_reduction * area_ha
    carbon_credits_tco2 = ghg_reduction_tco2e
    food_loss_credits_t = food_loss_reduction_t
    quality_credits_score = quality_premium * 100
    price_stability_credits_score = price_stability_index * 100

    baseline_cost_total = input_cost_baseline * area_ha
    roi_pct = (pbpe_value_usd - baseline_cost_total) / baseline_cost_total * 100 if baseline_cost_total > 0 else 0

    kpis = {
        "Disease Loss Reduction (%)": disease_reduction * 100,
        "Yield Gain (%)": mbt55_yield_gain * 100,
        "Quality Premium Score": quality_credits_score,
        "Anti-Spoilage (%)": spoilage_reduction * 100,
        "Food Loss Reduction (t)": food_loss_reduction_t,
        "Cost Reduction (USD)": (input_cost_baseline - effective_cost_per_ha) * area_ha,
        "Livestock Biosecurity Score": 0.0,
        "ΔC (tC)": delta_c_tc,
        "GHG Reduction (tCO₂e)": ghg_reduction_tco2e,
        "Price Stability Index": price_stability_index,
        "PBPE Biosecurity Value (USD)": pbpe_value_usd,
        "Biosecurity ROI (%)": roi_pct,
    }

    credits = {
        "Biosecurity Credits": biosecurity_credits,
        "Carbon Credits (tCO₂)": carbon_credits_tco2,
        "Food Loss Credits (t)": food_loss_credits_t,
        "Quality Credits Score": quality_credits_score,
        "Price Stability Credits Score": price_stability_credits_score,
    }

    summary = {
        "Total Yield (t)": total_yield_t,
        "Revenue (USD)": revenue_usd,
        "Total Cost (USD)": total_cost_usd,
        "PBPE Value (USD)": pbpe_value_usd,
        "ROI (%)": roi_pct,
        "ΔC (tC)": delta_c_tc,
        "GHG Reduction (tCO₂e)": ghg_reduction_tco2e,
        "Price Stability Index": price_stability_index,
        "Baseline Cost (USD)": baseline_cost_total,
    }

    return kpis, credits, summary

# -----------------------------
# SCENARIOS
# -----------------------------
kpis_base, credits_base, summary_base = compute_scenario("None")
kpis_mbt, credits_mbt, summary_mbt = compute_scenario(mbt55_level)

# -----------------------------
# TOP CARDS – PBPE VALUE / ROI / CREDITS
# -----------------------------
card_col1, card_col2, card_col3 = st.columns(3)

with card_col1:
    delta_pbpe = summary_mbt["PBPE Value (USD)"] - summary_base["PBPE Value (USD)"]
    delta_class = "metric-delta-pos" if delta_pbpe >= 0 else "metric-delta-neg"
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-title">{T["pbpe_value"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="metric-value">{summary_mbt["PBPE Value (USD)"]:,.0f}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="{delta_class}">Δ {delta_pbpe:,.0f}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with card_col2:
    delta_roi = summary_mbt["ROI (%)"] - summary_base["ROI (%)"]
    delta_class = "metric-delta-pos" if delta_roi >= 0 else "metric-delta-neg"
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-title">{T["roi"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="metric-value">{summary_mbt["ROI (%)"]:.1f}%</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="{delta_class}">Δ {delta_roi:.1f} pp</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with card_col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-title">{T["ghg"]} / {T["delta_c"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="metric-value">{summary_mbt["GHG Reduction (tCO₂e)"]:,.1f} tCO₂e</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="metric-delta-pos">ΔC {summary_mbt["ΔC (tC)"]:,.1f} tC</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# KPI & CREDIT CHARTS (CATEGORY COLORING)
# -----------------------------
kpi_category = {
    "Disease Loss Reduction (%)": "Biosecurity",
    "Yield Gain (%)": "Yield",
    "Quality Premium Score": "Quality",
    "Anti-Spoilage (%)": "Food Loss",
    "Food Loss Reduction (t)": "Food Loss",
    "Cost Reduction (USD)": "Cost",
    "Livestock Biosecurity Score": "Biosecurity",
    "ΔC (tC)": "Carbon",
    "GHG Reduction (tCO₂e)": "Carbon",
    "Price Stability Index": "Stability",
    "PBPE Biosecurity Value (USD)": "Value",
    "Biosecurity ROI (%)": "Value",
}

kpi_names = list(kpis_base.keys())
df_kpi = pd.DataFrame({
    "KPI": kpi_names,
    T["baseline"]: [kpis_base[k] for k in kpi_names],
    T["with_mbt"]: [kpis_mbt[k] for k in kpi_names],
    "Category": [kpi_category.get(k, "Other") for k in kpi_names],
})

df_kpi_melt = df_kpi.melt(
    id_vars=["KPI", "Category"],
    var_name="Scenario",
    value_name="Value"
)

kpi_col1, kpi_col2 = st.columns(2)

with kpi_col1:
    st.subheader(T["kpi_title"])
    fig_kpi = px.bar(
        df_kpi_melt,
        x="KPI",
        y="Value",
        color="Category",
        pattern_shape="Scenario",
        barmode="group",
        height=500,
    )
    fig_kpi.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_kpi, use_container_width=True)

with kpi_col2:
    st.subheader(T["credit_title"])
    credit_names = list(credits_base.keys())
    df_credits = pd.DataFrame({
        "Credit": credit_names,
        T["baseline"]: [credits_base[c] for c in credit_names],
        T["with_mbt"]: [credits_mbt[c] for c in credit_names],
    })
    df_credits_melt = df_credits.melt(
        id_vars="Credit",
        var_name="Scenario",
        value_name="Value"
    )
    fig_credits = px.bar(
        df_credits_melt,
        x="Credit",
        y="Value",
        color="Scenario",
        barmode="group",
        height=500,
    )
    fig_credits.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig_credits, use_container_width=True)

st.markdown("---")

# -----------------------------
# YIELD / REVENUE / COST – BEFORE/AFTER
# -----------------------------
col_y1, col_y2, col_y3 = st.columns(3)

with col_y1:
    st.subheader(T["yield_title"])
    st.metric(T["baseline"], f"{summary_base['Total Yield (t)']:,.1f}")
    st.metric(
        T["with_mbt"],
        f"{summary_mbt['Total Yield (t)']:,.1f}",
        f"{summary_mbt['Total Yield (t)'] - summary_base['Total Yield (t)']:,.1f}",
    )

with col_y2:
    st.subheader(T["revenue_title"])
    st.metric(T["baseline"], f"{summary_base['Revenue (USD)']:,.0f}")
    st.metric(
        T["with_mbt"],
        f"{summary_mbt['Revenue (USD)']:,.0f}",
        f"{summary_mbt['Revenue (USD)'] - summary_base['Revenue (USD)']:,.0f}",
    )

with col_y3:
    st.subheader(T["cost_title"])
    st.metric(T["baseline"], f"{summary_base['Total Cost (USD)']:,.0f}")
    st.metric(
        T["with_mbt"],
        f"{summary_mbt['Total Cost (USD)']:,.0f}",
        f"{summary_mbt['Total Cost (USD)'] - summary_base['Total Cost (USD)']:,.0f}",
    )

st.markdown("---")

# -----------------------------
# FORMULA TRANSPARENCY
# -----------------------------
with st.expander(T["formula_title"], expanded=False):
    st.markdown(T["formula_desc"])
    st.markdown(f"- {T['formula_rev']}")
    st.markdown(f"- {T['formula_cost']}")
    st.markdown(f"- {T['formula_pbpe']}")
    st.markdown(f"- {T['formula_roi']}")

    st.markdown("**Baseline vs With MBT55 (Current Scenario):**")
    formula_df = pd.DataFrame({
        "Scenario": [T["baseline"], T["with_mbt"]],
        "Total Yield (t)": [summary_base["Total Yield (t)"], summary_mbt["Total Yield (t)"]],
        "Price (USD/t)": [CROP_PRICE_PER_TON[crop]] * 2,
        "Revenue (USD)": [summary_base["Revenue (USD)"], summary_mbt["Revenue (USD)"]],
        "Cost (USD)": [summary_base["Total Cost (USD)"], summary_mbt["Total Cost (USD)"]],
        "PBPE Value (USD)": [summary_base["PBPE Value (USD)"], summary_mbt["PBPE Value (USD)"]],
        "ROI (%)": [summary_base["ROI (%)"], summary_mbt["ROI (%)"]],
    })

    # 🔧 ここを修正：数値列だけフォーマットする
    numeric_cols = [
        "Total Yield (t)",
        "Price (USD/t)",
        "Revenue (USD)",
        "Cost (USD)",
        "PBPE Value (USD)",
        "ROI (%)",
    ]
    st.dataframe(
        formula_df.style.format(
            {col: "{:,.2f}" for col in numeric_cols}
        )
    )

st.markdown("---")

# -----------------------------
# CREDITS EXPLANATION
# -----------------------------
st.markdown(f"### {T['credits_expl_title']}")
for k, v in T["credits_expl"].items():
    st.markdown(f"- **{k}**: {v}")

st.markdown("---")

# -----------------------------
# CSV EXPORT
# -----------------------------
st.markdown(f"### {T['csv_title']}")

summary_df = pd.DataFrame(
    {
        "Metric": list(summary_mbt.keys()),
        "Value": list(summary_mbt.values()),
    }
)

csv_col1, csv_col2, csv_col3 = st.columns(3)

with csv_col1:
    csv_kpi = df_kpi.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=T["csv_kpi"],
        data=csv_kpi,
        file_name="pbpe_kpi_table.csv",
        mime="text/csv",
    )

with csv_col2:
    csv_credits = df_credits.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=T["csv_credits"],
        data=csv_credits,
        file_name="pbpe_credits_table.csv",
        mime="text/csv",
    )

with csv_col3:
    csv_summary = summary_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=T["csv_summary"],
        data=csv_summary,
        file_name="pbpe_summary_table.csv",
        mime="text/csv",
    )
