import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from utils.custom_visuals import rainbow_divider


CONN = st.connection("postgresql", type="sql")

def populate_sidebar() -> str:
    """
    Populate the sidebar with analysis options.
    """
    st.sidebar.title('Analysis')

    selected_analysis = st.sidebar.selectbox(
        label='Select analysis:',
        options=['Colon Cancer'],
        index=None,
        placeholder='None'
    )

    return selected_analysis

def populate_body(analysis):
    """
    Populate main body of the page.
    """
    if not analysis:
        st.info("Please select analysis from the sidebar.")

    elif analysis == 'Colon Cancer':
        st.text('Is primary insurance type statistically significant to receiving preventive care for colon cancer?')
        st.image("src/figures/colon_odds_ratios.png")

def main() -> None:
    """
    Display the Analysis page.
    """

    st.title("Analysis", text_alignment="center")

    rainbow_divider()

    analysis = populate_sidebar()

    populate_body(analysis)


if __name__ == '__main__':
    main()