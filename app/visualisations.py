import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd


def pick_colour(magnitude):
    if magnitude < 1.5:
        return '#40ad00'
    if magnitude < 3:
        return '#fae22b'
    elif magnitude < 6:
        return 'orange'
    return 'red'


def additional_transformations():
    st.session_state['filtered_data']['normalised_mag'] = (
            (st.session_state['filtered_data']['magnitude'] -
             st.session_state['filtered_data']['magnitude'].min()) /
            (st.session_state['filtered_data']['magnitude'].max() -
             st.session_state['filtered_data']['magnitude'].min())
        )
    st.session_state['filtered_data'][
        'colour'] = st.session_state['filtered_data'][
        'magnitude'].transform(pick_colour)


def create_map():
    additional_transformations()

    map = folium.Map(location=[41, 35], zoom_start=2, height='40%')

    for i, row in st.session_state['filtered_data'].iterrows():
        folium.CircleMarker(
            [row.latitude, row.longitude],
            radius=5+(10*row.normalised_mag),
            tooltip=row.id,
            color=row.colour,
            fill=True,
            fill_opacity=0.5
        ).add_to(map)
    return map


def display_map(map):
    min_time = st.session_state['filtered_data']['time'].min()
    max_time = st.session_state['filtered_data']['time'].max()
    st.subheader(f'Data between {min_time} and {max_time}')
    map_data = st_folium(map, use_container_width=True)
    st.session_state.coordinates = map_data['last_object_clicked']
    st.session_state.info = map_data['last_object_clicked_tooltip']


def display_info():
    st.subheader('Earthquake Info:')

    if st.session_state.coordinates is not None:
        tooltip_info = st.session_state.info
        info = st.session_state['filtered_data'][
                st.session_state['filtered_data']['id'] == str(tooltip_info)
            ]

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.metric('latitude', info['latitude'])
            st.divider()
            st.metric('magnitude', info['magnitude'].item())
            st.divider()
        with col2:
            st.metric('longitude', info['longitude'])
            st.divider()
            st.metric('depth km', info['depth'].item())
            st.divider()
        st.write(f'Occured At: {info['time'].item()}')
        st.divider()
        st.write(f'Region: {info['location'].item()}')
        st.divider()
        st.write(f'Event Type: {info['type'].item()}')
    else:
        st.caption(
                'Select an event from the map to view some cool information!'
            )


def second_tab():
    st.dataframe(st.session_state['filtered_data'][[
        'time',
        'id',
        'magnitude',
        'longitude',
        'latitude',
        'location',
        'type',
        'depth',
        ]])
    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        series = st.session_state['filtered_data']['magnitude'].groupby(
            st.session_state['filtered_data']['time'].dt.hour
            ).count()
        df2 = pd.DataFrame({
            'hour': series.index.map(str)+":00",
            'counted': series.values}
            )

        st.subheader('Number of Earthquakes at Each Hour')
        st.bar_chart(
            df2,
            x='hour',
            y='counted',
            y_label='number of earthquakes'
            )

    with col2:
        st.subheader('Depth VS Magnitude')
        st.line_chart(
            st.session_state['filtered_data'],
            x='depth',
            y='magnitude',
            x_label='depth (km)',
            color='#008f2b'
            )


def display_visualisations():
    tab1, tab2 = st.tabs(["View Map", "Data Analyser"])
    with tab1:
        map = create_map()
        col1, col2 = st.columns([0.7, 0.3], gap='medium')
        with col1.container():
            display_map(map)

        with col2.container():
            display_info()

    with tab2:
        second_tab()
