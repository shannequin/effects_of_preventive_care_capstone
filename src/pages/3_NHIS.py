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

def populate_sidebar() -> str:
    """
    Populate the sidebar with survey options.
    """

    st.sidebar.title('Surveys')

    selected_survey = st.sidebar.selectbox(
        label='Select a survey:',
        options=sorted(SURVEY_TABLE_MAP.keys()),
        index=None,
        placeholder='None'
    )

    return selected_survey

def populate_body(selected_survey) -> None:
    """
    Populate the body with the selected survey's data.
    """
    if not selected_survey:
        st.info("Please select a survey from the sidebar.")
    else:
        st.subheader(selected_survey)

        table_name = SURVEY_TABLE_MAP.get(selected_survey) #TODO: Change to table title field

        st.write(f"Displaying data from table: {table_name}")

def main() -> None:
    """
    Display the National Health Interview Survey page.
    """
    st.title("National Health Interview Survey", text_alignment="center")

    rainbow_divider()

    selected_survey = populate_sidebar()

    populate_body(selected_survey)

if __name__ == "__main__":
    main()