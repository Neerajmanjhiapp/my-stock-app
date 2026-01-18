import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Nifty 50 Gainers", layout="wide")
st.title("🚀 Nifty 50 Top Gainers (Live)")

nifty50_tickers = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", 
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "LTIM.NS",
    "KOTAKBANK.NS", "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS",
    "TITAN.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "SUNPHARMA.NS", "ADANIENT.NS"
]

@st.cache_data(ttl=60)
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
                    "Change": round(change, 2) # Column ka naam yahan 'Change' hai
                })
        except:
            continue
    return pd.DataFrame(data_list)

df = get_gainer_data()

if not df.empty:
    top_gainers = df.sort_values(by="Change", ascending=False).head(5)
    
    st.subheader("🔥 Top 5 Gainers Today")
    cols = st.columns(5)
    
    # Yahan correction ki gayi hai: row.Change use kiya hai
    for i, row in enumerate(top_gainers.itertuples()):
        with cols[i]:
            st.metric(label=row.Symbol, value=f"₹{row.LTP}", delta=f"{row.Change}%")

    st.divider()
    st.subheader("📊 All Nifty Stocks Performance")
    # Table mein display
    st.dataframe(df.sort_values(by="Change", ascending=False), use_container_width=True)
else:
    st.error("Data fetch nahi ho pa raha.")
