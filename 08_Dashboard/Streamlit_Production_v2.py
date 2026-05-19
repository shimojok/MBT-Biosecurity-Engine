import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="MBT‑Biosecurity‑Engine – Investor View",
    layout="wide"
)

# -----------------------------
# LANGUAGE PACK
# -----------------------------
LANG = {
    "EN": {
        "title": "MBT‑Biosecurity‑Engine – Investor Scenario Explorer",
        "desc": "Compare Baseline (No MBT55) vs With MBT55 across 12 KPIs, PBPE Value, ROI, and Credits.",
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
    },
    "JP": {
        "title": "MBT‑Biosecurity‑Engine – 投資家向けシナリオ体験モデル",
        "desc": "MBT55 なし（Baseline）と MBT55 あり（With MBT55）を比較し、12 指標・PBPE価値・ROI・クレジットを表示します。",
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
    }
}

# -----------------------------
# LANGUAGE SWITCH
# -----------------------------
lang_choice = st.sidebar.radio("Language / 言語", ["EN", "JP"], index=0)
T = LANG[lang_choice]

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
    }

    return kpis, credits, summary

# -----------------------------
# SCENARIOS
# -----------------------------
kpis_base, credits_base, summary_base = compute_scenario("None")
kpis_mbt, credits_mbt, summary_mbt = compute_scenario(mbt55_level)

# -----------------------------
# LAYOUT
# -----------------------------
st.title(T["title"])
st.markdown(T["desc"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(f"{T['pbpe_value']} – {T['baseline']}", f"{summary_base['PBPE Value (USD)']:,.0f}")
    st.metric(
        f"{T['pbpe_value']} – {T['with_mbt']}",
        f"{summary_mbt['PBPE Value (USD)']:,.0f}",
        f"{summary_mbt['PBPE Value (USD)'] - summary_base['PBPE Value (USD)']:,.0f}"
    )

with col2:
    st.metric(f"{T['roi']} – {T['baseline']}", f"{summary_base['ROI (%)']:.1f}%")
    st.metric(
        f"{T['roi']} – {T['with_mbt']}",
        f"{summary_mbt['ROI (%)']:.1f}%",
        f"{summary_mbt['ROI (%)'] - summary_base['ROI (%)']:.1f} pp"
    )

with col3:
    st.metric(f"{T['ghg']} – {T['with_mbt']}", f"{summary_mbt['GHG Reduction (tCO₂e)']:,.1f}")
    st.metric(f"{T['delta_c']} – {T['with_mbt']}", f"{summary_mbt['ΔC (tC)']:,.1f}")

st.markdown("---")

# -----------------------------
# KPI & CREDIT CHARTS
# -----------------------------
kpi_names = list(kpis_base.keys())
df_kpi = pd.DataFrame({
    "KPI": kpi_names,
    T["baseline"]: [kpis_base[k] for k in kpi_names],
    T["with_mbt"]: [kpis_mbt[k] for k in kpi_names],
})

df_kpi_melt = df_kpi.melt(id_vars="KPI", var_name="Scenario", value_name="Value")

fig_kpi = px.bar(df_kpi_melt, x="KPI", y="Value", color="Scenario", barmode="group", height=500)
fig_kpi.update_layout(xaxis_tickangle=-45)

st.subheader(T["kpi_title"])
st.plotly_chart(fig_kpi, use_container_width=True)

st.markdown("---")

credit_names = list(credits_base.keys())
df_credits = pd.DataFrame({
    "Credit": credit_names,
    T["baseline"]: [credits_base[c] for c in credit_names],
    T["with_mbt"]: [credits_mbt[c] for c in credit_names],
})

df_credits_melt = df_credits.melt(id_vars="Credit", var_name="Scenario", value_name="Value")

fig_credits = px.bar(df_credits_melt, x="Credit", y="Value", color="Scenario", barmode="group", height=500)
fig_credits.update_layout(xaxis_tickangle=-30)

st.subheader(T["credit_title"])
st.plotly_chart(fig_credits, use_container_width=True)

st.markdown("---")

# -----------------------------
# YIELD / REVENUE / COST
# -----------------------------
col_y1, col_y2, col_y3 = st.columns(3)

with col_y1:
    st.subheader(T["yield_title"])
    st.metric(T["baseline"], f"{summary_base['Total Yield (t)']:,.1f}")
    st.metric(
        T["with_mbt"],
        f"{summary_mbt['Total Yield (t)']:,.1f}",
        f"{summary_mbt['Total Yield (t)'] - summary_base['Total Yield (t)']:,.1f}"
    )

with col_y2:
    st.subheader(T["revenue_title"])
    st.metric(T["baseline"], f"{summary_base['Revenue (USD)']:,.0f}")
    st.metric(
        T["with_mbt"],
        f"{summary_mbt['Revenue (USD)']:,.0f}",
        f"{summary_mbt['Revenue (USD)'] - summary_base['Revenue (USD)']:,.0f}"
    )

with col_y3:
    st.subheader(T["cost_title"])
    st.metric(T["baseline"], f"{summary_base['Total Cost (USD)']:,.0f}")
    st.metric(
        T["with_mbt"],
        f"{summary_mbt['Total Cost (USD)']:,.0f}",
        f"{summary_mbt['Total Cost (USD)'] - summary_base['Total Cost (USD)']:,.0f}"
    )

st.markdown("---")

# -----------------------------
# RAW TABLES
# -----------------------------
if st.checkbox(T["raw_tables"]):
    st.subheader(T["kpi_table"])
    st.dataframe(df_kpi)

    st.subheader(T["credit_table"])
    st.dataframe(df_credits)
