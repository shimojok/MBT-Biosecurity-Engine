import streamlit as st
import pandas as pd
import numpy as np

# ---------- Helper KPI functions ----------

def disease_loss_reduction(before_pct, after_pct):
    if before_pct == 0:
        return 0.0
    return (before_pct - after_pct) / before_pct

def yield_gain(before, after):
    if before == 0:
        return 0.0
    return (after - before) / before

def anti_spoilage(before_pct, after_pct):
    if before_pct == 0:
        return 0.0
    return (before_pct - after_pct) / before_pct

def delta_c(soc_before, soc_after):
    return soc_after - soc_before

def ghg_reduction(ch4_before, ch4_after, n2o_before, n2o_after, gwp_ch4=28, gwp_n2o=265):
    d_ch4 = ch4_before - ch4_after
    d_n2o = n2o_before - n2o_after
    return d_ch4 * gwp_ch4 / 1000.0 + d_n2o * gwp_n2o / 1000.0  # kg→tCO2e

def pbpe_value(loss_reduction_usd, cost_reduction_usd, yield_gain_usd,
               quality_premium_usd, food_loss_reduction_usd, climate_credits_usd):
    return (loss_reduction_usd + cost_reduction_usd + yield_gain_usd +
            quality_premium_usd + food_loss_reduction_usd + climate_credits_usd)

def roi(pbpe_value_usd, mbt_cost_usd):
    if mbt_cost_usd == 0:
        return 0.0
    return (pbpe_value_usd - mbt_cost_usd) / mbt_cost_usd

def price_stability_index(sigma_before, sigma_after):
    if sigma_before == 0:
        return 0.0
    return 1.0 - (sigma_after / sigma_before)

# ---------- Dummy data generator (to be replaced by real DB/API) ----------

def load_dummy_data():
    farms = ["Farm-A", "Farm-B", "Farm-C"]
    seasons = [2022, 2023, 2024]
    data = []
    for f in farms:
        for s in seasons:
            row = {
                "farm_id": f,
                "season": s,
                "yield_before": np.random.uniform(0.8, 1.2),
                "yield_after": np.random.uniform(1.1, 1.6),
                "disease_before": np.random.uniform(0.2, 0.4),
                "disease_after": np.random.uniform(0.05, 0.15),
                "spoilage_before": np.random.uniform(0.3, 0.5),
                "spoilage_after": np.random.uniform(0.05, 0.15),
                "soc_before": np.random.uniform(20, 30),
                "soc_after": np.random.uniform(21, 32),
                "ch4_before": np.random.uniform(500, 800),
                "ch4_after": np.random.uniform(300, 600),
                "n2o_before": np.random.uniform(50, 80),
                "n2o_after": np.random.uniform(30, 60),
                "base_price": np.random.uniform(3.0, 4.0),
                "pbpe_price": np.random.uniform(3.5, 5.0),
                "price_sigma_before": np.random.uniform(0.4, 0.8),
                "price_sigma_after": np.random.uniform(0.1, 0.4),
                "mbt_cost": np.random.uniform(80, 150)
            }
            data.append(row)
    return pd.DataFrame(data)

# ---------- Streamlit App ----------

st.set_page_config(page_title="MBT-Biosecurity-Engine Dashboard", layout="wide")

st.title("MBT-Biosecurity-Engine Dashboard")
st.caption("Planetary Biosecurity × Regenerative Agriculture × PBPE Climate Architecture")

df = load_dummy_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_farm = st.sidebar.selectbox("Farm", ["All"] + sorted(df["farm_id"].unique().tolist()))
selected_season = st.sidebar.selectbox("Season", ["All"] + sorted(df["season"].unique().tolist()))

filtered = df.copy()
if selected_farm != "All":
    filtered = filtered[filtered["farm_id"] == selected_farm]
if selected_season != "All":
    filtered = filtered[filtered["season"] == selected_season]

# Aggregate
agg = filtered.mean(numeric_only=True)

# KPI calculations
disease_idx = disease_loss_reduction(agg["disease_before"], agg["disease_after"])
yield_idx = yield_gain(agg["yield_before"], agg["yield_after"])
spoilage_idx = anti_spoilage(agg["spoilage_before"], agg["spoilage_after"])
delta_c_val = delta_c(agg["soc_before"], agg["soc_after"])
ghg_red = ghg_reduction(
    agg["ch4_before"], agg["ch4_after"],
    agg["n2o_before"], agg["n2o_after"]
)
pbpe_val = pbpe_value(
    loss_reduction_usd=1000 * disease_idx,
    cost_reduction_usd=500 * spoilage_idx,
    yield_gain_usd=2000 * yield_idx,
    quality_premium_usd=800,
    food_loss_reduction_usd=700 * spoilage_idx,
    climate_credits_usd=50 * ghg_red
)
roi_val = roi(pbpe_val, agg["mbt_cost"])
psi = price_stability_index(agg["price_sigma_before"], agg["price_sigma_after"])

# ---------- Layout ----------

tab_overview, tab_crops, tab_soil, tab_econ = st.tabs(
    ["Overview", "Crops & Disease", "Soil & Climate", "PBPE Value & ROI"]
)

with tab_overview:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Disease Loss Reduction", f"{disease_idx*100:.1f} %")
    col2.metric("Yield Gain", f"{yield_idx*100:.1f} %")
    col3.metric("ΔC (Soil Carbon)", f"{delta_c_val:.2f} tC/ha")
    col4.metric("GHG Reduction", f"{ghg_red:.2f} tCO₂e")

    st.subheader("Price & PBPE")
    c1, c2, c3 = st.columns(3)
    c1.metric("Base Price", f"{agg['base_price']:.2f} $/kg")
    c2.metric("PBPE Price", f"{agg['pbpe_price']:.2f} $/kg")
    c3.metric("Price Stability Index", f"{psi*100:.1f} %")

with tab_crops:
    st.subheader("Yield and Disease")
    c1, c2 = st.columns(2)
    c1.bar_chart(filtered[["season", "yield_before", "yield_after"]].set_index("season"))
    c2.bar_chart(filtered[["season", "disease_before", "disease_after"]].set_index("season"))

    st.subheader("Spoilage & Food Loss")
    st.bar_chart(filtered[["season", "spoilage_before", "spoilage_after"]].set_index("season"))

with tab_soil:
    st.subheader("Soil Carbon (SOC)")
    st.line_chart(filtered[["season", "soc_before", "soc_after"]].set_index("season"))

    st.subheader("GHG Emissions (CH₄ & N₂O)")
    ghg_df = pd.DataFrame({
        "season": filtered["season"],
        "CH4_before": filtered["ch4_before"],
        "CH4_after": filtered["ch4_after"],
        "N2O_before": filtered["n2o_before"],
        "N2O_after": filtered["n2o_after"]
    }).set_index("season")
    st.line_chart(ghg_df)

with tab_econ:
    st.subheader("PBPE-Biosecurity Value & ROI")
    c1, c2 = st.columns(2)
    c1.metric("PBPE-Biosecurity Value", f"{pbpe_val:,.0f} USD")
    c2.metric("Biosecurity ROI", f"{roi_val*100:.1f} %")

    st.subheader("Price Volatility")
    vol_df = filtered[["season", "price_sigma_before", "price_sigma_after"]].set_index("season")
    st.line_chart(vol_df)
