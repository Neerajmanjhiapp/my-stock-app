import streamlit as st
import yfinance as yf

# App Title
st.title("📈 My Mobile Stock Screener")

# A simple message
st.write("Hello World! My app is now running on my mobile.")

# Test Input
ticker = st.text_input("Enter Stock Ticker (e.g., RELIANCE.NS)", "TATAMOTORS.NS")

if st.button("Get Live Price"):
    data = yf.Ticker(ticker)
    price = data.history(period="1d")['Close'].iloc[-1]
    st.metric(label=ticker, value=f"₹{price:.2f}")
