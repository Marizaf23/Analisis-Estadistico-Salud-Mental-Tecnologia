import pandas as pd
import numpy  as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly as px
import streamlit as st
import requests
from io import StringIO

# Título de la aplicación
st.title("Problemáticas y Estigmas de las Enfermedades Mentales en la Industria Tecnológica Estadounidense 2016-2019")

# Crea un menú de pestañas
tab1, tab2 = st.tabs(["Introducción", "Datos"])

# Contenido de la página 1
with tab1:
    st.header("Introducción")
    st.write("Información de la Data Suministrada.")

# Contenido de la página 2
with tab2:
    st.header("Visualización de los Datos")
    st.write("Información de la Data Suministrada.")

    @st.cache
    def load_csv_from_github(url):
        response = requests.get(url)
        if response.status_code == 200:
            return pd.read_csv(StringIO(response.text))
        else:
            st.error("Failed to load data from GitHub.")
            return None

    # URLs of CSV files in GitHub repository
    urls = {
        '2016': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/f9543f9242e7869a95a82e55fb2d1289971a9c40/CSV/Investigacion1.csv',
        '2017': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/f9543f9242e7869a95a82e55fb2d1289971a9c40/CSV/Investigacion2.csv',
        '2018': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/f9543f9242e7869a95a82e55fb2d1289971a9c40/CSV/Investigacion3.csv',
        '2019': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/f9543f9242e7869a95a82e55fb2d1289971a9c40/CSV/Investigacion4.csv'
    }

    # Load CSV files from GitHub
    df_2016 = load_csv_from_github(urls['2016'])
    df_2017 = load_csv_from_github(urls['2017'])
    df_2018 = load_csv_from_github(urls['2018'])
    df_2019 = load_csv_from_github(urls['2019'])

    # Crea un selectbox con las opciones
    option = st.selectbox('Año de Encuesta:', ['2016', '2017', '2018', '2019'])

    # Muestra el DataFrame correspondiente según la opción seleccionada
    if option == '2016':
        st.dataframe(df_2016)
    elif option == '2017':
        st.dataframe(df_2017)
    elif option == '2018':
        st.dataframe(df_2018)
    elif option == '2019':
        st.dataframe(df_2019)