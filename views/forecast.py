# ---------------------------------------------------------
# Stock Price Prediction with Prophet: ESG Impact Navigator
# Language: Python
# Author: [Mahmoud Tahawi]
# Date Created: [02.12.2024]
# Description: This script uses Streamlit and Prophet to predict
#              future stock prices based on historical data fetched
#              from Yahoo Finance.
#              Key features include:
#              - Fetching stock data from Yahoo Finance.
#              - Preparing data for Prophet's forecasting requirements.
#              - Visualizing predictions alongside actual historical prices.
# Assistance: Guidance Provided by Mohammad Tahawi. Code structure and comments partially inspired by ChatGPT,
#             an AI language model by OpenAI. 
# ---------------------------------------------------------
#Used to create the forecast plot showing actual vs. predicted stock prices.
import matplotlib.pyplot as plt

import pandas as pd
import streamlit as st
import yfinance as yf
#A forecasting library developed by Meta for time series prediction.
#Trains a model to predict stock prices.
from prophet import Prophet


# Step 1: Fetch stock data from Yahoo Finance
def fetch_stock_data(ticker):
    # Git historical data from yfinance
    stock_data = yf.download(ticker, start="2015-01-01", end="2023-12-31")
    # Use timestamp as the index for rows in dataframe
    stock_data.reset_index(inplace=True)
    return stock_data


# Step 2: Prepare data for Prophet
def prepare_data_for_prophet(stock_data):
    # Prophet requires columns: 'ds' (date) and 'y' (value to predict)
    df = pd.DataFrame()
    # remove time zone from date, Prophet doesn't support it
    df["ds"] = stock_data["Date"].dt.tz_localize(None)
    # The "Close" column contains a nested dataframe, which contains one column, which is the close value for the chosen ticker
    df["y"] = stock_data["Close"][stock_data["Close"].columns[0]]
    return df


# Step 3: Train Prophet model
def train_prophet_model(prophet_data):
    model = Prophet(daily_seasonality=True)
    model.fit(prophet_data) # train step
    return model


# Step 4: Make future predictions
def make_predictions(model, periods):
    future = model.make_future_dataframe(periods=periods)  # Predict next 'periods' days
    forecast = model.predict(future)
    return forecast


# Step 5: Visualize the results
def plot_forecast(stock_data, forecast):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_data["ds"], stock_data["y"], label="Actual Prices")
    ax.plot(forecast["ds"], forecast["yhat"], label="Predicted Prices", color="orange")
    ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="orange", alpha=0.2)
    ax.legend()
    ax.set_title("Stock Price Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    st.pyplot(fig)


def show_forecast_page():
    st.title("ESG Impact Navigator")
    st.header("Stock Price Prediction with Prophet")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):")
    if ticker:
        # Fetch data
        st.write(f"Fetching data for {ticker}...")
        stock_data = fetch_stock_data(ticker)

        if not stock_data.empty:
            st.write("Data fetched successfully!")

            # Display raw data
            st.subheader("Raw Stock Data")
            st.write(stock_data.head())

            # Prepare data for Prophet (ML model developed by Meta)
            prophet_data = prepare_data_for_prophet(stock_data)

            # Train the model
            st.write("Training the Prophet model...")
            model = train_prophet_model(prophet_data)

            # Make future predictions
            st.write("Making future predictions...")
            forecast = make_predictions(model, periods=365)  # Predict 1 year into the future

            # Display forecast data
            st.subheader("Forecast Data")
            st.write(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())

            # Plot results
            st.subheader("Forecast Plot")
            plot_forecast(prophet_data, forecast)
        else:
            st.write("Failed to fetch data. Please check the ticker.")
