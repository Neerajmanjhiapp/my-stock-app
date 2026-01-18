import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Nifty 50 Gainers", layout="wide")

st.title("🚀 Nifty 50 Top Gainers (Live)")

# Nifty 50 Stocks ki List
nifty50_tickers = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", 
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "LTIM.NS",
    "KOTAKBANK.NS", "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS",
    "TITAN.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "SUNPHARMA.NS", "ADANIENT.NS"
    # Note: Aap isme baaki 50 tickers bhi add kar sakte hain
]

@st.cache_data(ttl=60) # 60 seconds tak data cache rahega
def get_gainer_data():
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
                    "% Change": round(change, 2)
                })
        except:
            continue
    return pd.DataFrame(data_list)

# Data fetching
df = get_gainer_data()

if not df.empty:
    # Top 5 Gainers nikalna
    top_gainers = df.sort_values(by="% Change", ascending=False).head(5)
    
    # Display Metrics in Columns
    st.subheader("🔥 Top 5 Gainers Today")
    cols = st.columns(5)
    for i, row in enumerate(top_gainers.itertuples()):
        with cols[i]:
            st.metric(label=row.Symbol, value=f"₹{row.LTP}", delta=f"{row.item_3}%")

    st.divider()

    # Full List Table
    st.subheader("📊 All Nifty Stocks Performance")
    st.dataframe(df.sort_values(by="% Change", ascending=False), use_container_width=True)
else:
    st.error("Data fetch nahi ho pa raha. Internet check karein.")

st.button("Manual Refresh")
