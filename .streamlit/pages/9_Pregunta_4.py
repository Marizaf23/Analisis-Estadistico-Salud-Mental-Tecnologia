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



st.header("Pregunta 4")
st.subheader('¿Cuál es la enfermedad mental más común dentro de cada puesto de trabajo en la industria tecnológica estadounidense? ¿De este grupo cuántos trabajan remotamente?')

# Crea un selectbox con las opciones
option = st.selectbox('Enfermedades Mentales:', ['Diagnosticadas','No Diagnosticadas'])

if option == 'Diagnosticadas':
    
    # Filtrar los registros que no tienen 'No respondió' en la columna Enfermedades Mentales Diagnosticadas
    df_2016_filtrado_1 = df_2016[df_2016['Enfermedades Mentales Diagnosticadas']!= 'No respondió']

    # Crear un nuevo dataframe que muestra la enfermedad mental diagnosticada más común para cada puesto de trabajo
    Pregunta4_1 = df_2016_filtrado_1.groupby('Puesto de Trabajo')['Enfermedades Mentales Diagnosticadas'].value_counts().reset_index(name='Número de Empleados')
    Pregunta4_1 = Pregunta4_1.loc[Pregunta4_1.groupby('Puesto de Trabajo')['Número de Empleados'].idxmax()]
    Pregunta4_1 = Pregunta4_1.sort_values(by='Número de Empleados', ascending=False)

    # Agregar columna con información de trabajo remoto
    Pregunta4_1['Trabajo Remoto'] = Pregunta4_1['Puesto de Trabajo'].apply(lambda x: df_2016_filtrado_1[df_2016_filtrado_1['Puesto de Trabajo'] == x]['Trabajo Remoto'].mode().values[0])

    # Reordenar columnas
    Pregunta4_1 = Pregunta4_1.loc[:, ['Puesto de Trabajo', 'Enfermedades Mentales Diagnosticadas', 'Trabajo Remoto', 'Número de Empleados']]

    Pregunta4_1 = Pregunta4_1.sort_values(by='Número de Empleados', ascending=False)

    # Contar la frecuencia de cada enfermedad mental diagnosticada
    Enfermedades2016_4_1 = df_2016_filtrado_1['Enfermedades Mentales Diagnosticadas'].value_counts().to_frame('Número de Empleados')

    Enfermedades2016_4_1.drop(Enfermedades2016_4_1.index[13], inplace=True)

    Enfermedades2016_4_1 = Enfermedades2016_4_1.reset_index(drop=False) 
    Enfermedades2016_4_1 = Enfermedades2016_4_1.rename(columns={'index': 'Enfermedades Mentales Diagnosticadas'}) 
    Enfermedades2016_4_1['Abreviatura'] = ['TA', 'TD/TB', 'TDAH', 'TEPT', 'TOC', 'TP', 'TCS', 'SRE', 'TP', 'TAE', 'LCT', 'TA', 'AS', 'TEP'] 
    Enfermedades2016_4_1 = Enfermedades2016_4_1.loc[:, ['Abreviatura', 'Enfermedades Mentales Diagnosticadas', 'Número de Empleados']]

    correcciones = {
    'Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)': 'Trastorno de Ansiedad (Generalizado, Social, Fobia, etc.)'}

    Enfermedades2016_4_1['Enfermedades Mentales Diagnosticadas'] = Enfermedades2016_4_1['Enfermedades Mentales Diagnosticadas'].replace(correcciones)

    fig20164_1 = px.bar(Enfermedades2016_4_1, x='Abreviatura', y='Número de Empleados', 
             title='Enfermedades Mentales Diagnosticadas',
             labels={'Abreviatura': 'Diagnóstico', 'Número de Empleados': 'Número de Empleados'},
             color='Abreviatura', color_discrete_sequence=['#004080', '#004d99', '#0059b3', '#0066cc', '#0073e6', '#0080ff', '#1a8cff', '#3399ff', '#4da6ff', '#66b3ff', '#80bfff', '#99ccff'],
             hover_name='Enfermedades Mentales Diagnosticadas')
    
    # Contar la frecuencia de cada puesto de trabajo
    Trabajo2016_4_1 = df_2016_filtrado_1['Puesto de Trabajo'].value_counts().to_frame('Cantidad de Empleados')

    # Pivot table para contar trabajo remoto
    Trabajo2016_4_1 = df_2016_filtrado_1.pivot_table(index='Puesto de Trabajo', columns='Trabajo Remoto', aggfunc='size', fill_value=0)

    # Agregar columna Total
    Trabajo2016_4_1['Total'] = Trabajo2016_4_1.sum(axis=1)

    # Renombrar columna Total a Número de Empleados
    Trabajo2016_4_1 = Trabajo2016_4_1.rename(columns={'Total': 'Número de Empleados'})

    # Reordenar columnas
    Trabajo2016_4_1 = Trabajo2016_4_1.loc[:, ['Siempre', 'A veces', 'Nunca', 'Número de Empleados']]

    # Ordenar por Total en orden descendente
    Trabajo2016_4_1 = Trabajo2016_4_1.sort_values(by='Número de Empleados', ascending=False)

    Trabajo_Remoto = ['Programador(a) Back-End', 'Programador(a) Front-End', 'Supervisor(a)/Líder de Equipo', 'Director(a) Ejecutivo', 'Promotor(a) de Desarrollo', 'Administrador(a) de Sistemas', 'Soporte o Ayuda', 'Diseñador(a)', 'Emprendedor(a)', 'Otros', 'Vendedor(a)', 'Recursos Humanos']

    fig20164_3 = go.Figure(data=[
    go.Bar(name='Siempre trabajo remoto', y=Trabajo_Remoto, x=[17, 11, 9, 9, 10, 12, 10, 3, 9, 4, 0, 0], orientation='h', marker_color='rgb(0, 89, 179)'),
    go.Bar(name='A veces trabajo remoto', y=Trabajo_Remoto, x=[57, 34, 26, 27, 25, 13, 11, 14, 8, 8, 2, 0], orientation='h', marker_color='rgb(0, 128, 255)'),
    go.Bar(name='Nunca trabajo remoto', y=Trabajo_Remoto, x=[23, 9, 11, 8, 5, 3, 1, 2, 2, 3, 1, 1], orientation='h', marker_color='rgb(102, 179, 255)')
    ])

    fig20164_3.update_layout(barmode='stack',
                  margin=dict(l=200),
                  title=dict(text='Distribución de Puestos de Trabajo Según Trabajo Remoto (Diagnóstico)',
                             font=dict(size=18)))

    st.dataframe(Enfermedades2016_4_1, width=1000, height=528, hide_index=True)
    st.plotly_chart(fig20164_1, use_container_width=True)

    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>El top 3 de enfermedades mentales diagnosticadas en el 2016 es el Trastorno de Ansiedad con 229 empleados, seguido por el Trastorno del Estado de Ánimo con 166 y el Trastorno por Déficit de Atención e Hiperactividad con 19 respuestas.</li>
                <li>Nota: Esta pregunta sólo se responderá para 2016 debido a que la variable de Enfermedades Mentales Diagnosticadas fue contestada unicamente ese año, al igual que Puesto de Trabajo.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)

    st.dataframe(Trabajo2016_4_1, width=1000, height=458)
    st.plotly_chart(fig20164_3, use_container_width=True)

    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>Los tres puestos que más trabajan remotamente son los Programadores Back-End (17 personas), los Emprendedores (12 personas), Supervisores y Líderes de Equipo (11 personas).</li>
                <li>Sin embargo, para esta época el trabajo remoto iba en ascenso más no era tan común todo el tiempo. Hay trabajadores que rara vez podrán trabajar remotamente como los Vendedores y el personal de Recursos Humanos.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)

    st.dataframe(Pregunta4_1, width=1000, height=458, hide_index=True)

    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>En la industria tecnológica predomina el Trastorno de Ansiedad en todos los puestos de trabajo, siendo los más afectados los Programadores Front-End.</li>
                <li>La mayoría de estos trabaja a distancia a veces. Los profesionales de Soporte o Ayuda trabajan siempre remotamente, a diferencia del Vendedor con TA que nunca a trabajado a distancia.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)

