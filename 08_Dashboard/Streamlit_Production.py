import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# 1. KPI FUNCTIONS (12 指標)
# ============================================================

def disease_loss_reduction(before, after):
    return (before - after) / before if before else 0

def yield_gain(before, after):
    return (after - before) / before if before else 0

def quality_premium(brix_b, brix_a, poly_b, poly_a, defect_b, defect_a):
    return (0.4*(brix_a-brix_b) + 0.4*(poly_a-poly_b) - 0.2*(defect_a-defect_b))

def anti_spoilage(before, after):
    return (before - after) / before if before else 0

def food_loss_reduction(m_before, m_after):
    return m_after - m_before

def cost_reduction(f_b, f_a, p_b, p_a, a_b, a_a, w_b, w_a):
    return (f_b-f_a) + (p_b-p_a) + (a_b-a_a) + (w_b-w_a)

def livestock_biosecurity(i_b, i_a, c_b, c_a, ab_b, ab_a, fcr_b, fcr_a):
    return (
        0.25*(i_b-i_a)/i_b +
        0.25*(c_b-c_a)/max(c_b,1) +
        0.25*(ab_b-ab_a)/max(ab_b,1) +
        0.25*(fcr_b-fcr_a)/fcr_b
    )

def delta_c(soc_b, soc_a):
    return soc_a - soc_b

def ghg_reduction(ch4_b, ch4_a, n2o_b, n2o_a, gwp_ch4=28, gwp_n2o=265):
    return ((ch4_b-ch4_a)*gwp_ch4 + (n2o_b-n2o_a)*gwp_n2o) / 1000

def price_stability(sigma_b, sigma_a):
    return 1 - (sigma_a / sigma_b) if sigma_b else 0

def pbpe_value(loss_usd, cost_usd, yield_usd, quality_usd, food_usd, climate_usd):
    return loss_usd + cost_usd + yield_usd + quality_usd + food_usd + climate_usd

def roi(value, cost):
    return (value - cost) / cost if cost else 0


# ============================================================
# 2. LOAD DATA (ダミー → 後で AGRIX / PBPE API に置換)
# ============================================================

def load_data():
    return pd.DataFrame({
        "farm": ["Farm-A", "Farm-B", "Farm-C"],
        "yield_before": [1.0, 0.9, 1.1],
        "yield_after": [1.4, 1.3, 1.5],
        "disease_before": [0.30, 0.25, 0.35],
        "disease_after": [0.10, 0.08, 0.12],
        "brix_before": [12, 11, 13],
        "brix_after": [14, 13, 15],
        "poly_before": [180, 160, 200],
        "poly_after": [220, 210, 240],
        "def_before": [8, 10, 7],
        "def_after": [4, 5, 3],
        "spoil_before": [0.40, 0.35, 0.45],
        "spoil_after": [0.08, 0.10, 0.12],
        "market_before": [0.6, 0.55, 0.65],
        "market_after": [0.9, 0.85, 0.92],
        "soc_before": [25, 22, 28],
        "soc_after": [28, 26, 31],
        "ch4_before": [700, 650, 720],
        "ch4_after": [450, 420, 480],
        "n2o_before": [70, 65, 75],
        "n2o_after": [45, 40, 50],
        "price_sigma_before": [0.6, 0.55, 0.7],
        "price_sigma_after": [0.25, 0.22, 0.3],
        "mbt_cost": [120, 110, 130]
    })


# ============================================================
# 3. STREAMLIT UI
# ============================================================

st.set_page_config(page_title="MBT-Biosecurity-Engine Dashboard", layout="wide")
st.title("MBT‑Biosecurity‑Engine Dashboard")
st.caption("12 KPIs powering PBPE Climate Architecture")

df = load_data()

farm = st.sidebar.selectbox("Select Farm", df["farm"].unique())
row = df[df["farm"] == farm].iloc[0]

# ============================================================
# 4. KPI CALCULATIONS
# ============================================================

k1 = disease_loss_reduction(row.disease_before, row.disease_after)
k2 = yield_gain(row.yield_before, row.yield_after)
k3 = quality_premium(row.brix_before, row.brix_after, row.poly_before, row.poly_after, row.def_before, row.def_after)
k4 = anti_spoilage(row.spoil_before, row.spoil_after)
k5 = food_loss_reduction(row.market_before, row.market_after)
k6 = cost_reduction(100, 70, 80, 50, 40, 20, 30, 10)  # example
k7 = livestock_biosecurity(0.3, 0.1, 20, 5, 10, 3, 2.0, 1.7)
k8 = delta_c(row.soc_before, row.soc_after)
k9 = ghg_reduction(row.ch4_before, row.ch4_after, row.n2o_before, row.n2o_after)
k10 = price_stability(row.price_sigma_before, row.price_sigma_after)

# PBPE Value
k11 = pbpe_value(
    loss_usd=k1*2000,
    cost_usd=k6,
    yield_usd=k2*3000,
    quality_usd=k3*50,
    food_usd=k5*1000,
    climate_usd=k9*40
)

k12 = roi(k11, row.mbt_cost)

# ============================================================
# 5. DISPLAY (12 指標)
# ============================================================

st.header("📊 12 Core Biosecurity KPIs")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Disease Loss Reduction", f"{k1*100:.1f}%")
col2.metric("Yield Gain", f"{k2*100:.1f}%")
col3.metric("Quality Premium Score", f"{k3:.2f}")
col4.metric("Anti‑Spoilage Effect", f"{k4*100:.1f}%")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Food Loss Reduction (t)", f"{k5:.2f}")
col6.metric("Cost Reduction (USD)", f"{k6:.0f}")
col7.metric("Livestock Biosecurity Score", f"{k7:.2f}")
col8.metric("ΔC (Soil Carbon)", f"{k8:.2f} tC/ha")

col9, col10, col11, col12 = st.columns(4)
col9.metric("GHG Reduction", f"{k9:.2f} tCO₂e")
col10.metric("Price Stability Index", f"{k10*100:.1f}%")
col11.metric("PBPE‑Biosecurity Value", f"{k11:,.0f} USD")
col12.metric("Biosecurity ROI", f"{k12*100:.1f}%")

st.success("All 12 KPIs computed successfully.")
