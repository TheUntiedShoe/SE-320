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
        dictionary: a dictionary containing the minimum, maximum, average, and median of the stock values
        for the last 5 years, as well as the ticker symbol used in the URL
    """
    ticker = ticker.upper()
    from_date = '2020-02-10' # a date 5 years ago, to be used in collecting data
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={from_date}&limit=9999"

    raw_data = dict() # this dictionary will contain the data as it is gathered directly from the web
    processed_data = dict() # the function will return this dictionary

    try:
        response = get(base_url + path).json() # retrieve the data from the web and format it as a json
        for row in response["data"]["tradesTable"]["rows"]:
            raw_data[row["date"]] = float(row["close"])
    except Exception as e:
        print(e)

    # sort the data so that finding the median is easier
    sorted_data = {key: num for key, num in sorted(raw_data.items(), key = lambda x: x[1])}

    # variables to contain processed values
    minimum = 1000.0
    maximum = 0.0
    avg = 0.0
    median = 0.0

    # variables to help in the calculation of the processed values
    total_records = len(sorted_data)
    count = 0

    for value in sorted_data.values():
        if value < minimum:
            # keep track of which value is the smallest
            minimum = value

        if value > maximum:
            # keep track of which value is the largest
            maximum = value

        # avg will contain the sum of all values for now so it can be averaged later
        avg += value

        if total_records % 2 == 0:
            # if the total number of records is even, check if the current record is the first of the middle two
            if count == total_records / 2:
                # if it is, then set the median to the current value for now
                median = value
            elif count == total_records / 2 + 1:
                # if the current record is the second of the middle two, then set the median to the average
                # of the previous value (contained in the median variable) and the current value
                median = (median + value) / 2
        elif count == total_records / 2 + 1:
            # if the total number of records is odd, and the current item is the middle, then the current value is the median
            median = value

        # increment the count variable
        count += 1

    # now that the loop is finished, average avg
    avg = avg / total_records

    # add data to processed_data
    processed_data["min"] = minimum
    processed_data["max"] = maximum
    processed_data["avg"] = avg
    processed_data["median"] = median
    processed_data["ticker"] = ticker

    return processed_data

download_data("AAPL")
