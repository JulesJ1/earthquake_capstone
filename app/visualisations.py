import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd


def pick_colour(magnitude):
    if magnitude < 2.5:
        return '#fae22b'
    elif magnitude < 6:
        return 'orange'
    return 'red'


def additional_transformations(dataframe: pd.DataFrame):
    dataframe['normalised_mag'] = ((dataframe['magnitude'] -
                                    dataframe['magnitude'].min()) /
                                   (dataframe['magnitude'].max() -
                                    dataframe['magnitude'].min())
                                   )
    dataframe['colour'] = dataframe['magnitude'].transform(pick_colour)
    return dataframe


def create_map():
    data_to_display = additional_transformations(st.session_state['data'])
    map = folium.Map(location=[41, 35], zoom_start=2, height='40%')
    for i, row in data_to_display.iterrows():
        folium.CircleMarker(
            [row.latitude, row.longitude],
            radius=5+(10*row.normalised_mag),
            tooltip=row.id, color=row.colour,
            fill=True,
            fill_opacity=0.5
        ).add_to(map)
    return map


def display_map(map):
    map_data = st_folium(map, use_container_width=True)
    st.session_state.coordinates = map_data['last_object_clicked']
    st.session_state.info = map_data['last_object_clicked_tooltip']


def display_info():
    st.subheader('Earchquake Info:')

    if st.session_state.coordinates is not None:
        tooltip_info = st.session_state.info
        info = st.session_state['data'][
                st.session_state['data']['id']==str(tooltip_info)
            ]

        st.write(f'Occured at: {info['time'].item()}')
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.metric('latitude', info['latitude'])
            st.metric('magnitude', info['magnitude'].item())
        with col2:
            st.metric('longitude', info['longitude'])
            st.metric('depth km', info['depth'].item())
        st.write(f'Region: {info['location'].item()}')
        st.write(f'Event Type: {info['type'].item()}')
    else:
        st.caption(
                'Select an event from the map to view some cool information!'
            )


def display_visualisations():
    tab1, tab2 = st.tabs(["View Map", "Data Analyser"])
    with tab1:
        map = create_map()
        col1, col2 = st.columns([0.7, 0.3], gap='medium')
        with col1.container():
            min_time = st.session_state['data']['time'].min()
            max_time = st.session_state['data']['time'].max()
            st.subheader(f'Data between {min_time} and {max_time}')
            display_map(map)

        with col2.container():
            display_info()

    with tab2:
        st.dataframe(st.session_state['data'][['time',
                                               'id',
                                               'magnitude',
                                               'longitude',
                                               'latitude',
                                               'location',
                                               'type',
                                               'depth']])
        #st.session_state['data']['hour'] = st.session_state['data']['time'].dt.hour
        #st.session_state['data']['count'] = st.session_state['data'].groupby(['hour'])['hour'].count()
        #print(df_todisplay)
        #print(df_todisplay.index)
        #df_todisplay.index = pd.to_datetime(df_todisplay.index)
        #st.line_chart(st.session_state['data'],x = 'hour',y='magnitude')
        #st.line_chart(x = None,y = st.session_state['data']['count'])

    
