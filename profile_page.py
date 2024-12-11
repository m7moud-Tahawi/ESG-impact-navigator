# ---------------------------------------------------------
# ESG Investment Navigator: Profile Page
# Language: Python
# Author: [Mahmoud Tahawi]
# Date Created: [02.12.2024]
# Description: This script implements the Profile Page for the ESG Impact Navigator application.
#              Users can provide their preferences and complete an ESG-focused survey to personalize
#              their investment experience. Key features:
#              - User input for name and ESG preferences.
#              - Risk tolerance selection.
#              - ESG-related survey questions.
#              - Preferred sectors selection.
# Assistance: Code structure and comments partially inspired by ChatGPT,
#             an AI language model by OpenAI.
# ---------------------------------------------------------

# Import necessary libraries
import streamlit as st

import data.survey_constants as survey_constants


def profile_page():
    st.title("ESG Impact Navigator")
    st.image(r"Logo.jpg", caption=None, width=None)
    st.logo(r"Logo.jpg", size="large", link=None, icon_image=None)

    # Create a form to get user input
    with st.form("my_form"):
        st.header("Profile Page")
        name = st.text_input("Name")

        # Variables to store survey answers and share them with other pages
        answers = {}
        risk_options = ["Low", "Moderate", "High"]
        # Low = from 5% to 10%, Moderate= 10% to 20%, High= 20% and higher.
        # Store the answer for risk tolerance question
        answers[survey_constants.USER_RISK_TOLERANCE] = st.radio("Select your risk tolerance level",
                                                                 options=risk_options, label_visibility="visible")

        # Possible answers for survey questions
        survey_options = [
            "Strongly disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly agree",
        ]

        # dictionary mapping from question's key to questions' text
        questions = {
            survey_constants.USER_ESG_AWARENESS_RATE: "I prioritize environmental sustainability when making investment decisions",
            survey_constants.USER_IMPACT_INVESTMENT_RATE: "I am comfortable with investing in companies that may have a smaller carbon footprint, even if it could mean potentially lower returns",
            survey_constants.USER_E_WEIGHT: "I prefer to invest in companies that are actively working toward reducing their environmental impact (e.g., zero-waste goals, carbon neutrality).",
            survey_constants.USER_S_WEIGHT: "I believe companies should be held accountable for their social impact, including labor practices and community engagement.",
            survey_constants.USER_G_WEIGHT: "I prefer to invest in companies that have a transparent board structure and clear governance policies",
            survey_constants.USER_CONTROVERSY_THRESHOLD: "I would prefer to avoid investments in companies involved in controversial sectors (e.g., fossil fuels, tobacco, weapons)",
            survey_constants.USER_GREEN_INDUSTRY_THRESHOLD: "I am interested in investments in industries that promote sustainability, such as renewable energy, clean technology, and sustainable agriculture",
            survey_constants.USER_ESG_SCORE_THRESHOLD: "I am comfortable investing in companies with strong sustainability scores, even if they operate in traditionally 'non-green' industries (e.g., sustainable mining or oil)",
        }

        for question_key, question in questions.items():
            # Create all the questions, store each answer in "answers" dictionary, using the key associated with each question
            answers[question_key] = st.select_slider(label=question, options=survey_options)

        sectors_available = ["Basic Materials", "Industrials", "Communication Services", "Healthcare",
                             "Real Estate", "Technology", "Energy", "Utilities", "Financial Services",
                             "Consumer Defensive", "Consumer Cyclical"]
        answers[survey_constants.USER_SECTORS] = st.multiselect(label="What are your preferred sector(s)?",
                                                                options=sectors_available)

        submitted = st.form_submit_button("Submit (double click)")
        if submitted:
            for k, v in answers.items():
                # Map answers "strongly disagree" .. "strongly agree" to numerical value, skip the two questions that have different answer type
                if k not in [survey_constants.USER_SECTORS, survey_constants.USER_RISK_TOLERANCE]:
                    answers[k] = survey_options.index(v) + 1  # map to values 1-5

            # store the answers in session_state, so it is available in other pages
            st.session_state.answers = {"name": name, "survey_answers": answers}
