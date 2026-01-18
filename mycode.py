import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Nifty 50 Tracker", layout="wide")
st.title("📈 Nifty 50: Top Gainers & Losers")

# Nifty 50 ki main companies
nifty50_tickers = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", 
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "LTIM.NS",
    "KOTAKBANK.NS", "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS",
    "TITAN.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "SUNPHARMA.NS", "ADANIENT.NS",
    "JIOFIN.NS", "TATASTEEL.NS", "NTPC.NS", "POWERGRID.NS", "COALINDIA.NS"
]

@st.cache_data(ttl=300) # 5 minute tak data save rahega taaki app fast chale
def get_stock_data():
    data_list = []
    for ticker in nifty50_tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            if len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change = ((current_price - prev_price) / prev_price) * 100
                data_list.append({
                    "Symbol": ticker.replace(".NS", ""),
                    "LTP": round(current_price, 2),
                    "Change": round(change, 2)
                })
        except:
            continue
    return pd.DataFrame(data_list)

df = get_stock_data()

if not df.empty:
    # --- TOP GAINERS SECTION ---
    st.subheader("🔥 Top 5 Gainers")
    top_gainers = df.sort_values(by="Change", ascending=False).head(5)
    cols_g = st.columns(5)
    for i, row in enumerate(top_gainers.itertuples()):
        with cols_g[i]:
            st.metric(label=row.Symbol, value=f"₹{row.LTP}", delta=f"{row.Change}%")

    st.write("---") # Partition Line

    # --- TOP LOSERS SECTION ---
    st.subheader("❄️ Top 5 Losers")
    top_losers = df.sort_values(by="Change", ascending=True).head(5)
    cols_l = st.columns(5)
    for i, row in enumerate(top_losers.itertuples()):
        with cols_l[i]:
            # Delta automatic red dikhayega kyunki value minus mein hogi
            st.metric(label=row.Symbol, value=f"₹{row.LTP}", delta=f"{row.Change}%")

    st.divider()
    
    # --- FULL TABLE ---
    st.subheader("📊 Full Market Performance")
    st.dataframe(df.sort_values(by="Change", ascending=False), use_container_width=True)
else:
    st.error("Data load nahi ho raha, thodi der baad try karein.")
