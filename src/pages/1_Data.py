import streamlit as st

from utils.custom_visuals import rainbow_divider


def main() -> None:
    """
    Display the Data page.
    """
    st.title('Information about the Data', text_alignment='center')

    rainbow_divider()

    # BRFSS Data
    st.text(
        'The Behavioral Risk Factor Surveillance System (BRFSS) is the largest continuously conducted health survey in the '
        'United States, collecting self-reported data on health behaviors, chronic conditions, and use of preventive health '
        'services from adults in all 50 states, the District of Columbia, and participating U.S. territories.'
    )

    # NHIS Data
    st.text(
        'The National Health Interview Survey (NHIS) is a major source of information on the health of the U.S. population, '
        'collecting data through personal household interviews on a broad range of health topics, including preventive care, '
        'chronic conditions, and health behaviors.'
    )

    # CDC Data
    st.text(
        'The Centers for Disease Control and Prevention (CDC) provides a wide range of health data, including statistics on '
        'preventive health services, vaccination coverage, and disease incidence, which are used to inform public health '
        'policies and programs.'
    )

    st.header('Challenges with the Data')
    st.text(
        'Sourcing datasets: Most of the available data is from studies and reports that are already cleaned and aggregated '
        'which limits the ability to perform custom analysis.'
    )
    st.text(
        'Loading the database: The BRFSS dataset in particular required most of the effort due to the rows being formatted as '
        'without delimiters. A custom script was needed to map the character position and length for each column per row.'
    )

if __name__ == '__main__':
    main()