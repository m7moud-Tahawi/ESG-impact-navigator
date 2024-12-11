# CS 5.8


### Install dependencies

```
pip install -r requirements.txt
```

---

# **ESG Impact Navigator**

## **Overview**
The ESG Impact Navigator is a Python-based multi-page application developed with Streamlit. This tool helps users make sustainable investment decisions by analyzing their preferences, financial forecasts, and news updates in alignment with ESG (Environmental, Social, and Governance) principles.

---

## **Features**
- **Profile Page**: Capture user-specific investment preferences and ESG parameters.
- **Investment Portfolio**: View ESG-compliant portfolios tailored to user preferences.
- **News Page**: Stay updated with the latest investment news realting to your portfolio and ESG-related topics.
- **AI Forecast**: Leverage AI models to provide financial forecasts.

---

## **Installation**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd esg-impact-navigator
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**
1. Launch the app:
   ```bash
   streamlit run app.py
   ```
2. Use the sidebar to navigate between pages:
   - **Profile**
   - **Investment Portfolio**
   - **News**
   - **AI Forecast**
3. Customize preferences on the Profile page to influence other pages.

---

## **Dependencies**
Refer to the `requirements.txt` file for the complete list:
- **Streamlit**
- **Python-dotenv**
- **yfinance**
- **Requests**
- **Plotly**
- **Pandas**
- **Requests-Cache**
- **Prophet**
- **Matplotlib**

---

## **Project Structure**
- **`app.py`**: Entry point for the Streamlit app. Manages page navigation.
- **`views`**: Directory containing separate modules for each page:
  - **`forecast.py`**: Handles AI-based financial forecasting.
  - **`investment_portfolio_page.py`**: Displays user-tailored ESG portfolios.
  - **`news_page.py`**: Fetches and presents investment-related news.
  - **`profile_page.py`**: Captures user-specific ESG preferences.

---
