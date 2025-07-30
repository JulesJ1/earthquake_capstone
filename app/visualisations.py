import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from folium.plugins import HeatMap
import plotly.express as px


def pick_colour(magnitude):
    if magnitude < 1.5:
        return '#40ad00'
    if magnitude < 3:
        return '#f2d600'
    elif magnitude < 6:
        return 'orange'
    return 'red'


def additional_transformations():
    if len(st.session_state['filtered_data']) > 1:
        st.session_state['filtered_data']['normalised_mag'] = (
                (st.session_state['filtered_data']['magnitude'] -
                 st.session_state['filtered_data']['magnitude'].min()) /
                (st.session_state['filtered_data']['magnitude'].max() -
                 st.session_state['filtered_data']['magnitude'].min())
            )
    else:
        st.session_state['filtered_data']['normalised_mag'] = 2

    st.session_state['filtered_data'][
        'colour'] = st.session_state['filtered_data'][
        'magnitude'].transform(pick_colour)


def create_map(data):

    map = folium.Map(location=[41, 35], zoom_start=2)

    for i, row in data.iterrows():
        folium.CircleMarker(
            [row.latitude, row.longitude],
            radius=5+(10*row.normalised_mag),
            tooltip=row.id,
            color=row.colour,
            fill=True,
            fill_opacity=0.5,
            weight=2
        ).add_to(map)
    return map


def display_map(map):
    map_data = st_folium(map, use_container_width=True)
    st.session_state.coordinates = map_data['last_object_clicked']
    st.session_state.info = map_data['last_object_clicked_tooltip']


def heatmap(data):
    map = folium.Map(location=[41, 35], zoom_start=2)
    heat_data = data[
        ['latitude', 'longitude', 'magnitude']
        ].values.tolist()
    HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(map)
    st_folium(map, use_container_width=True)


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
        st.markdown(f'##### Occured At: {info['time'].item()}')
        st.divider()
        st.markdown(f'##### Region: {info['location'].item()}')
        st.divider()
        st.markdown(f'##### Event Type: {info['type'].item()}')
    """
    else:
        st.caption(
                'Select an event from the map to view some information!'
            )
    """


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

        st.subheader('Number Of Earthquakes At Each Hour')
        st.bar_chart(
            df2,
            x='hour',
            y='counted',
            y_label='number of earthquakes'
            )

    with col2:
        st.subheader('Depth vs. Magnitude')
        st.line_chart(
            st.session_state['filtered_data'],
            x='depth',
            y='magnitude',
            x_label='depth (km)',
            color='#008f2b'
            )


def metrics(data):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Earthquakes Today",
                  value=len(data))
    with col2:
        st.metric(label="Highest Magnitude",
                  value=max(data['magnitude']))
    with col3:
        st.metric(label="Lowest Magnitude",
                  value=min(data['magnitude']))


def graphs(data):

    series = data['magnitude'].groupby(
            data['time'].dt.hour
            ).count()

    series = series.reindex(range(23), fill_value=0)
    df2 = pd.DataFrame({
            'hour': series.index.map(str)+":00",
            'counted': series.values}
            )

    st.subheader('Number Of Earthquakes At Each Hour')
    st.bar_chart(
            df2,
            x='hour',
            y='counted',
            y_label='number of earthquakes'
            )

    col1, col2 = st.columns(2)
    with col1:

        fig = px.histogram(
            data,
            x="location",
            title="locations"

        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.histogram(
            data,
            x="magnitude",
            nbins=20,  # adjust as needed
            title="Magnitude Histogram"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader('Depth vs. Magnitude')
    st.scatter_chart(
        data,
        x='depth',
        y='magnitude',
        x_label='depth (km)',
        color='#008f2b'
        )


def display_visualisations():
    additional_transformations()
    tab1, tab2 = st.tabs(["USGS Data", "ESMC Data"])
    with tab1:
        data1 = st.session_state['filtered_data'].loc[
            st.session_state['filtered_data']['apisource'] == 'USGS'
            ]

        map = create_map(data1)

        col1, col2 = st.columns([0.7, 0.3], gap='medium')
        with col1.container():
            metrics(data1)

            if st.session_state['heatmap']:
                heatmap(data1)
            else:
                display_map(map)

        with col2.container():
            display_info()

        graphs(data1)

    with tab2:
        data = st.session_state['filtered_data'].loc[
            st.session_state['filtered_data']['apisource'] == 'esmc'
            ]

        map = create_map(data)

        col1, col2 = st.columns([0.7, 0.3], gap='medium')
        with col1.container():
            metrics(data)

            if st.session_state['heatmap']:
                heatmap(data)
            else:
                display_map(map)

        with col2.container():
            display_info()

        graphs(data)
