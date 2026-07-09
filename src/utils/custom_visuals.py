import streamlit as st


def rainbow_divider(height: int = 2) -> None:
    st.html(f"""
    <hr style="
        border: 0;
        height: {height}px;
        background: linear-gradient(
            to right,
            red,
            orange,
            yellow,
            green,
            blue,
            indigo,
            violet
        );
        margin: 1rem 0;
    ">
    """)
