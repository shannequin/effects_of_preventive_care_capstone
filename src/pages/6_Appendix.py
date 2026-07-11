import streamlit as st

from utils.custom_visuals import rainbow_divider

def main() -> None:
    st.title('Appendix', text_alignment='center')

    rainbow_divider()

    st.header('Sources')

    st.text('https://www.cdc.gov/brfss/index.html')
    st.text('https://odphp.health.gov/healthypeople/objectives-and-data/browse-objectives/cancer')
    st.text('https://www.cdc.gov/united-states-cancer-statistics/public-use/index.html')

if __name__ == '__main__':
    main()