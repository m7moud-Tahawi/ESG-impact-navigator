# ---------------------------------------------------------
# Class: NewtonAnalyticsEngine
#
# Language: Python
# Author: [Mahmoud Tahawi]
# Date Created: [02.12.2024]
# Description: This class provides a method to fetch portfolio analytics data
#              from the Newton Analytics API. The method, `get_portfolio_data`,
#              accepts a list of ticker symbols, formats the request parameters,
#              and retrieves the portfolio analysis data for the given tickers
#              over a 12-month period. The API endpoint and request interval
#              are pre-configured.
#
# Usage:
#     - Instantiate the NewtonAnalyticsEngine class.
#     - Call `get_portfolio_data` with a list of tickers (e.g., ["AAPL", "MSFT"]).
# Assistance:  partially guided by Mohammad Tahawi and ChatGPT
# ---------------------------------------------------------

import requests


class NewtonAnalyticsEngine:
    BASE_URL = "https://api.newtonanalytics.com/modern-portfolio/"

    def get_portfolio_data(self, tickers):
        """
        Fetch portfolio data from the given API.

        Parameters:
            tickers (list of str): List of ticker symbols.

        Returns:
            dict: JSON response from the API.
        """
        # Convert list of tickers to a comma-separated string
        tickers_str = ",".join(tickers)

        # Define the query parameters
        params = {
            "tickers": tickers_str,
            "interval": '1mo',  # one month
            "observations": 12
        }

        # Make the GET request
        response = requests.get(NewtonAnalyticsEngine.BASE_URL, params=params)

        # Raise an exception if the request failed
        response.raise_for_status()

        # Return the JSON response
        return response.json()
