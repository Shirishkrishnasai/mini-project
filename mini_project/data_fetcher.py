import yfinance as yf

def get_stock_data(ticker, start_date, end_date):
    """
    Fetches stock data from Yahoo Finance and calculates the 20-day average volume.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        pandas.DataFrame: Stock data with 20-day average volume.
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data['20DayAvgVolume'] = stock_data['Volume'].rolling(window=20).mean()
    return stock_data
