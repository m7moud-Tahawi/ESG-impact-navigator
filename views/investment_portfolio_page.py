# ---------------------------------------------------------
# ESG Investment Portfolio Optimizer: Newton Analytics
# Language: Python
# Author: [Mahmoud Tahawi]
# Date Created: [02.12.2024]
# Description: This script provides functionality for constructing
#              and visualizing optimized ESG investment portfolios
#              using user survey preferences. Key features include:
#              - Calculating portfolio weights based on ESG scores.
#              - Fetching enriched company data from Yahoo Finance based
#              on Survey answers (Sectors and controversies).
#              - Visualizing portfolio distributions with Plotly.
# Assistance: Code structure and comments partially inspired by ChatGPT,
#             an AI language model by OpenAI. Guided by Mohammad Tahawi.
# ---------------------------------------------------------

#Importing required libraries
import math

import pandas as pd
import plotly.express as px
import streamlit as st

import data.survey_constants as survey_constants
from api.newton_analytics_engine import NewtonAnalyticsEngine
from api.yahoo_finance_repository import data_repo

analysis_engine = NewtonAnalyticsEngine()


def investment_portfolio_page():
    # to calculate portfolio, we first need survey answers
    if "answers" not in st.session_state:
        st.write("Please answer survey first ....")
    else:
        # Read answers from session_state, stored there by profile page
        sectors = st.session_state["answers"]["survey_answers"][survey_constants.USER_SECTORS]

        # get the accepted controversies count for the investor, using his survey answer
        controversies_count = get_accepted_controversies_count(
            st.session_state["answers"]["survey_answers"][survey_constants.USER_CONTROVERSY_THRESHOLD])

        # get tickers data from yfinance api
        initial_companies_data = data_repo.get_investment_universe(sectors, controversies_count)

        # Add more fields to the initial data: e_score, s_score, g_score, sector, controversies
        enriched_companies = enrich_companies_data(initial_companies_data)

        for c in enriched_companies:
            # Calculate weight of each company based on its ESG score and investor preferences
            c["score"] = get_preference_score(c, st.session_state["answers"]["survey_answers"])

        # st.write(st.session_state["answers"])

        # Sort based on the calculated weight
        sorted_companies = sorted(enriched_companies, key=lambda c: c["score"], reverse=True)
        # st.write({"sorted_companies": sorted_companies})

        # Use Newton API to get recommended portfolio, taking into account the investor risk tolerance
        recommended_portfolio = get_portfolio_recommendation(sorted_companies, 10,
                                                             map_risk_level(
                                                                 st.session_state["answers"]["survey_answers"][
                                                                     survey_constants.USER_RISK_TOLERANCE]))

        if recommended_portfolio is None:
            st.write("No suitable portfolio found")
        else:
            st.session_state.recommended_portfolio = recommended_portfolio
            # st.write({"recommended_portfolio": recommended_portfolio})

            col1, col2 = st.columns(2)
            with col1:
                st.header(f"Return: {recommended_portfolio['return']:.2%}")

            with col2:
                st.header(f"Risk: {recommended_portfolio['risk']:.2%}")

            df = pd.DataFrame(recommended_portfolio["companies"])
            df.set_index("name", inplace=True)
            # st.write(df)

            plot_company_proportions_pie_chart(recommended_portfolio)
            plot_company_sectors_pie_chart(recommended_portfolio)
            plot_company_bar_chart(recommended_portfolio)
        # List of companies names
        # Pie chart for sectors
        # Risk indicator
        # Estimated return
        # Pie chart proportions


def plot_company_proportions_pie_chart(portfolio):
    columns = ["Name", "%"]
    names = [c["name"] for c in portfolio["companies"]]
    total_sum = sum([abs(v) for v in portfolio["proportions"]])
    value = [abs(v) / total_sum for v in portfolio["proportions"]]
    data = zip(names, value)
    df = pd.DataFrame(data, columns=columns)
    fig = px.pie(df, values='%', names='Name', title="Portfolio Distribution")
    st.plotly_chart(fig)