if option == 'No Diagnosticadas':
    
    # Filtrar los registros que no tienen 'No respondió' en la columna Enfermedades Mentales Diagnosticadas
    df_2016_filtrado_2 = df_2016[df_2016['Enfermedades Mentales No Diagnosticadas']!= 'No respondió']

    # Crear un nuevo dataframe que muestra la enfermedad mental diagnosticada más común para cada puesto de trabajo
    Pregunta4_2 = df_2016_filtrado_2.groupby('Puesto de Trabajo')['Enfermedades Mentales No Diagnosticadas'].value_counts().reset_index(name='Número de Empleados')
    Pregunta4_2 = Pregunta4_2.loc[Pregunta4_2.groupby('Puesto de Trabajo')['Número de Empleados'].idxmax()]
    Pregunta4_2 = Pregunta4_2.sort_values(by='Número de Empleados', ascending=False)

    # Agregar columna con información de trabajo remoto
    Pregunta4_2['Trabajo Remoto'] = Pregunta4_2['Puesto de Trabajo'].apply(lambda x: df_2016_filtrado_2[df_2016_filtrado_2['Puesto de Trabajo'] == x]['Trabajo Remoto'].mode().values[0])

    # Reordenar columnas
    Pregunta4_2 = Pregunta4_2.loc[:, ['Puesto de Trabajo', 'Enfermedades Mentales No Diagnosticadas', 'Trabajo Remoto', 'Número de Empleados']]

    Pregunta4_2 = Pregunta4_2.sort_values(by='Número de Empleados', ascending=False)

    # Contar la frecuencia de cada enfermedad mental no diagnosticada
    Enfermedades2016_4_2 = df_2016_filtrado_2['Enfermedades Mentales No Diagnosticadas'].value_counts().to_frame('Número de Empleados')

    Enfermedades2016_4_2 = Enfermedades2016_4_2.reset_index(drop=False)
    Enfermedades2016_4_2 = Enfermedades2016_4_2.rename(columns={'index': 'Enfermedades Mentales No Diagnosticadas'})
    Enfermedades2016_4_2['Abreviatura'] = ['TA', 'TD/TB', 'TDAH', 'TCS', 'TP', 'TEPT', 'TOC', 'DPP/A', 'SA', 'TEA', 'TCA']
    Enfermedades2016_4_2 = Enfermedades2016_4_2.loc[:, ['Abreviatura', 'Enfermedades Mentales No Diagnosticadas', 'Número de Empleados']]

    fig20164_2 = px.bar(Enfermedades2016_4_2, x='Abreviatura', y='Número de Empleados', 
             title='Enfermedades Mentales No Diagnosticadas',
             labels={'Abreviatura': 'Creencia', 'Número de Empleados': 'Número de Empleados'},
             color='Abreviatura', 
             color_discrete_sequence=['#400080', '#4d0099', '#5900b3', '#6600cc', '#7300e6', '#8000ff', '#8c1aff', '#9933ff', '#a64dff', '#b366ff', '#bf80ff'],
             hover_name='Enfermedades Mentales No Diagnosticadas')
    
    Trabajo2016_4_2 = df_2016_filtrado_2['Puesto de Trabajo'].value_counts().to_frame('Cantidad de Empleados')

    # Pivot table para contar trabajo remoto
    Trabajo2016_4_2 = df_2016_filtrado_2.pivot_table(index='Puesto de Trabajo', columns='Trabajo Remoto', aggfunc='size', fill_value=0)

    # Agregar columna Total
    Trabajo2016_4_2['Total'] = Trabajo2016_4_2.sum(axis=1)

    # Renombrar columna Total a Número de Empleados
    Trabajo2016_4_2 = Trabajo2016_4_2.rename(columns={'Total': 'Número de Empleados'})

    # Reordenar columnas
    Trabajo2016_4_2 = Trabajo2016_4_2.loc[:, ['Siempre', 'A veces', 'Nunca', 'Número de Empleados']]

    # Ordenar por Total en orden descendente
    Trabajo2016_4_2 = Trabajo2016_4_2.sort_values(by='Número de Empleados', ascending=False)

    Trabajo_Remoto = ['Programador(a) Back-End', 'Programador(a) Front-End', 'Supervisor(a)/Líder de Equipo', 'Director(a) Ejecutivo', 'Promotor(a) de Desarrollo', 'Administrador(a) de Sistemas', 'Soporte o Ayuda', 'Diseñador(a)', 'Emprendedor(a)', 'Otros', 'Vendedor(a)', 'Recursos Humanos']

    fig20164_4 = go.Figure(data=[
    go.Bar(name='Siempre trabajo remoto', y=Trabajo_Remoto, x=[9, 7, 8, 6, 3, 9, 7, 2, 1, 0, 0], orientation='h', marker_color='rgb(77, 0, 153)'),
    go.Bar(name='A veces trabajo remoto', y=Trabajo_Remoto, x=[21, 18, 15, 8, 10, 5, 1, 2, 3, 1, 1], orientation='h', marker_color='rgb(153, 51, 255)'),
    go.Bar(name='Nunca trabajo remoto', y=Trabajo_Remoto, x=[9, 9, 4, 7, 6, 1, 1, 2, 0, 0, 0], orientation='h', marker_color='rgb(191, 128, 255)')
    ])

    fig20164_4.update_layout(barmode='stack',
                  margin=dict(l=200),
                  title=dict(text='Distribución de Puestos de Trabajo Según Trabajo Remoto (Creencia)',
                             font=dict(size=18)))
    
    st.dataframe(Enfermedades2016_4_2, width=1000, height=422, hide_index=True)
    st.plotly_chart(fig20164_2, use_container_width=True)

    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>El top 3 de enfermedades mentales no diagnosticadas en el 2016 es el Trastorno de Ansiedad con 108 empleados, seguido por el Trastorno del Estado de Ánimo con 49 y el Trastorno por Déficit de Atención e Hiperactividad con 8 respuestas. Cuando se refiere a Creencia o Enfermedad Mental No Diagnosticada quiere decir que la persona cree tener esta enfermedad y no ha sido formalmente diagnosticada por un especialista.</li>
                <li>Nota: Esta pregunta sólo se responderá para 2016 debido a que la variable de Enfermedades Mentales No Diagnosticadas fue contestada unicamente ese año, al igual que Puesto de Trabajo.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)

    st.dataframe(Trabajo2016_4_2, width=1000, height=422)
    st.plotly_chart(fig20164_4, use_container_width=True)

    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>Los tres puestos que más trabajan remotamente son los Emprendedores (9 personas), los Programadores Back-End (9 personas) y los DevOps/Administradores de Sistemas (8 personas).</li>
                <li>La mayoría trabaja a distancia a cierta medida.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)

    st.dataframe(Pregunta4_2, width=1000, height=422, hide_index=True)
    
    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>Aquí vuelve a predominar el Trastorno de Ansiedad en casi los puestos de trabajo, siendo la excepción los Diseñadores y Vendedores que afirmaron tener Trastorno del Estado del Ánimo.</li>
                <li>La mayoría de estos trabaja a distancia a veces. Los Emprendedores y Promotores de Desarrollo trabajan siempre remotamente.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)
