import streamlit as st
from math import log, sqrt, exp
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
#######################
# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model by Mark Galperin",
    layout="wide",
    initial_sidebar_state="expanded")

def call_calculation(spot, strike, rf, sigma, time):  # time in years
    d1 = (log(spot / strike) + (rf + 0.5 * sigma**2) * time) / (sigma * sqrt(time))
    d2 = d1 - sigma * sqrt(time)
    call = spot * norm.cdf(d1) - strike * exp(-rf * time) * norm.cdf(d2)
    return call

def put_calculation(spot, strike, rf, sigma, time):
    d1 = (log(spot / strike) + (rf + 0.5 * sigma**2) * time) / (sigma * sqrt(time))
    d2 = d1 - sigma * sqrt(time)
    put = strike * exp(-rf * time) * norm.cdf(-d2) - spot * norm.cdf(-d1)
    return put

# Heatmap for Options
def generate_heatmap(option_type, strike, rf, time, spot_range, vol_range):
    spot_vals = np.linspace(*spot_range, 10)

    vol_vals = np.linspace(*vol_range, 10)

    heatmap_data = np.zeros((len(vol_vals), len(spot_vals)))

    for i, vol in enumerate(vol_vals):
        for j, spot in enumerate(spot_vals):
            if option_type == "Call":
                price = call_calculation(spot, strike, rf, vol, time)
            else:
                price = put_calculation(spot, strike, rf, vol, time)
            heatmap_data[i, j] = price

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(heatmap_data, xticklabels=np.round(spot_vals, 2), yticklabels=np.round(vol_vals, 2),
                cmap="viridis", ax=ax, cbar_kws={'label': 'Option Price'})
    ax.set_xlabel("Spot Price")
    ax.set_ylabel("Volatility")
    ax.set_title(f"{option_type} Option Price Sensitivity Heatmap")
    return fig


# --- Streamlit App ---

st.title("Black-Scholes Option Pricer")

# Input sliders
with st.sidebar:
    st.title("Black-Scholes Model Call/Put")
    st.write("By: ")
    linkedin_url = "https://www.linkedin.com/in/mark-galperin-20905b253/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;"> Mark Galperin </a>', unsafe_allow_html=True)
st.sidebar.header("Input Parameters")
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])
spot = st.sidebar.number_input("Spot Price (S)", value=100.0)
strike = st.sidebar.number_input("Strike Price (K)", value=100.0)
rf = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05, format="%.4f")
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2, format="%.4f")
time = st.sidebar.number_input("Time to Maturity (T, in years)", value=1.0, format="%.2f")

# Calculate and display result
if option_type == "Call":
    price = call_calculation(spot, strike, rf, sigma, time)
else:
    price = put_calculation(spot, strike, rf, sigma, time)

st.markdown(f"### {option_type} Option Price: ${price:.2f}")
st.subheader("Option Price Sensitivity Heatmap")

spot_range = st.slider("Select Spot Price Range", 50, 150, (80, 120))
vol_range = st.slider("Select Volatility Range", 0, 100, (10, 40))

# Convert % to decimals for calculation
vol_range_decimal = (vol_range[0] / 100, vol_range[1] / 100)

fig = generate_heatmap(option_type, strike, rf, time, spot_range, vol_range_decimal)
st.pyplot(fig)
