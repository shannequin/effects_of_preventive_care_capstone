"""
WIP
"""

import streamlit as st

from utils.custom_visuals import rainbow_divider


CONN = st.connection("postgresql", type="sql")

def populate_sidebar() -> str:
    """
    Populate the sidebar with study options.
    """
    st.sidebar.title('Studies')

    selected_study = st.sidebar.selectbox(
        label='Select a study:',
        options=['TBD'],
        index=None,
        placeholder='None'
    )

    return selected_study

def populate_body(selected_study: str) -> None:
    """
    Populate the body with the selected study's data.
    """
    st.header('TBD')
    
    if not selected_study:
        st.info('Please select a study from the sidebar.')

    else:
        st.info('TBD')

def main() -> None:
    """
    Display the Center for Disease Control and Prevention page.
    """
    st.title('Center for Disease Control and Prevention', text_alignment='center')

    rainbow_divider()

    selected_study = populate_sidebar()

    populate_body(selected_study)

if __name__ == '__main__':
    main()