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


def display_info(current_data):
    st.divider()
    st.subheader('Earthquake Information')

    if st.session_state.coordinates is not None:
        tooltip_info = st.session_state.info
        info = current_data[
                current_data['id'] == str(tooltip_info)
            ]

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.metric('latitude', round(info['latitude'], 2))
            st.divider()
            st.metric('magnitude', info['magnitude'].item())
            st.divider()
        with col2:
            st.metric('longitude', round(info['longitude'], 2))
            st.divider()
            st.metric('depth km', info['depth'].item())
            st.divider()
        st.markdown(f'##### Occured At: {info['time'].item()}')
        st.divider()
        st.markdown(f'##### Region: {info['location'].item()}')
        # st.divider()
        # st.markdown(f'##### Event Type: {info['type'].item()}')

    else:
        st.caption(
                'Select an event from the map to view some information!'
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
        st.metric(label="Earthquake Count",
                  value=len(data))
    with col2:
        st.metric(label="Highest Magnitude",
                  value=max(data['magnitude']))
    with col3:
        st.metric(label="Lowest Magnitude",
                  value=min(data['magnitude']))


def graphs(data):

    hour_series = data['time'].dt.hour

    counts = hour_series.value_counts().sort_index()

    counts = counts.reindex(range(24), fill_value=0)

    df = pd.DataFrame({
        'hour': [f"{h:02d}:00" for h in counts.index],
        'count': counts.values
    })
    st.subheader('Number Of Earthquakes At Each Hour')
    st.bar_chart(df, x='hour', y='count', y_label='number of earthquakes')

    col1, col2 = st.columns(2)
    with col1:

        fig = px.histogram(
            data,
            x="location",
            title="Number Of Earthquakes At Each Location"

        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.histogram(
            data,
            x="magnitude",
            nbins=20,
            title="Magnitude Histogram",
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
    """
    fig = px.scatter(
        data,
        x='depth',
        y='magnitude',
    )
    st.plotly_chart(fig, use_container_width=True)
    """


def filter_magnitude(data):
    st.sidebar.slider(
        label='filter minimum magnitude',
        min_value=0.0,
        max_value=max(data['magnitude']),
        key='mag_filter'
        )


def filter_type(options):
    st.sidebar.pills(
        'Type',
        options,
        selection_mode='single',
        default=options[0],
        key='type_filter'
        )


def call_select_filters(data):
    options = data['type'].unique()
    filter_type(options)
    filter_magnitude(data)

    check_if_empty = data[
        (data['magnitude'] >= st.session_state.mag_filter)
        & (data['type'] ==
           str(st.session_state.type_filter))
    ]
    if check_if_empty.empty:
        st.badge(
            'No data available for the selected filters, '
            'default data will be displayed instead!',
            icon='❌',
            color='red'
            )
    else:
        data = check_if_empty.copy()


def display_visualisations():
    additional_transformations()
    tab1, tab2 = st.tabs(["USGS Data", "ESMC Data"])
    with tab1:

        if 'mag_filter_usgs' not in st.session_state:
            usgsdata = st.session_state['filtered_data'].loc[
                (st.session_state['filtered_data']['apisource'] == 'USGS')]

        else:
            usgsdata = st.session_state['filtered_data'].loc[
                (st.session_state['filtered_data']['apisource'] == 'USGS')
                & (st.session_state[
                    'filtered_data'
                    ]['magnitude'] >= st.session_state['mag_filter_usgs'])
                ]

        if "location_search_usgs" in st.session_state:
            usgsdata = usgsdata[
                usgsdata['location'].str.contains(
                    st.session_state[
                        'location_search_usgs'
                        ], case=False, na=False)
                ]

        map = create_map(usgsdata)

        col1, col2 = st.columns([0.8, 0.2], gap='medium')
        with col1.container():
            metrics(usgsdata)

            show_heatmap = st.session_state.get('heatmap_usgs', False)
            if show_heatmap:
                heatmap(usgsdata)
            else:
                display_map(map)

        with col2.container():
            # display_info()
            st.subheader("Local Filters")
            st.slider(
                label='filter minimum magnitude',
                min_value=0.0,
                max_value=float(
                    usgsdata['magnitude'].max()
                    ) if not usgsdata.empty else 10.0,
                key='mag_filter_usgs'
            )

            st.toggle("heatmap", key='heatmap_usgs')
            st.text_input("Search by location:", key="location_search_usgs")

            display_info(usgsdata)

        graphs(usgsdata)

    with tab2:

        if 'mag_filter_esmc' not in st.session_state:
            esmcdata = st.session_state['filtered_data'].loc[
                (st.session_state['filtered_data']['apisource'] == 'esmc')]

        else:
            esmcdata = st.session_state['filtered_data'].loc[
                (st.session_state['filtered_data']['apisource'] == 'esmc')
                & (st.session_state[
                    'filtered_data'
                    ]['magnitude'] >= st.session_state['mag_filter_esmc'])
                ]

        if "location_search_esmc" in st.session_state:
            esmcdata = esmcdata[esmcdata[
                'location'
                ].str.contains(
                st.session_state['location_search_esmc'], case=False, na=False
                )]

        map = create_map(esmcdata)

        col1, col2 = st.columns([0.8, 0.2], gap='medium')
        with col1.container():
            metrics(esmcdata)

            show_heatmap = st.session_state.get('heatmap_esmc', False)
            if show_heatmap:
                heatmap(esmcdata)
            else:
                display_map(map)

        with col2.container():
            # display_info()
            st.subheader("Local Filters")
            st.slider(
                label='filter minimum magnitude',
                min_value=0.0,
                max_value=float(esmcdata[
                    'magnitude'].max()) if not esmcdata.empty else 10.0,
                key='mag_filter_esmc'
            )

            st.toggle("heatmap", key='heatmap_esmc')
            st.text_input(
                "Search by location (case-insensitive):",
                key="location_search_esmc")

            display_info(esmcdata)

        graphs(esmcdata)
