import pandas as pd
import streamlit as st
import os
import altair as alt

file_path = os.path.join(os.path.dirname(__file__), 'data', 'london_weather.csv')

df = pd.read_csv(
    'london_weather.csv',
    parse_dates=['date'],
    date_format="%Y%m%d"
)

# Filtrowanie danych, aby zachować tylko lata od 2018-2020
df = df[(df['date'].dt.year >= 2018) & (df['date'].dt.year <= 2020)].copy()

# Filtrowanie danych dla poszczególnych lat
df_2018 = df[(df['date'].dt.year == 2018)].copy()
df_2019 = df[(df['date'].dt.year == 2019)].copy()
df_2020 = df[(df['date'].dt.year == 2020)].copy()

df['year'] = pd.to_datetime(df['date']).dt.year

df['day_of_year'] = pd.to_datetime(df['date']).dt.dayofyear

# Wyświetlenie tytułu
st.title('''London weather 2018-2020''')

# Nagłówek
st.header('2020 Summary')

col1, col2, col3 = st.columns(3)

delta_avg_temp = (df[df['date'].dt.year == 2020]['mean_temp'].mean()) - (df[df['date'].dt.year == 2019]['mean_temp'].mean())
delta_min_temp = (df[df['date'].dt.year == 2020]['min_temp'].min()) - (df[df['date'].dt.year == 2019]['min_temp'].min())
delta_max_temp = (df[df['date'].dt.year == 2020]['max_temp'].max()) - (df[df['date'].dt.year == 2019]['max_temp'].max())


with col1:
    st.metric(
    label="Average temperature",
    value=f"{df[df['date'].dt.year == 2020]['mean_temp'].mean():.1f} °C",
    delta=f'{delta_avg_temp:.1f}'
    )

with col2:
    st.metric(
    label="Min temperature",
    value=f"{df[df['date'].dt.year == 2020]['min_temp'].min():.1f} °C",
    delta=f'{delta_min_temp:.1f}'
    )

with col3:
    st.metric(
    label="Max temperature",
    value=f"{df[df['date'].dt.year == 2020]['max_temp'].max():.1f} °C",
    delta=f'{delta_max_temp:.1f}'
    )

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
    label="Average precipitation",
    value=f"{df[df['date'].dt.year == 2020]['precipitation'].mean():.1f} mm"
    )

with col2:
    st.metric(
    label="Max precipitation",
    value=f"{df[df['date'].dt.year == 2020]['precipitation'].max():.1f} mm"
    )

# Wykres liniowy (line chart) dla średniej temperatury
chart = alt.Chart(df).mark_line().encode(
    x=alt.X('day_of_year', axis=alt.Axis(title='Day of the year'),
    scale=alt.Scale(domain=[1, 365])),
    y=alt.Y('mean_temp', title='Average temperature (°C)'),
    color='year:N',
    tooltip=[
        alt.Tooltip('date', title='Data'),
        alt.Tooltip('mean_temp', title='Temperature', format='.2f')
    ]
).properties(
    title='Average temperature trend in London'
).interactive()

# Wyświetl wykres w Streamlit
st.altair_chart(chart, use_container_width=True)