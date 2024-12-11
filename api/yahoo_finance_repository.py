# -----------------------------------------------
# YahooFinanceRepository: Stock Market Data with ESG Metrics
# Language: Python
# Author: [Mahmoud Tahawi]
# Date: [02.12.2024]
# Description: This class interacts with Yahoo Finance APIs to fetch
#              stock market and ESG-related data. It uses caching
#              to optimize API calls and improve performance.
# Assistance:  partially guided by Mohammad Tahawi and ChatGPT .
# -----------------------------------------------


# A Python library used to fetch stock market and financial data, including ESG scores and sustainability metrics
import logging

import yfinance as yf

logger = logging.getLogger(__name__)
#CacheMixin and SQLiteCache enable API request caching.
#Prevents repeated API calls by storing responses in a local SQLite database
from requests_cache import CacheMixin, SQLiteCache
from requests import Session


# This is used to create a session where we cache API responses in database
class CachedSession(CacheMixin, Session):
    pass


session = CachedSession(
    backend=SQLiteCache("yfinance.cache"),
)


class YahooFinanceRepository:
    MAX_RISK_SCORE = 40

    def __init__(self):
        self.cache = {}

    # read the required field from the API response
    def _parse_response(self, response, field, default_value):
        if response is None or response.empty:
            return default_value
        return response.loc[field].esgScores or default_value

    def get_esg_score(self, ticker):
        logger.info(f"Requesting {ticker}")
        if ticker in self.cache:
            logger.info(f"{ticker} is already cached, skipping request")
            return self.cache[ticker].sustainability

        stock = yf.Ticker(ticker, session=session)
        if not stock:
            logger.warning(f"Could not find ticker {ticker}")
            return None
        elif stock.sustainability.empty:
            logger.warning(f"Could not find ESG data for {ticker}")
            return None

        self.cache[ticker] = stock
        return stock.sustainability

    def get_sector(self, ticker):
        logger.info(f"Requesting {ticker}")
        if ticker in self.cache:
            logger.info(f"{ticker} is already cached, skipping request")
            return self.cache[ticker].info.get("sector", None)

        stock = yf.Ticker(ticker, session=session)
        if not stock:
            logger.warning(f"Could not find ticker {ticker}")
            return None
        elif stock.sustainability.empty:
            logger.warning(f"Could not find ESG data for {ticker}")
            return None

        self.cache[ticker] = stock
        return stock.info.get("sector", None)

    def get_news(self, ticker):
        logger.info(f"Requesting {ticker}")
        if ticker in self.cache:
            logger.info(f"{ticker} is already cached, skipping request")
            return self.cache[ticker].get_news()

        stock = yf.Ticker(ticker, session=session)
        if not stock:
            logger.warning(f"Could not find ticker {ticker}")
            return None
        elif stock.sustainability.empty:
            logger.warning(f"Could not find ESG data for {ticker}")
            return None

        self.cache[ticker] = stock
        return stock.get_news()

    def get_controversies(self, ticker):
        return self._parse_response(self.get_esg_score(ticker), "highestControversy", 10)

    # yfinance returns RISK and score, we convert risk to score by deducting it from 40 (max risk according to yfinance)

    def get_e_score(self, ticker):
        return YahooFinanceRepository.MAX_RISK_SCORE - self._parse_response(self.get_esg_score(ticker),
                                                                            "environmentScore",
                                                                            YahooFinanceRepository.MAX_RISK_SCORE)

    def get_s_score(self, ticker):
        return YahooFinanceRepository.MAX_RISK_SCORE - self._parse_response(self.get_esg_score(ticker), "socialScore",
                                                                            YahooFinanceRepository.MAX_RISK_SCORE)

    def get_g_score(self, ticker):
        return YahooFinanceRepository.MAX_RISK_SCORE - self._parse_response(self.get_esg_score(ticker),
                                                                            "governanceScore",
                                                                            YahooFinanceRepository.MAX_RISK_SCORE)

    def get_investment_universe(self, sectors, highest_controversies_threshold):
        countries = ['us', 'gr', 'ch', 'au', 'fr']

        # Add filters for the yfinance tickers' API

        # filter #1: companies must be in the selected countries
        q_region = yf.EquityQuery('or', [yf.EquityQuery('eq', ['region', country]) for country in countries])
        # filter #2: companies must be in the selected sectors
        q_sectors = yf.EquityQuery('or', [yf.EquityQuery('eq', ['sector', sector]) for sector in sectors])
        # filter #3: companies must have less controversies than investor's limit
        q_controversies = yf.EquityQuery('lt', ['highest_controversy', highest_controversies_threshold])

        # filter #4: companies must have ESG data
        esg_score = yf.EquityQuery('gt', ['esg_score', 0])
        e_score = yf.EquityQuery('gt', ['environmental_score', 0])
        s_score = yf.EquityQuery('gt', ['social_score', 0])
        g_score = yf.EquityQuery('gt', ['governance_score', 0])
        q = yf.EquityQuery('and', [q_controversies, q_region, q_sectors, esg_score, e_score, s_score, g_score])


        # Screener is the yfinance class used to get send queries with filters about companies
        screener = yf.Screener()
        screener.set_body({
            "offset": 0,
            "size": 200,
            "sortField": "esg_score",
            "sortType": "desc",
            "quoteType": "equity",
            "query": q.to_dict(),
            "userId": "",
            "userIdType": "guid"
        })

        r = screener.response

        # Extract the data needed from yfinance response
        return [{"ticker": quote['symbol'], "name": quote['shortName']} for quote in r["quotes"]]


data_repo = YahooFinanceRepository()
