# ---------------------------------------------------------
# Multi-Page Streamlit Application: ESG Investment Navigator
# Language: Python
# Author: [Mahmoud Tahawi]
# Date Created: [02.12.2024]
# Description: This file serves as the main entry point for a Streamlit-based
#              multi-page application designed to provide insights into
#              investment portfolios, user investment preferences, financial forecasts, and
#              ESG (Environmental, Social, Governance) filtering. Users can
#              navigate between pages via a sidebar menu. Key features include:
#              - Displaying user-specific ESG investment details.
#              - Providing news updates on investments.
#              - Offering AI-based forecast analysis.
# Assistance: Some portions of the code, including comments and structure,
#             were inspired by ChatGPT, an AI language model by OpenAI.
# ---------------------------------------------------------
import streamlit as st

from views.forecast import show_forecast_page
from views.investment_portfolio_page import investment_portfolio_page
from views.news_page import news_page
from views.profile_page import profile_page

# DEBUG
# st.session_state.answers = {'name': 'hector',
#                             'survey_answers': {'USER_RISK_TOLERANCE': 'Low', 'USER_ESG_AWARENESS_RATE': 3,
#                                                'USER_IMPACT_INVESTMENT_RATE': 3, 'USER_E_WEIGHT': 3, 'USER_S_WEIGHT': 3,
#                                                'USER_G_WEIGHT': 3, 'USER_CONTROVERSY_THRESHOLD': 3,
#                                                'USER_GREEN_INDUSTRY_THRESHOLD': 3, 'USER_ESG_SCORE_THRESHOLD': 3,
#                                                'USER_SECTORS': ['Real Estate', 'Technology', 'Energy']}}

# Page selection, Matching each entry in the dropdown list to the function that is going to render the selected page
menu = {
    "Profile": profile_page,
    "Investment portfolio": investment_portfolio_page,
    "News": news_page,
    "AI": show_forecast_page,
}

# Create a drop down list using dictionary keys as entries, store the selected entry in variable choice
choice = st.sidebar.selectbox("Menu", menu)

# if the profile is submitted, go directly to the portfolio page
if choice == "Profile" and "answers" in st.session_state:
    investment_portfolio_page()
else:
    # call the function to show the selected page
    menu.get(choice)()
