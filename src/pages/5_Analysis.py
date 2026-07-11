import streamlit as st

from analysis.analysis import analysis
from config.analysis_config import ANALYSIS_CONFIG
from utils.custom_visuals import rainbow_divider


def populate_sidebar() -> tuple[str, str]:
    """
    Populate the sidebar with analysis options.
    """
    # Initialize the variable
    selected_analysis = None

    st.sidebar.title('Analysis')

    selected_care = st.sidebar.selectbox(
        label='Select care:',
        options=list(ANALYSIS_CONFIG.keys()),
        index=None,
        placeholder='None'
    )

    if selected_care:
        selected_analysis = st.sidebar.selectbox(
            label='Select analysis:',
            options=list(ANALYSIS_CONFIG[selected_care]['Analysis'].keys()),
            index=None,
            placeholder='None'
        )

    return selected_care, selected_analysis

def populate_body(selected_care: str, selected_analysis: str) -> None:
    """
    Populate main body of the page.
    """
    if not selected_care:
        st.info("Please select care from the sidebar.")

    elif not selected_analysis:
        st.info("Please select analysis from the sidebar.")

    else:
        # Get the analysis configuration for the selected care and analysis
        care_config = ANALYSIS_CONFIG[selected_care]

        st.header(care_config['Analysis'][selected_analysis]['header'])
        st.text(care_config['Description'])

        analysis(
            selected_care,
            selected_analysis
        )

def main() -> None:
    """
    Display the Analysis page.
    """
    st.title("BRFSS Data Analysis", text_alignment="center")

    rainbow_divider()

    selected_care, selected_analysis = populate_sidebar()

    populate_body(selected_care, selected_analysis)

if __name__ == '__main__':
    main()