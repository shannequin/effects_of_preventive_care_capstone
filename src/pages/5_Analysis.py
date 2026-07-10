import streamlit as st

from analysis.colorectal_analysis import colorectal_insurance_analysis
from utils.custom_visuals import rainbow_divider


def populate_sidebar() -> str:
    """
    Populate the sidebar with analysis options.
    """
    st.sidebar.title('Analysis')

    selected_analysis = st.sidebar.selectbox(
        label='Select analysis:',
        options=['Colorectal Cancer'],
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

    elif analysis == 'Colorectal Cancer':
        st.header('Is the type of primary insurance statistically significant to receiving colorectal cancer screenings?')
        st.text('Colorectal cancer screenings include colonoscopy, sigmoidoscopy, virtual colonoscopy, CT colonography, blood stool test, FIT DNA, or Cologuard test.')

        df, model = colorectal_insurance_analysis()

        st.image("src/figures/colon_odds_ratios.png")

        st.text(model.summary())

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