import streamlit as st
from filters import apply_filters, fetch_data
from visualisations import display_visualisations
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

    if 'data' not in st.session_state:
        st.session_state['data'] = fetch_data()

    if 'filtered_Data' not in st.session_state:
        st.session_state['filtered_data'] = st.session_state['data'].copy()

    st.title('Earthquake visualiser')

    apply_filters()

    display_visualisations()


if __name__ == "__main__":
    main()
