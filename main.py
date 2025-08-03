import streamlit as st
from app.filters import apply_filters, fetch_data
from app.visualisations import display_visualisations
from utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)


def main():
    st.set_page_config(
        page_title="Earthquake Dashboard",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="auto",
    )

    with open('style.css') as f:
        st.write(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if 'data' not in st.session_state:
        st.session_state['heatmap'] = False
        st.session_state['data'] = fetch_data()

    if 'filtered_Data' not in st.session_state:
        st.session_state['filtered_data'] = st.session_state['data'].copy()

    st.title('Earthquake Dashboard')

    apply_filters()

    display_visualisations()


if __name__ == "__main__":
    main()
