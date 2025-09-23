import pandas as pd
import streamlit as st
import os
import altair as alt


#Wczytanie danych z pliku CSV
file_path = os.path.join(os.path.dirname(__file__), 'data', 'london_weather.csv')

df = pd.read_csv(
    'london_weather.csv',
    parse_dates=['date'],
    date_format="%Y%m%d"
)

# Filtrowanie danych, aby zachować tylko lata od 2018-2020
df = df[(df['date'].dt.year >= 2018) & (df['date'].dt.year <= 2020)].copy()

# Dodanie kolumny z rokiem
df['year'] = pd.to_datetime(df['date']).dt.year

# Dodanie kolumny z miesiącem
df['month'] = df['date'].dt.month

# Dodanie kolumny z dniem w roku
df['day_of_year'] = pd.to_datetime(df['date']).dt.dayofyear

# Wyświetlenie tytułu
st.title('''London weather 2018-2020''')

# Nagłówek
st.header('2020 Summary')

# Utworzenie trzech kolumn do wyświetlenia metryk
col1, col2, col3 = st.columns(3)

# Obliczenie różnicy między latami 2019 i 2020 dla średniej, min i max temperatury
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

st.write("*Compare to 2019")

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

# Lata dostępne do wyboru
all_years = sorted(df['year'].unique())

# Utorzenie pola do wyboru lat
selected_years = st.multiselect(
    'Select year to display',
    options=all_years,
    default=[2020],
    key='year_selection')

# Filtrowanie danych na podstawie wybranych lat
chart_filtered_df = df[df['year'].isin(selected_years)]

# Tworzenie wykresu w Altair na podstawie wybranych lat
chart = alt.Chart(chart_filtered_df).mark_line().encode(
    x=alt.X('day_of_year', axis=alt.Axis(title='Day of the year'),
    scale=alt.Scale(domain=[1, 365])),
    y=alt.Y('mean_temp', title='Temperature (°C)'),
    color='year:N',
    tooltip=[
        alt.Tooltip('date', title='Data'),
        alt.Tooltip('mean_temp', title='Temperature', format='.2f'),
        alt.Tooltip('year', title='Year')
    ]
).properties(
    title='Daily mean temperature in London (2018-2020)'
).interactive()

# Wyświetl wykres w Streamlit
st.altair_chart(chart, use_container_width=True)

# Przygotowanie danych do wykresu opadów
# Grupowanie danych według miesiecy i lat oraz sumowanie opadów
precipitation_df = df.groupby(['year', 'month'])['precipitation'].sum().reset_index()

# Dodanie nazwy miesiąca
precipitation_df['month_name'] = pd.to_datetime(precipitation_df['month'], format='%m').dt.strftime('%B')

# Tworzenie wykresu słupkowego opadów w Altair
precipitation_chart = alt.Chart(precipitation_df).mark_bar().encode(
    x=alt.X('month_name', sort=None, title='Month'),
    y=alt.Y('precipitation', title='Total Precipitation (mm)'),
    color='year:N',
    tooltip=[
        alt.Tooltip('year', title='Year'),
        alt.Tooltip('month_name', title='Month'),
        alt.Tooltip('precipitation', title='Total Precipitation (mm)', format='.2f')
    ]
).properties(
    title='Total monthly precipitation in London (2018-2020)'
).interactive()

# Wyświetlenie wykresu opadów w Streamlit
st.altair_chart(precipitation_chart, use_container_width=True)

# Wyświetlenie szczegółowych danych w tabeli
st.write('Raw data')
st.dataframe(df)