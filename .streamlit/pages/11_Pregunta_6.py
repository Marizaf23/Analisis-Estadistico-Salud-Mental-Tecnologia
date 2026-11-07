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


st.header("Pregunta 6")
st.subheader('¿El nivel de productividad de los trabajadores estadounidenses con enfermedades mentales diagnosticadas varía según su rango de edad?')

labels = ['1-25%', '26-50%', '51-75%', '76-100%']
sizes = [1, 1, 2, 3]

# Crear figura y axe
fig6_4, ax = plt.subplots()

colores = ['#4d94ff', '#3385ff', '#66a3ff', '#0066ff']

# Crear gráfico circular
ax.pie(sizes, labels=labels, autopct=lambda p: '{:.0f}'.format(p* sum(sizes) / 100), colors=colores)

# Título del gráfico
ax.set_title('Porcentaje de Tiempo Afectado por una Enfermedad Mental entre las Edades 20-28')

st.pyplot(fig6_4, use_container_width=True)

st.write("Entre las personas de 20 a 28 años que afirman tener una enfermedad mental diagnosticada, se observa una distribución variable en cuanto al impacto de estas condiciones en su tiempo laboral:")

st.write("""
    <p style="text-align: justify;">La afectación del tiempo laboral se distribuye de la siguiente manera:</p>
    <ul style="text-align: justify;">
        <li>Afectación leve (1-25%): 1 persona (14.28%) reportan que su enfermedad mental afecta su tiempo laboral en un rango bajo, entre 1% y 25%.</li>
        <li>Afectación moderada (26-50%): 1 persona (14.28%) indican que su enfermedad mental impacta su tiempo laboral en un rango moderado, entre 26% y 50%.</li>
        <li>Afectación significativa (51-75%): 2 personas (28.57%) reportan una afectación significativa, con un impacto en su tiempo laboral entre 51% y 75%.</li>
        <li>Afectación grave (76-100%): 3 personas (42.85%) indican una afectación grave, con un impacto en su tiempo laboral superior al 75%.</li>
    </ul>
""", unsafe_allow_html=True)

labels = ['1-25%', '26-50%', '51-75%', '76-100%']
sizes = [10, 2, 1, 1]

# Crear figura y axe
fig6_5, ax = plt.subplots()

colores = ['#4d94ff', '#3385ff', '#66a3ff', '#0066ff']

# Crear gráfico circular
ax.pie(sizes, labels=labels, autopct=lambda p: '{:.0f}'.format(p* sum(sizes) / 100), colors=colores)

# Título del gráfico
ax.set_title('Porcentaje de Tiempo Afectado por una Enfermedad Mental entre las Edades 38-46')

st.pyplot(fig6_5, use_container_width=True)

st.write("Entre las personas de 36 a 46 años que afirman tener una enfermedad mental diagnosticada, se observa una distribución variable en cuanto al impacto de estas condiciones en su tiempo laboral:")

st.write("""
    <p style="text-align: justify;">La afectación del tiempo laboral se distribuye de la siguiente manera:</p>
    <ul style="text-align: justify;">
        <li>Afectación leve (1-25%): 10 personas (71.42%) reportan que su enfermedad mental afecta su tiempo laboral en un rango bajo, entre 1% y 25%.</li>
        <li>Afectación moderada (26-50%): 2 personas (12.28%) indican que su enfermedad mental impacta su tiempo laboral en un rango moderado, entre 26% y 50%.</li>
        <li>Afectación significativa (51-75%): 1 persona (7.14%) reportan una afectación significativa, con un impacto en su tiempo laboral entre 51% y 75%.</li>
        <li>Afectación grave (76-100%): 1 persona (7.14%) indica una afectación grave, con un impacto en su tiempo laboral superior al 75%.</li>
    </ul>
""", unsafe_allow_html=True)

labels = ['1-25%', "26-50%", '51-75%', "76-100%"]
sizes = [6, 3, 2, 1]

# Crear figura y axe
fig6_1, ax = plt.subplots()

colores = ['#4d94ff', '#3385ff', '#66a3ff', '#0066ff']

# Crear gráfico circular
ax.pie(sizes, labels=labels, autopct=lambda p: '{:.0f}'.format(p* sum(sizes) / 100), colors=colores)

# Título del gráfico
ax.set_title('Porcentaje de Tiempo Afectado por una Enfermedad Mental entre las Edades 47-55')

st.pyplot(fig6_1, use_container_width=True)

st.write("""
    <p style="text-align: justify;">La afectación del tiempo laboral se distribuye de la siguiente manera:</p>
    <ul style="text-align: justify;">
        <li>Afectación leve (1-25%): 6 personas (37.5%) reportan que su enfermedad mental afecta su tiempo laboral en un rango bajo, entre 1% y 25%.</li>
        <li>Afectación moderada (26-50%): 3 personas (18.75%) indican que su enfermedad mental impacta su tiempo laboral en un rango moderado, entre 26% y 50%.</li>
        <li>Afectación significativa (51-75%): 2 personas (12.5%) reportan una afectación significativa, con un impacto en su tiempo laboral entre 51% y 75%.</li>
        <li>Afectación grave (76-100%): 1 persona (6.25%) indica una afectación grave, con un impacto en su tiempo laboral superior al 75%.</li>
    </ul>
""", unsafe_allow_html=True)

# Datos
data = [2, 2]  # example data
labels = ['1-25%', '51-75%']

# Crear figura y axe
fig6_2, ax = plt.subplots()

colores = ['#4d94ff', '#3385ff', '#66a3ff', '#0066ff']

# Crear gráfico circular
ax.pie(data, labels=labels, autopct=lambda p : '{:.0f}'.format(data[int(p/100*len(data))]), colors=colores)

# Título del gráfico
ax.set_title('Porcentaje de Tiempo Afectado por una Enfermedad Mental entre las Edades 56-65')

st.pyplot(fig6_2, use_container_width=True)

st.write("Entre las personas de 56-65 años que afirman tener una enfermedad mental diagnosticada, se observa una distribución variable en cuanto al impacto de estas condiciones en su tiempo laboral:")

st.write("""
    <ul style="text-align: justify;">
        <li>Afectación leve (1-25%): 2 personas (50%) reportan que su enfermedad mental afecta su tiempo laboral en un rango bajo, entre 1% y 25%.</li>
        <li>Afectación significativa (51-75%): 2 personas (50%) reportan una afectación significativa, con un impacto en su tiempo laboral entre 51% y 75%.</li>
    </ul>
""", unsafe_allow_html=True)
