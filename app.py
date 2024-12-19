import streamlit as st
from mini_project.data_fetcher import get_stock_data
from mini_project.breakout_analyzer import analyze_breakouts

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
