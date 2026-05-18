import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="MBT-Biosecurity-Engine – Investor View",
    layout="wide"
)

# -----------------------------
# 1. CONFIG
# -----------------------------

CROP_OPTIONS = ["Coffee", "Citrus", "Rice", "Wheat", "Maize"]
REGION_OPTIONS = ["LATAM", "Africa", "Asia"]
CLIMATE_OPTIONS = ["Normal", "Drought", "Wet"]
MBT55_LEVELS = ["None", "Low", "Medium", "High"]
DISEASE_LEVELS = ["Low", "Medium", "High"]

# Base coefficients (very simplified, illustrative)
CROP_YIELD_BASE = {
    "Coffee": 1.5,
    "Citrus": 20.0,
    "Rice": 5.0,
    "Wheat": 4.0,
    "Maize": 6.0,
}

CROP_PRICE_PER_TON = {
    "Coffee": 3500,
    "Citrus": 300,
    "Rice": 400,
    "Wheat": 300,
    "Maize": 250,
}

REGION_RISK_MULTIPLIER = {
    "LATAM": 1.0,
    "Africa": 1.1,
    "Asia": 0.95,
}

CLIMATE_YIELD_FACTOR = {
    "Normal": 1.0,
    "Drought": 0.8,
    "Wet": 0.9,
}

MBT55_YIELD_GAIN = {
    "None": 0.00,
    "Low": 0.05,
    "Medium": 0.10,
    "High": 0.15,
}

MBT55_DISEASE_REDUCTION = {
    "None": 0.00,
    "Low": 0.30,
    "Medium": 0.50,
    "High": 0.70,
}

DISEASE_LOSS_BASE = {
    "Low": 0.05,
    "Medium": 0.15,
    "High": 0.30,
}

MBT55_QUALITY_PREMIUM = {
    "None": 0.00,
    "Low": 0.02,
    "Medium": 0.05,
    "High": 0.08,
}

MBT55_SPOILAGE_REDUCTION = {
    "None": 0.00,
    "Low": 0.10,
    "Medium": 0.25,
    "High": 0.40,
}

MBT55_COST_REDUCTION = {
    "None": 0.00,
    "Low": 0.05,
    "Medium": 0.10,
    "High": 0.15,
}

MBT55_DELTA_C_TC = {
    "None": 0.0,
    "Low": 0.3,
    "Medium": 0.6,
    "High": 1.0,
}

MBT55_GHG_REDUCTION_TCO2E = {
    "None": 0.0,
    "Low": 0.5,
    "Medium": 1.0,
    "High": 1.5,
}

MBT55_PRICE_STABILITY = {
    "None": 0.0,
    "Low": 0.1,
    "Medium": 0.25,
    "High": 0.4,
}

# -----------------------------
# 2. SIDEBAR – INVESTOR CONTROLS
# -----------------------------

st.sidebar.title("MBT55 Scenario Controls")

crop = st.sidebar.selectbox("Crop Type", CROP_OPTIONS, index=0)
region = st.sidebar.selectbox("Region", REGION_OPTIONS, index=0)
climate = st.sidebar.selectbox("Climate Scenario", CLIMATE_OPTIONS, index=0)

mbt55_level = st.sidebar.selectbox("MBT55 Application Level", MBT55_LEVELS, index=2)
disease_pressure = st.sidebar.selectbox("Disease Pressure", DISEASE_LEVELS, index=1)

soil_carbon_baseline = st.sidebar.slider(
    "Soil Carbon Baseline (tC/ha)", min_value=10.0, max_value=80.0, value=40.0, step=1.0
)

post_harvest_loss_baseline = st.sidebar.slider(
    "Post-Harvest Loss Baseline (%)", min_value=5, max_value=40, value=20, step=1
)

market_volatility = st.sidebar.slider(
    "Market Volatility (0–1)", min_value=0.0, max_value=1.0, value=0.4, step=0.05
)

area_ha = st.sidebar.slider(
    "Area (ha)", min_value=10, max_value=1000, value=100, step=10
)

input_cost_baseline = st.sidebar.slider(
    "Input Cost Baseline (USD/ha)", min_value=200, max_value=1500, value=600, step=50
)

st.sidebar.markdown("---")
st.sidebar.caption("All outputs are illustrative and for investor scenario exploration only.")

# -----------------------------
# 3. CORE CALCULATION FUNCTIONS
# -----------------------------

