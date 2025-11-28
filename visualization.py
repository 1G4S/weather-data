
import altair
import streamlit as st
import pandas as pd


df = pd.read_json('./gold_data/weather-data.json')
st.set_page_config(layout="wide")
df['timestamp'] = pd.to_datetime(df['timestamp'])
min_ts = df['timestamp'].min()
max_ts = df['timestamp'].max()
min_date = min_ts.to_pydatetime()
max_date = max_ts.to_pydatetime()

transformed_dates = (min_date, max_date)
with st.container():
    st.header("Dane pogodowe")

with st.container(border=True):
    col5, col6 = st.columns(2)
    with col5:
        first_filter = df
        city = st.multiselect('Wybierz miasto', options=list(first_filter['city'].unique()),
                              default=list(first_filter['city'].unique()))
        second_filter = first_filter[first_filter['city'].isin(city)]
    with col6:
        start_time, end_time = st.slider('Wybierz zakres dat', min_value=min_date, max_value=max_date, value=transformed_dates,
                                         format="YYYY-MM-DD")
        mask = (second_filter['timestamp'] >= start_time) & (second_filter['timestamp'] < end_time)
        third_filter = second_filter.loc[mask]

with st.container(border=False):
    # result = st.radio('Select day or nights', options=['Day', 'Night'])
    # if result == 'Day':
    #     first_filter = df[
    #         (df['timestamp'].dt.hour >= 6) &
    #         (df['timestamp'].dt.hour <= 18)
    #     ]
    # else:
    #     first_filter = df[
    #         (df['timestamp'].dt.hour >= 18) |
    #         (df['timestamp'].dt.hour <= 6)
    #     ]

    col7, col8, col9, col10 = st.columns(4, vertical_alignment='center', border=True)
    max_temp = third_filter['temperature'].max()
    min_temp = third_filter['temperature'].min()
    max_humidity = third_filter['humidity'].max()
    min_humidity = third_filter['humidity'].min()
    max_pm25 = third_filter['PM25'].max()
    min_pm25 = third_filter['PM25'].min()
    max_pm10 = third_filter['PM10'].max()
    min_pm10 = third_filter['PM10'].min()
    with col7:
        st.metric('Najwyższa temperatura', f'{max_temp} °C')
        st.metric('Najniższa temperatura', f'{min_temp} °C')

    with col8:
        st.metric('Najwyższa wilgotność', f'{max_humidity} %')

        st.metric('Najniższa wilgotność', f'{min_humidity} %')

    with col9:
        st.metric('Najwyższe stężenie PM2.5', f'{max_pm25} µg/m³')
        st.metric('Najniższe stężenie PM2.5', f'{min_pm25} µg/m³')

    with col10:
        st.metric('Najwyższe stężenie PM10', f'{max_pm10} µg/m³')
        st.metric('Najniższe stężenie PM10', f'{min_pm10} µg/m³')

with st.container():
    col3, col4 = st.columns(2, border=True)
    with col3:
        chart3 = altair.Chart(third_filter, title="Temperatura").mark_line(
        ).encode(x=altair.X('timestamp', axis=altair.Axis(title='Czas [h]')),
                 y=altair.Y('temperature', axis=altair.Axis(title='Temperatura [°C]')),
                 color=altair.Color('city', title='Miasto'))
        st.altair_chart(chart3)
    with col4:
        chart4 = altair.Chart(third_filter, title="Wilgotność").mark_line(
        ).encode(x=altair.X('timestamp', axis=altair.Axis(title='Czas [h]')),
                 y=altair.Y('humidity', axis=altair.Axis(title='Wilgotność [%]')),
                 color=altair.Color('city', title='Miasto'))
        st.altair_chart(chart4)

with st.container():
    col1, col2 = st.columns(2, border=True)
    with col1:
        chart1 = altair.Chart(third_filter, title="PM2.5 w porównaniu z normą").mark_line(
        ).encode(x=altair.X('timestamp', axis=altair.Axis(title='Czas [h]')),
                 y=altair.Y('PM25', axis=altair.Axis(title='Stężenie PM2.5 [µg/m³]')),
                 color=altair.Color('city', title='Miasto'))

        rule_1 = (
            altair.Chart(third_filter)
            .mark_line(color='red', strokeDash=[5, 5])
            .encode(x='timestamp', y='PM25_norm')
        )
        st.altair_chart(chart1 + rule_1)

    with col2:
        chart2 = altair.Chart(third_filter, title='PM10 w porównaniu z normą').mark_line(
        ).encode(x=altair.X('timestamp', axis=altair.Axis(title='Czas [h]')),
                 y=altair.Y('PM10', axis=altair.Axis(title='Stężenie PM10 [µg/m³]')),
                 color=altair.Color('city', title='Miasto'))

        rule_2 = (
            altair.Chart(third_filter)
            .mark_line(color='red', strokeDash=[5, 5])
            .encode(x='timestamp', y='PM10_norm')
        )
        st.altair_chart(chart2 + rule_2)
