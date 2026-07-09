import streamlit as st

from utils.custom_visuals import rainbow_divider

def main() -> None:
    st.title('Appendix', text_alignment='center')

    rainbow_divider()

    st.header('Sources')

    st.text('')
    
if __name__ == '__main__':
    main()