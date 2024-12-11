# ---------------------------------------------------------
# Investment News Viewer
# Language: Python
# Author: [Mahmoud Tahawi]
# Date Created: [02.12.2024]
# Description: This script displays financial news related to the user's
#               portfolio. Key features include:
#              - Fetching and displaying the latest news for portfolio tickers.
#              - User-friendly news layout with thumbnails and links.
# Assistance: Code structure and comments partially inspired by ChatGPT,
#             an AI language model by OpenAI.
# ---------------------------------------------------------
import streamlit as st
from datetime import datetime

from api.yahoo_finance_repository import data_repo


def news_page():
    # We don't show news if the portfolio hasn't been calculated yet
    if "recommended_portfolio" not in st.session_state:
        st.write("No portfolio to show news....")
    else:
        # get the recommended portfolio from the session_state
        portfolio = st.session_state.recommended_portfolio
        # for every ticker, use yfinance api to get news about it,
        newsList = [data_repo.get_news(t) or None for t in portfolio["tickers"]]
        # take latest news for each company, skip companies that don't have news (Empty list of news)
        news =  [ticker_news[0] for ticker_news in newsList if ticker_news is not None and len(ticker_news) > 0]

        col1, col2 = st.columns(2)

        # display news in two columns, up to 5 each
        with col1:
            for item in news[0:5]:
                # call the function that takes the api response for a news item, and show a news entry
                display_news_item(item)

        with col2:
            for item in news[5:]:
                display_news_item(item)


def display_news_item(item):
    st.subheader(item['title'])
    st.write(f"**Published by:** {item['publisher']}")
    st.write(f"**Type:** {item['type']}")

    # Convert Unix time to a human-readable format
    publish_time = datetime.utcfromtimestamp(item['providerPublishTime']).strftime('%Y-%m-%d %H:%M:%S')
    st.write(f"**Published on:** {publish_time}")

    # Display thumbnail image
    if 'thumbnail' in item and 'resolutions' in item['thumbnail']:
        thumbnail_url = item['thumbnail']['resolutions'][0]['url']  # Using the firsst resolution
        st.image(thumbnail_url, use_container_width=True)

    # Link to the full story
    st.markdown(f"[Read Full Article]({item['link']})", unsafe_allow_html=True)

    # Related tickers
    if 'relatedTickers' in item:
        st.write(f"**Related Tickers:** {', '.join(item['relatedTickers'])}")
    # Separator
