import yfinance as yf
import pandas as pd
import streamlit as st

# Function to fetch and process stock data
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data['20DayAvgVolume'] = stock_data['Volume'].rolling(window=20).mean()
    return stock_data

# Function to identify breakout days and calculate returns
def analyze_breakouts(data, vol_threshold, price_threshold, holding_period):
    breakout_days = []
    for i in range(20, len(data) - holding_period):
        row = data.iloc[i]
        avg_vol = data['20DayAvgVolume'].iloc[i]
        prev_close = data['Close'].iloc[i - 1]
        if row['Volume'] > avg_vol * (vol_threshold / 100) and (row['Close'] / prev_close - 1) * 100 >= price_threshold:
            breakout_day = {
                'Date': row.name,
                'BreakoutClose': row['Close'],
                'HoldingClose': data['Close'].iloc[i + holding_period],
                'Return (%)': ((data['Close'].iloc[i + holding_period] / row['Close']) - 1) * 100
            }
            breakout_days.append(breakout_day)
    print("code finished")
    return pd.DataFrame(breakout_days)

# Streamlit app setup
st.title("Stock Breakout Analysis")
ticker = st.text_input("Ticker", value="AAPL")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
vol_threshold = st.number_input("Volume Breakout Threshold (%)", value=200)
price_threshold = st.number_input("Price Change Threshold (%)", value=2)
holding_period = st.number_input("Holding Period (days)", value=10, step=1)
if st.button("Generate Report"):
    try:
        stock_data = get_stock_data(ticker, start_date, end_date)
        breakout_report = analyze_breakouts(stock_data, vol_threshold, price_threshold, holding_period)
        st.dataframe(breakout_report)
        csv = breakout_report.to_csv(index=False)
        st.download_button("Download Report as CSV", csv, "breakout_report.csv")
    except Exception as e:
        st.error(f"Error: {e}")
