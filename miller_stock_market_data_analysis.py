"""
This module creates a function that imports NASDAQ data on stocks in the years 2020-2024 from the web
"""

from requests import get

def download_data(ticker: str) -> dict:
    """
    Downloads data from the NASDAQ website

    Args:
        ticker (str): the ticker symbol used in the url to retrieve data

    Returns:
        dictionary: a dictionary containing the stock values for the given ticker symbol for the last 5 years
    """
    ticker = ticker.upper()
    from_date = '2020-02-10' # a date 5 years ago, to be used in collecting data
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={from_date}&limit=9999"

    data = dict() # the function will return this dictionary

    try:
        response = get(base_url + path).json() # retrieve the data from the web and format it as a json
        for row in response["data"]["tradesTable"]["rows"]:
            data[row["date"]] = row["close"]
    except Exception as e:
        print(e)

    return data

download_data("AAPL")
