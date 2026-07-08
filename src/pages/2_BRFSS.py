import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


CONN = st.connection("postgresql", type="sql")

def populate_sidebar() -> tuple['DataFrame', str]:
    """
    Populate the sidebar with survey questions from the BRFSS dataset.
    """
    st.sidebar.title('Survey Questions')

    question_query = f"""SELECT *
                        FROM staging.behavioral_risk_factor_surveillance_system_questions;"""

    brfss_question_df = CONN.query(sql=question_query)

    brfss_question_df = brfss_question_df[brfss_question_df['Question'] != 'Interview Date']

    selected_question = st.sidebar.selectbox(
        label='Select a question:',
        options=brfss_question_df['Question'].tolist(),
        index=None,
        placeholder='None'
    )

    return brfss_question_df, selected_question

def populate_body(brfss_question_df, selected_question) -> None:
    """
    Populate the main body of the page with the selected survey question's results.
    """
    if not selected_question:
        st.text("Please select a question from the sidebar.")

    else:
        column_name = brfss_question_df[brfss_question_df['Question'] == selected_question]['Field'].values[0]

        st.subheader(selected_question)

        results_query = f"""SELECT {column_name}, COUNT(*)
                            FROM staging.behavioral_risk_factor_surveillance_system
                            GROUP BY {column_name};"""

        brfss_response_df = CONN.query(sql=results_query)

        brfss_response_df = brfss_response_df.dropna(subset=[column_name, 'count'])

        fig, ax = plt.subplots()
        fig.set_size_inches(fig.get_size_inches()[0], fig.get_size_inches()[1] * 2)

        colors = plt.cm.rainbow(np.linspace(1, 0, len(brfss_response_df)))
        ax.barh(
            y=brfss_response_df[column_name].sort_values(ascending=False),
            width=brfss_response_df.set_index(column_name).loc[brfss_response_df[column_name].sort_values(ascending=False)]['count'],
            color=colors
        )
        ax.grid(axis='x', which='major', linestyle='--', alpha=0.7)
        ax.set_xlabel('Count')
        ax.set_xlim(0, brfss_response_df['count'].mean() * 3)
        ax.set_yticklabels([label.get_text()[:25] for label in ax.get_yticklabels()])

        st.pyplot(fig)

        st.dataframe(brfss_response_df, hide_index=True)

def main() -> None:
    """
    Display the Behavioral Risk Factor Surveillance System page.
    """

    st.title("Behavioral Risk Factor Surveillance System", text_alignment="center")

    st.markdown(
        "<hr style='border: 0; height: 2px; background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);'>",
        unsafe_allow_html=True
    )

    brfss_question_df, selected_question = populate_sidebar()

    populate_body(brfss_question_df, selected_question)

if __name__ == "__main__":
    main()