import pandas as pd
import re
import streamlit as st

from utils.custom_visuals import rainbow_divider


CONN = st.connection("postgresql", type="sql")

SURVEY_TABLE_MAP = {
    'Colorectal Cancer': 'c07_colorectal_cancer_screenings',
    'Health Insurance': 'ahs01_health_insurance',
    'Female Breast Cancer': 'c05_breast_cancer_screenings',
    'Cervical Cancer': 'c09_cervical_cancer_screenings',
    'Flu Vaccine': 'iid09_flu_vaccinations',
    'Overall Wellbeing': 'ohm01_overall_well_being',
    'Life Expectancy at Birth': 'ohm04_life_expectancy_at_birth',
    'Health Status': 'ohm08_respondent_assessed_health_status'
}

def populate_sidebar() -> tuple[str, str, pd.DataFrame]:
    """
    Populate the sidebar with survey options.
    """
    # Initialize the variables
    selected_demographic = None
    survey_df = pd.DataFrame()

    st.sidebar.title('Surveys')

    survey_options = sorted(SURVEY_TABLE_MAP.keys())
    selected_survey = st.sidebar.selectbox(
        label='Select a survey:',
        options=survey_options,
        index=None,
        placeholder='None'
    )

    if selected_survey:
        table_name = SURVEY_TABLE_MAP.get(selected_survey)

        query = f"""SELECT *
                    FROM staging.{table_name};"""

        survey_df = CONN.query(sql=query)

        # Format the survey name for display
        survey_title = re.sub(r' - OHM.+', '', survey_df['title'].iloc[0])
        st.subheader(survey_title, text_alignment='center')

        # Get the unique demographic groups for the selected survey
        demographic_options = [demographic for demographic in survey_df['demographic_group'].unique()]

        selected_demographic = st.sidebar.selectbox(
            label='Select a demographic:',
            options=sorted(demographic_options),
            index=None,
            placeholder='None'
        )

    return selected_survey, selected_demographic, survey_df

def populate_body(survey: str, demographic: str, survey_df: pd.DataFrame) -> None:
    """
    Populate the body with the selected survey data.
    """
    if not survey:
        st.info('Please select a survey from the sidebar.')

    elif not demographic:
        st.info('Please select a demographic from the sidebar.')

    else:
        # Filter the survey dataframe based on the selected demographic
        survey_df = survey_df.loc[survey_df['demographic_group'] == demographic]

        # Drop unnecessary columns and sort the dataframe for better display
        survey_df = (
            survey_df
            .drop(columns=['code', 'title', 'demographic_group'])
            .sort_values(['population', 'period'])
        )

        # Display the survey dataframe
        st.dataframe(survey_df, hide_index=True)

def main() -> None:
    """
    Display the National Health Interview Survey page.
    """
    st.title('National Health Interview Survey', text_alignment='center')

    rainbow_divider()

    survey, demographic, survey_df = populate_sidebar()

    populate_body(survey, demographic, survey_df)

if __name__ == '__main__':
    main()