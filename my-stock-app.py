import streamlit as st
import yfinance as yf
import pandas as pd

# Page setup for Mobile
st.set_page_config(page_title="Pocket Trader", page_icon="📈", layout="wide")

st.title("📈 Pocket Stock Screener")

# 1. Watchlist Section
st.subheader("My Watchlist")
watchlist = ["RELIANCE.NS", "TCS.NS", "TATAMOTORS.NS", "SBIN.NS", "INFY.NS", "ZOMATO.NS"]

cols = st.columns(len(watchlist))

for i, ticker in enumerate(watchlist):
    try:
        stock = yf.Ticker(ticker)
        # Getting live price and change
        info = stock.history(period="2d")
        current_price = info['Close'].iloc[-1]
        prev_price = info['Close'].iloc[-2]
        change = ((current_price - prev_price) / prev_price) * 100
        
        with cols[i % 3]: # Mobile friendly grid
            st.metric(label=ticker.replace(".NS", ""), 
                      value=f"₹{current_price:.2f}", 
                      delta=f"{change:.2f}%")
    except:
        continue

st.divider()

# 2. Detailed Search Section
st.subheader("🔍 Stock Analysis")
search_ticker = st.text_input("Enter Ticker (e.g., ADANIENT.NS)", "RELIANCE.NS").upper()

if st.button("Analyze Stock"):
    with st.spinner('Fetching Data...'):
        stock_detail = yf.Ticker(search_ticker)
        hist = stock_detail.history(period="5d")
        
        if not hist.empty:
            st.write(f"### {search_ticker} Price History")
            st.line_chart(hist['Close']) # Mobile par graph bahut accha dikhta hai
            
            # Key Stats
            col1, col2 = st.columns(2)
            col1.write(f"**Day High:** ₹{hist['High'].iloc[-1]:.2f}")
            col2.write(f"**Day Low:** ₹{hist['Low'].iloc[-1]:.2f}")
        else:
            st.error("Stock not found. Please add .NS for Indian stocks.")

st.sidebar.info("Tip: Ye app ab aapke pocket mein hai. Browser menu se 'Add to Home Screen' karna na bhoolein!")
