import pandas as pd
import numpy  as np
import seaborn as sns
import matplotlib.pyplot as plt
from pywaffle import Waffle
import plotly.graph_objects as go
import streamlit as st
import requests
from io import StringIO
import plotly.express as px
import base64

LOGO_IMAGE1 = "logos/UCV.png"
LOGO_IMAGE2 = "logos/EECA.png"

st.markdown(
    f"""
    <div style="background-color:#80bfff;padding:10px;display:flex;justify-content:space-between;align-items:center;margin-top:-30px;">
        <img src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE1, "rb").read()).decode()}" style="height:40px;margin:30px;">
        <img src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE2, "rb").read()).decode()}" style="height:40px;margin:30px;">
    </div>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_csv_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None

# URLs of CSV files in GitHub repository
urls = {
    '2016': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/95f59adcc416732d98f3b9aa494eb78cadd12c0d/CSV/Investigacion1.csv',
    '2017': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/95f59adcc416732d98f3b9aa494eb78cadd12c0d/CSV/Investigacion2.csv',
    '2018': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/95f59adcc416732d98f3b9aa494eb78cadd12c0d/CSV/Investigacion3.csv',
    '2019': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/95f59adcc416732d98f3b9aa494eb78cadd12c0d/CSV/Investigacion4.csv'
}

# Load CSV files from GitHub
df_2016 = load_csv_from_github(urls['2016'])
df_2017 = load_csv_from_github(urls['2017'])
df_2018 = load_csv_from_github(urls['2018'])
df_2019 = load_csv_from_github(urls['2019'])

st.header("Pregunta 3")
st.subheader('Según la cantidad de empleados en las empresas tecnológicas ¿Cuál tiene la mayor cantidad con enfermedades mentales? ¿Los empleados conocen los beneficios que ofrece la empresa?')

# Crea un selectbox con las opciones
option = st.selectbox('Año de Encuesta:', ['2016', '2017', '2018', '2019'])


if option == '2016':
    df1 = pd.DataFrame([["1-5", "3", "2"], ["6-25", "19", "9"], ["26-100", "50", "25"], ["100-500", "80", "21"], ["500-1000", "85", "8"], ["Más de 1000","85", "44"]],
                   columns = ["Tamaño de la Empresa", "Cantidad de Personas dentro de la Empresa con una Enfermedad mental diagnosticada", "Cantidad de Empleados con una Enfermedad Mental que saben de los Beneficios que ofrece la empresa para ellos"])

    x = ['1-5', '6-25', '26-100', '100-500', "500-1000","Más de 1000" ]

    figp3_1 = go.Figure(data=[
        go.Bar(
            name='Cantidad de Personas con una Enfermedad Mental que conocen los Beneficios que Ofrece la Empresa',
            x=x,
            y=[2, 9, 25, 21, 8, 44],
            marker_color='#b366ff'  # changed color
            ),
        go.Bar(
            name='Cantidad de Personas dentro de la Empresa con una Enfermedad Mental Diagnosticada',
            x=x,
            y=[3, 19, 50, 80, 85, 82],
            marker_color='#cc99ff'  # changed color
            )
        ])

    figp3_1.update_layout(barmode='group', 
                title= "Cantidad de empleados con una Enfermedad Mental y si Conocen de los Beneficios que Ofrece su Empresa (2016)")

    st.plotly_chart(figp3_1, use_container_width=True)

    st.write("""
    <p style="text-align: justify;">
        <ul>
            <li>Empresas de 1-5 empleados: solo 3 empleados tenían una enfermedad mental diagnosticada, y solo 2 de ellos conocen los beneficios que ofrece la empresa para este tipo de casos.</li>
                <li>Empresas de 6-25 empleados: Hay 19 empleados con una enfermedad mental diagnosticada, de esos 9 conocen de los beneficios que ofrece la empresa para ellos.</li>
                    <li>Empresas de 26-100 empleados: Hay 50 personas con una Enfermedad mental Diagnostica y de estos 25 conoce sobre los beneficios que ofrece la empresa.</li>
                    <li>Empresas de 100-500 empleados: Hay 80 personas con una Enfermedad Mental Diagnosticada y 21 personas conocen sobre los beneficios que ofrece la empresa.</li>
                <li>Empresas de 500-1000 empleados: Es la empresa que tiene más empleados con una Enfermedad Mental Diagnosticada con una total 85 empleados, pero apenas solo 8 conocen de los beneficios de la empresa.</li>
            <li>Empresas de más de 1000 empleados: Es la segunda empresa que tiene mas empleados con una enfermedad mental diagnostica con un total de 82 empleados, en esta empresa más de la mitad (44) conocen de los beneficios que ofrece la empresa.</li>
        </ul>
    </p>
    """, unsafe_allow_html=True)

elif option == '2017':
    df2 = pd.DataFrame ([["1-5", "7", "0"], ["6-25", "25", "4"], ["26-100", "46", "3"], ["100-500", "107", "37"], ["500-1000", "36", "11"], ["Más de 1000","88", "46"]],
                   columns = ["Tamaño de la Empresa", "Cantidad de Personas dentro de la Empresa con una Enfermedad mental diagnosticada", "Cantidad de Empleados con una Enfermedad Mental que saben de los Beneficios que ofrece la empresa para ellos"])

    random_x = np.random.randint(1, 101, 100)
    random_y = np.random.randint(1, 101, 100)

    x = ['1-5', '6-25', '26-100', '100-500', "500-1000","Más de 1000" ]

    figp3_2 = go.Figure(data=[
        go.Bar(
            name='Cantidad de Personas con una Enfermedad Mental que conocen los Beneficios que Ofrece la Empresa',
            x=x,
            y=[0, 4, 3, 37, 11, 46],
            marker_color='#b366ff'  # changed color
            ),
        go.Bar(
            name='Cantidad de Personas dentro de la Empresa con una Enfermedad Mental Diagnosticada',
            x=x,
            y=[7, 25, 46, 107, 36, 88],
            marker_color='#cc99ff'  # changed color
            )
        ])

    figp3_2.update_layout(barmode='group', title="Cantidad de empleados con Enfermedad Mental y si Conocen de los Beneficios que Ofrece su Empresa (2017)")

    st.plotly_chart(figp3_2, use_container_width=True)

    st.write("""
    <p style="text-align: justify;">
        <ul>
            <li>Empresas de 1-5 empleados: Hay solo 7 empleados con una enfermedad Mental diagnosticada, y ninguno conoce de los beneficios que la empresa para este tipo de personas.</li>
                <li>Empresas de 6-25 empleados: 25 empleados con enfermedades mentales diagnosticadas. De ellos, solo 4 (16%) conocen los beneficios que ofrece la empresa para este tipo de personas.</li>
                    <li>Empresas de 26-100 empleados: 46 empleados con enfermedades mentales diagnosticadas. De ellos, solo 3 (6%) conocen los beneficios que ofrece la empresa para este tipo de personas.</li>
                    <li>Empresas de 100-500 empleados: La empresa con mayor cantidad de empleados con enfermedades mentales: 107 en total. Sin embargo, menos de la mitad (37, 45%) conocen los beneficios que ofrece la empresa para este tipo de personas.</li>
                <li>Empresas de 500-1000 empleados: 36 empleados con enfermedades mentales diagnosticadas. De ellos, solo 11 (31%) conocen los beneficios que ofrece la empresa para este tipo de personas.</li>
            <li>Empresas de más de 1000 empleados: Segunda empresa con mayor cantidad de empleados con enfermedades mentales: 88 en total. De ellos, 46 (52%) conocen los beneficios que ofrece la empresa para este tipo de personas.</li>
        </ul>
    </p>
    """, unsafe_allow_html=True)

elif option == '2018':
    df3 = pd.DataFrame ([["1-5", "3", "1"], ["6-25", "24", "3"], ["26-100", "30", "8"], ["100-500", "44", "20"], ["500-1000", "31", "10"], ["Más de 1000","71", "35"]],
                   columns = ["Tamaño de la Empresa", "Cantidad de Personas dentro de la Empresa con una Enfermedad mental diagnosticada", "Cantidad de Empleados con una Enfermedad Mental que saben de los Beneficios que ofrece la empresa para ellos"])

    random_x = np.random.randint(1, 101, 100)
    random_y = np.random.randint(1, 101, 100)

    x = ['1-5', '6-25', '26-100', '100-500', "500-1000","Más de 1000" ]

    figp3_3 = go.Figure(data=[
        go.Bar(
            name='Cantidad de Personas con una Enfermedad Mental que conocen los Beneficios que Ofrece la Empresa',
            x=x,
            y=[1, 3, 8, 20, 10, 35],
            marker_color='#b366ff'  # changed color
            ),
        go.Bar(
            name='Cantidad de Personas dentro de la Empresa con una Enfermedad Mental Diagnosticada',
            x=x,
            y=[3, 24, 30, 44, 31, 71],
            marker_color='#cc99ff'  # changed color
            )
        ])

    figp3_3.update_layout(barmode='group', title="Cantidad de empleados con Enfermedad Mental y si Conocen de los Beneficios que Ofrece su Empresa (2018)")

    st.plotly_chart(figp3_3, use_container_width=True)

    st.write("""
    <p style="text-align: justify;">
        <ul>
            <li>Empresas de 1-5 empleados: solo 3 empleados tenían una enfermedad mental diagnosticada, y solo 1 de ellos conoce los beneficios que ofrece la empresa para este tipo de casos.</li>
                <li>Empresas de 6-25 empleados: Hay 24 empleados con una enfermedad mental diagnosticada, de esos 3 conocen de los beneficios que ofrece la empresa para ellos.</li>
                    <li>Empresas de 26-100 empleados: Hay 30 Personas con una Enfermedad mental Diagnostica y de estos 8 conoce sobre los beneficios que ofrece la empresa.</li>
                    <li>Empresas de 100-500 empleados: Es la segunda empresa que tiene más empleados con una enfermedad mental diagnostica con un total de 44 con una Enfermedad Mental y casi la mitad (20) conoce de los beneficios que tiene la empresa.</li>
                <li>Empresas de 500-1000 empleados: Hay 31 empleados con una enfermedad mental diagnosticada, de esos 10 conocen de los beneficios que ofrece la empresa para ellos.</li>
            <li>Empresas de más de 1000 empleados: Es la empresa que tiene más empleados con una Enfermedad Mental Diagnosticada con una total 71 empleados, y casi la mitad de estos (35) conoce sobre los beneficios que ofrece la empresa. Esto podría deberse a recursos y estrategias de comunicación más robustas en empresas de mayor tamaño.</li>
        </ul>
    </p>
    """, unsafe_allow_html=True)

elif option == '2019':
    df4 = pd.DataFrame ([["1-5", "3", "0"], ["6-25", "15", "3"], ["26-100", "21", "3"], ["100-500", "33", "11"], ["500-1000", "11", "3"], ["Más de 1000","48", "32"]],
                   columns = ["Tamaño de la Empresa", "Cantidad de Personas dentro de la Empresa con una Enfermedad mental diagnosticada", "Cantidad de Empleados con una Enfermedad Mental que saben de los Beneficios que ofrece la empresa para ellos"])

    random_x = np.random.randint(1, 101, 100)
    random_y = np.random.randint(1, 101, 100)

    x = ['1-5', '6-25', '26-100', '100-500', "500-1000","Más de 1000" ]

    figp3_4 = go.Figure(data=[
        go.Bar(
            name='Cantidad de Personas con una Enfermedad Mental que conocen los Beneficios que Ofrece la Empresa',
            x=x,
            y=[0,3, 3, 11, 3, 32],
            marker_color='#b366ff'
            ),
        go.Bar(
            name='Cantidad de Personas dentro de la Empresa con una Enfermedad Mental Diagnosticada',
            x=x,
            y=[3, 15, 21, 33, 11, 48],
            marker_color='#cc99ff'  # changed color
            )
        ])

    figp3_4.update_layout(barmode='group', title="Cantidad de empleados con Enfermedad Mental y si Conocen de los Beneficios que Ofrece su Empresa (2019)")

    st.plotly_chart(figp3_4, use_container_width=True)

    st.write("""
    <p style="text-align: justify;">
        <ul>
            <li>Empresas de 1-5 empleados: solo 3 empleados tenían una enfermedad mental diagnosticada, y ninguno conoce sobre los beneficios que ofrece la empresa.</li>
                <li>Empresas de 6-25 empleados: Hay 15 empleados con una enfermedad mental diagnosticada, de esos 3 conocen de los beneficios que ofrece la empresa para ellos.</li>
                    <li>Empresas de 26-100 empleados: Hay 21 Personas con una Enfermedad mental Diagnostica y de estos 3 conoce sobre los beneficios que ofrece la empresa.</li>
                    <li>Empresas de 100-500 empleados: Es la segunda empresa que tiene más empleados con una enfermedad mental diagnostica con un total de 33 con una Enfermedad Mental y solo 11 personas conocen de los beneficios que tiene la empresa Diagnosticada.</li>
                <li>Empresas de 500-1000 empleados: Hay 11 empleados con una enfermedad mental diagnosticada, de esos 3 conocen de los beneficios que ofrece la empresa para ellos.</li>
            <li>Empresas de más de 1000 empleados: Es la empresa que tiene más empleados con una Enfermedad Mental Diagnosticada con una total 48 empleados, y más de la mitad de estos (32) conoce sobre los beneficios que ofrece la empresa. Esto podría deberse a recursos y estrategias de comunicación más robustas en empresas de mayor tamaño.</li>
        </ul>
    </p>
    """, unsafe_allow_html=True)