def compute_scenario(mbt55_level: str):
    # Base yield
    base_yield = CROP_YIELD_BASE[crop]
    climate_factor = CLIMATE_YIELD_FACTOR[climate]
    region_factor = REGION_RISK_MULTIPLIER[region]

    # Disease loss
    base_disease_loss = DISEASE_LOSS_BASE[disease_pressure]
    disease_reduction = MBT55_DISEASE_REDUCTION[mbt55_level]
    effective_disease_loss = base_disease_loss * (1 - disease_reduction)

    # Yield
    mbt55_yield_gain = MBT55_YIELD_GAIN[mbt55_level]
    yield_factor = climate_factor * region_factor * (1 - effective_disease_loss) * (1 + mbt55_yield_gain)
    yield_t_per_ha = base_yield * yield_factor
    total_yield_t = yield_t_per_ha * area_ha

    # Price & revenue
    price_per_ton = CROP_PRICE_PER_TON[crop]
    quality_premium = MBT55_QUALITY_PREMIUM[mbt55_level]
    effective_price = price_per_ton * (1 + quality_premium)
    revenue_usd = total_yield_t * effective_price

    # Post-harvest loss
    spoilage_reduction = MBT55_SPOILAGE_REDUCTION[mbt55_level]
    effective_ph_loss = post_harvest_loss_baseline * (1 - spoilage_reduction)
    food_loss_reduction_t = (post_harvest_loss_baseline - effective_ph_loss) / 100 * total_yield_t

    # Costs
    cost_reduction = MBT55_COST_REDUCTION[mbt55_level]
    effective_cost_per_ha = input_cost_baseline * (1 - cost_reduction)
    total_cost_usd = effective_cost_per_ha * area_ha

    # PBPE Value (simplified)
    pbpe_value_usd = revenue_usd - total_cost_usd

    # Climate
    delta_c_tc = MBT55_DELTA_C_TC[mbt55_level] * area_ha
    ghg_reduction_tco2e = MBT55_GHG_REDUCTION_TCO2E[mbt55_level] * area_ha

    # Price stability
    price_stability_index = max(0.0, min(1.0, MBT55_PRICE_STABILITY[mbt55_level] + (1 - market_volatility)))

    # Credits (very simplified)
    biosecurity_credits = disease_reduction * area_ha
    carbon_credits_tco2 = ghg_reduction_tco2e
    food_loss_credits_t = food_loss_reduction_t
    quality_credits_score = quality_premium * 100
    price_stability_credits_score = price_stability_index * 100

    # ROI (simplified)
    baseline_cost_total = input_cost_baseline * area_ha
    roi_pct = (pbpe_value_usd - baseline_cost_total) / baseline_cost_total * 100 if baseline_cost_total > 0 else 0

    # 12 KPIs (mapped)
    kpis = {
        "Disease Loss Reduction (%)": disease_reduction * 100,
        "Yield Gain (%)": mbt55_yield_gain * 100,
        "Quality Premium Score": quality_credits_score,
        "Anti-Spoilage (%)": spoilage_reduction * 100,
        "Food Loss Reduction (t)": food_loss_reduction_t,
        "Cost Reduction (USD)": (input_cost_baseline - effective_cost_per_ha) * area_ha,
        "Livestock Biosecurity Score": 0.0,  # placeholder (not modeled here)
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
# 4. SCENARIOS: BASELINE vs MBT55
# -----------------------------

kpis_base, credits_base, summary_base = compute_scenario("None")
kpis_mbt, credits_mbt, summary_mbt = compute_scenario(mbt55_level)

# -----------------------------
# 5. LAYOUT
# -----------------------------

st.title("MBT‑Biosecurity‑Engine – Investor Scenario Explorer")

st.markdown(
    f"""
**Crop:** {crop}  **Region:** {region}  **Climate:** {climate}  **Area:** {area_ha} ha  

This dashboard compares a **Baseline (No MBT55)** scenario with a **With MBT55 ({mbt55_level})** scenario  
across the **12 PBPE Biosecurity KPIs**, PBPE Value, and PBPE Credits.
"""
)

col_top1, col_top2, col_top3 = st.columns(3)

with col_top1:
    st.metric(
        "PBPE Value (USD) – Baseline",
        f"{summary_base['PBPE Value (USD)']:,.0f}"
    )
    st.metric(
        "PBPE Value (USD) – With MBT55",
        f"{summary_mbt['PBPE Value (USD)']:,.0f}",
        f"{summary_mbt['PBPE Value (USD)'] - summary_base['PBPE Value (USD)']:,.0f}"
    )

with col_top2:
    st.metric(
        "ROI (%) – Baseline",
        f"{summary_base['ROI (%)']:.1f}%"
    )
    st.metric(
        "ROI (%) – With MBT55",
        f"{summary_mbt['ROI (%)']:.1f}%",
        f"{summary_mbt['ROI (%)'] - summary_base['ROI (%)']:.1f} pp"
    )

with col_top3:
    st.metric(
        "GHG Reduction (tCO₂e) – With MBT55",
        f"{summary_mbt['GHG Reduction (tCO₂e)']:,.1f}"
    )
    st.metric(
        "ΔC (tC) – With MBT55",
        f"{summary_mbt['ΔC (tC)']:,.1f}"
    )

st.markdown("---")

# -----------------------------
# 6. 12 KPIs – RADAR / BAR
# -----------------------------

kpi_names = list(kpis_base.keys())
df_kpi = pd.DataFrame({
    "KPI": kpi_names,
    "Baseline": [kpis_base[k] for k in kpi_names],
    "With MBT55": [kpis_mbt[k] for k in kpi_names],
})

col_kpi1, col_kpi2 = st.columns(2)

with col_kpi1:
    st.subheader("12 PBPE Biosecurity KPIs – Comparison")
    df_kpi_melt = df_kpi.melt(id_vars="KPI", var_name="Scenario", value_name="Value")
    fig_bar = px.bar(
        df_kpi_melt,
        x="KPI",
        y="Value",
        color="Scenario",
        barmode="group",
        height=500
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_kpi2:
    st.subheader("PBPE Credits – Baseline vs With MBT55")
    credit_names = list(credits_base.keys())
    df_credits = pd.DataFrame({
        "Credit": credit_names,
        "Baseline": [credits_base[c] for c in credit_names],
        "With MBT55": [credits_mbt[c] for c in credit_names],
    })
    df_credits_melt = df_credits.melt(id_vars="Credit", var_name="Scenario", value_name="Value")
    fig_credits = px.bar(
        df_credits_melt,
        x="Credit",
        y="Value",
        color="Scenario",
        barmode="group",
        height=500
    )
    fig_credits.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig_credits, use_container_width=True)

st.markdown("---")

# -----------------------------
# 7. YIELD / REVENUE / COST – BEFORE / AFTER
# -----------------------------

col_y1, col_y2, col_y3 = st.columns(3)

with col_y1:
    st.subheader("Total Yield (t)")
    st.metric(
        "Baseline",
        f"{summary_base['Total Yield (t)']:,.1f}"
    )
    st.metric(
        "With MBT55",
        f"{summary_mbt['Total Yield (t)']:,.1f}",
        f"{summary_mbt['Total Yield (t)'] - summary_base['Total Yield (t)']:,.1f}"
    )

with col_y2:
    st.subheader("Revenue (USD)")
    st.metric(
        "Baseline",
        f"{summary_base['Revenue (USD)']:,.0f}"
    )
    st.metric(
        "With MBT55",
        f"{summary_mbt['Revenue (USD)']:,.0f}",
        f"{summary_mbt['Revenue (USD)'] - summary_base['Revenue (USD)']:,.0f}"
    )

with col_y3:
    st.subheader("Total Cost (USD)")
    st.metric(
        "Baseline",
        f"{summary_base['Total Cost (USD)']:,.0f}"
    )
    st.metric(
        "With MBT55",
        f"{summary_mbt['Total Cost (USD)']:,.0f}",
        f"{summary_mbt['Total Cost (USD)'] - summary_base['Total Cost (USD)']:,.0f}"
    )

st.markdown("---")

# -----------------------------
# 8. RAW TABLES (OPTIONAL FOR INVESTORS)
# -----------------------------

with st.expander("Show raw KPI and credit tables"):
    st.write("**12 PBPE Biosecurity KPIs**")
    st.dataframe(df_kpi.set_index("KPI"))

    st.write("**PBPE Credits**")
    st.dataframe(df_credits.set_index("Credit"))

st.caption("MBT‑Biosecurity‑Engine – Investor Scenario Explorer (Prototype v2)")