def plot_company_sectors_pie_chart(portfolio):
    df = pd.DataFrame(portfolio["companies"])
    frequency = df["sector"].value_counts()
    fig = px.pie(names=frequency.index, values=frequency.values, title="Sectors Distribution")
    st.plotly_chart(fig)


def plot_company_bar_chart(portfolio):
    df = pd.DataFrame(portfolio["companies"])
    df.set_index("name", inplace=True)
    fig = px.bar(df.iloc[:, 1:4], title="ESG combined")
    st.plotly_chart(fig)


def map_risk_level(risk_level):
    """
    Maps risk levels ('low', 'moderate', 'high') to numeric values (5, 10, 20).

    Parameters:
        risk_level (str): The risk level as a string ('low', 'moderate', 'high').

    Returns:
        int: The numeric value corresponding to the risk level.
    """
    # Define the mapping dictionary

    risk_mapping = {
        "low": 0.1,
        "moderate": 0.15,
        "high": 0.2
    }

    # Return the mapped value or raise an error if the input is invalid
    if risk_level.lower() in risk_mapping:
        return risk_mapping[risk_level.lower()]
    else:
        raise ValueError(f"Invalid risk level: '{risk_level}'. Must be one of {list(risk_mapping.keys())}.")


def get_portfolio_recommendation(companies, portfolio_size, risk_tolerance):

    # Loop over the companies taking n=portfolio_size companies at a time
    for i in range(len(companies) - portfolio_size + 1):
        tickers = [c["ticker"] for c in companies[i:i + portfolio_size]]  # Extract the current window

        # Get recommended portfolios using those companies
        result = analysis_engine.get_portfolio_data(tickers)

        portfolios = result["data"]

        # filter portfolios based on risk tolerance.
        # first element is return, last element is risk
        # Filter Portfolios according to the investor's risk tolerance
        portfolios = [p for p in portfolios if p[-1] <= risk_tolerance]

        # Sort portfolios on expected reutrn
        sorted_portfolio = sorted(portfolios, key=lambda c: c[0], reverse=True)

        # if we have positive return in the recommendations
        if len(sorted_portfolio) > 0 and sorted_portfolio[0][0] > 0:
            # take first recommended portfolio (highest return)
            target_portfolio = sorted_portfolio[0]
            return {"tickers": tickers, "proportions": target_portfolio[1:portfolio_size + 1],
                    "risk": target_portfolio[-1], "return": target_portfolio[0],
                    "companies": companies[i:i + portfolio_size]}

    return None


def enrich_companies_data(initial_companies_data):
    try:
        for c in initial_companies_data:
            # Y! finance gives ESG RISK, lower risk implies higher performance
            c.update({
                "e_score": data_repo.get_e_score(c["ticker"]),
                "s_score": data_repo.get_s_score(c["ticker"]),
                "g_score": data_repo.get_g_score(c["ticker"]),
                "controversies": data_repo.get_controversies(c["ticker"]),
                "sector": data_repo.get_sector(c["ticker"])
            })
        return initial_companies_data
    except Exception as e:
        print(e)


def get_accepted_controversies_count(controversy_threshold):
    match controversy_threshold:
        case 1 | 2:
            return math.inf
        case 3:
            return 3
        case 4:
            return 2
        case 5:
            return 1
        case _:
            raise ValueError(f"Unexpected value {controversy_threshold} for calculating accepted controversies count")


def get_preference_score(company, survey_answers):
    weights = [
        survey_answers[survey_constants.USER_E_WEIGHT],
        survey_answers[survey_constants.USER_S_WEIGHT],
        survey_answers[survey_constants.USER_G_WEIGHT]
    ]

    scores = [
        company["e_score"],
        company["s_score"],
        company["g_score"]
    ]

    return sum([weights[i] * scores[i] for i in range(3)])
