import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from utils.custom_visuals import rainbow_divider


CONN = st.connection("postgresql", type="sql")

def populate_sidebar() -> tuple[pd.DataFrame, str]:
    """
    Populate the sidebar with survey questions from the BRFSS dataset.
    """
    selected_question = None
    question_df = pd.DataFrame()

    st.sidebar.title('Survey Questions')

    query = f"""SELECT *
                FROM staging.behavioral_risk_factor_surveillance_system_questions;"""

    question_df = CONN.query(sql=query)

    question_df = question_df[question_df['Question'] != 'Interview Date']

    selected_question = st.sidebar.selectbox(
        label='Select a question:',
        options=question_df['Question'].tolist(),
        index=None,
        placeholder='None'
    )

    return question_df, selected_question

def populate_body(question_df: pd.DataFrame, question: str) -> None:
    """
    Populate the main body of the page with the selected survey question's results.
    """
    if not question:
        st.info("Please select a question from the sidebar.")

    else:
        column_name = question_df[question_df['Question'] == question]['Field'].values[0]

        st.subheader(question, text_alignment='center')

        query = f"""SELECT {column_name}, COUNT(*)
                    FROM staging.behavioral_risk_factor_surveillance_system
                    GROUP BY {column_name};"""

        survey_df = CONN.query(sql=query)

        survey_df = survey_df.dropna(subset=[column_name, 'count'])

        fig, ax = plt.subplots()
        fig.set_size_inches(fig.get_size_inches()[0], fig.get_size_inches()[1] * 2)

        colors = plt.cm.rainbow(np.linspace(1, 0, len(survey_df)))
        ax.barh(
            y=survey_df[column_name].sort_values(ascending=False),
            width=survey_df.set_index(column_name).loc[survey_df[column_name].sort_values(ascending=False)]['count'],
            color=colors
        )
        ax.grid(axis='x', which='major', linestyle='--', alpha=0.7)
        ax.set_xlabel('Count')
        ax.set_xlim(0, survey_df['count'].mean() * 3)
        ax.set_yticklabels([label.get_text()[:25] for label in ax.get_yticklabels()])

        st.pyplot(fig)

        st.dataframe(survey_df, hide_index=True)

def main() -> None:
    """
    Display the Behavioral Risk Factor Surveillance System page.
    """

    st.title("Behavioral Risk Factor Surveillance System", text_alignment="center")

    rainbow_divider()

    question_df, question = populate_sidebar()

    populate_body(question_df, question)

if __name__ == "__main__":
    main()