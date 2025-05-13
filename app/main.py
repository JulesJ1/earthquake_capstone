import streamlit as st
from filters import apply_filters, fetch_data
from visualisations import display_visualisations


def main():
    st.set_page_config(
        page_title="Earthquake Dashboard",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="auto",
    )

    if 'display_name' not in st.session_state:
        st.session_state.display_name = None

    if 'data' not in st.session_state:
        st.session_state['data'] = fetch_data()

    st.title('Earthquake visualiser')

    apply_filters()

    display_visualisations()


if __name__ == "__main__":
    main()
