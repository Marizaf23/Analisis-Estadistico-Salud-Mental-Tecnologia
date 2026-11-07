import pandas as pd
import numpy  as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import requests
from io import StringIO
from PIL import Image
import plotly.graph_objects as go
import base64

st.set_page_config(
    page_title="Grupo 2",
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io/help',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "Streamlit v1.13.0"
    }
)

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

st.markdown(
    """
    <style>
    :root {
        --primary-color: #4991f5;
    }
    body {
        color: #0a0a0a;
        background-color: #f5f5f5;
        font-family: serif;
    }
    .block-container {
        border-left: 1px solid var(--primary-color);
        border-right: 1px solid var(--primary-color);
        border-top: 1px solid var(--primary-color);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título de la aplicación
st.title("Problemáticas y Estigmas de las Enfermedades Mentales en la Industria Tecnológica Estadounidense 2016-2019")

# Contenido de la página 1
st.header("Introducción")
st.write('<p style="text-align: justify;">La salud mental es un aspecto crítico del desarrollo humano, social, económico, y es esencial para la salud en general.  Para los empleados de la TI (Industria Tecnológica) es un tema de preocupación creciente debido a las características únicas de este sector, el cual pueden contribuir de manera positiva o negativa al bienestar psicológico de sus empleados. Identificarse como una persona que padece de una Enfermedad Mental se ha convertido en un problema, una de las principales razones es el estigma y la discriminación que rodea las Enfermedades Mentales. La gente teme ser juzgada o tratada de manera diferente por sus compañeros de trabajo, familiares y amigos si se identifican con ello.</p>', unsafe_allow_html=True)

# Contenido de la página 2
st.header("Visualización de los Datos")

@st.cache_data
def load_csv_from_github(url):
        response = requests.get(url)
        if response.status_code == 200:
            return pd.read_csv(StringIO(response.text))
        else:
            st.error("Failed to load data from GitHub.")
            return None

# Identificar los URLs de los CSV del repositorio
urls = {
    '2016': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/95f59adcc416732d98f3b9aa494eb78cadd12c0d/CSV/Investigacion1.csv',
    '2017': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/95f59adcc416732d98f3b9aa494eb78cadd12c0d/CSV/Investigacion2.csv',
    '2018': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/95f59adcc416732d98f3b9aa494eb78cadd12c0d/CSV/Investigacion3.csv',
    '2019': 'https://raw.githubusercontent.com/Marizaf23/Analisis-Estadistico-Salud-Mental-Tecnologia/95f59adcc416732d98f3b9aa494eb78cadd12c0d/CSV/Investigacion4.csv'
}

# Cargar los CSV desde GitHub
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

st.write('<p style="text-align: justify;">La base de datos depurada y estructurada para esta investigación abarca los años 2016-2019. La fuente es Kaggle y su vez las encuestas anónimas realizadas por la organización OSMI para estudiar el conocimiento y aceptación de enfermedades mentales en la industria tecnológica. Se analizaron variables como diagnóstico, creencias, antecedentes heredofamiliares, trabajo remoto, recursos de apoyo, percepción externa, género y edad. El enfoque en este período previo a la pandemia permite observar cambios antes de la creciente conciencia sobre salud mental. A pesar de los desafíos en la normalización y limpieza de datos, se utilizaron herramientas como SQLite, Python y PowerBi para llevar a cabo la investigación.</p>', unsafe_allow_html=True)

st.header("Variables Cuantitativas")

st.subheader("Estadísticas Descriptivas de Edad por Año")

try:
    df_2016['Edad'] = pd.to_numeric(df_2016['Edad'], errors='coerce')
except Exception as e:
    st.write(f"Error: {e}")

Edad_2016 = df_2016['Edad'].describe().to_frame().T.round(2)

Edad_2017 = df_2017['Edad'].describe().to_frame().T.round(2)

Edad_2018 = df_2018['Edad'].describe().to_frame().T.round(2)

try:
    df_2019['Edad'] = pd.to_numeric(df_2019['Edad'], errors='coerce')
except Exception as e:
    st.write(f"Error: {e}")

Edad_2019 = df_2019['Edad'].describe().to_frame().T.round(2)

# Unir los DataFrames en uno
Edad_inv = pd.concat([Edad_2016, Edad_2017, Edad_2018, Edad_2019], ignore_index=True)

# Renombrar las filas con los años correspondientes
Edad_inv.index = ['2016', '2017', '2018', '2019']

# Renombrar las columnas
Edad_inv.columns = ['Muestra', 'Media', 'SD', 'Min', 'Q1', 'Md', 'Q3', 'Máx']

Edad_inv = Edad_inv[['Muestra', 'Media', 'Md', 'SD', 'Min', 'Máx', 'Q1', 'Q3']]

st.dataframe(Edad_inv, width=1800, height=178)

# Contenido de la página 3
st.header("Planteamiento Del Problema")
st.subheader("Objetivos")
st.write('<ul><li>Determinar las características e incidencias de las enfermedades mentales en la industria tecnológica estadounidense tomando en cuenta el diagnóstico, antecedentes heredofamiliares, edad, género y puesto de trabajo de los afectados.</li><li>Identificar el nivel de productividad de los empleados de la industria tecnológica estadounidense con enfermedades mentales y qué beneficios reciben para su tratamiento.</li><li>Indagar la percepción externa de los trabajadores sobre las enfermedades mentales en la industria tecnológica estadounidense.</li></ul>', unsafe_allow_html=True)

# Contenido de la página 4
st.header("Marco Teórico")
st.write("""
<style>
p {
  text-align: justify;
}
</style>
<p>La enfermedad mental puede ocasionar problemas en la vida cotidiana, por ejemplo, en la escuela, el trabajo o en las relaciones interpersonales. En la mayor parte de los casos, los síntomas pueden tratarse con una combinación de medicamentos y terapia de conversación (psicoterapia).</p>
<p>Las personas manifiestan problemas de salud mental de vez en cuando. Pero un problema de salud mental se convierte en una enfermedad mental cuando los signos y los síntomas se hacen permanentes, causan estrés y afectan la capacidad de funcionar normalmente.</p>
<p>Las enfermedades mentales son trastornos que van de leves a graves, que afectan el pensamiento, el estado de ánimo y/o el comportamiento de una persona. Según el Instituto Nacional de Salud Mental, casi uno de cada cinco adultos vive con una enfermedad mental.</p>
<p>Muchos factores contribuyen a tener problemas de salud mental, entre ellos:</p>
<ul>
  <li>Atributos hereditarios. La enfermedad mental es más frecuente en las personas cuyos parientes consanguíneos también la padecen. Ciertos genes pueden aumentar el riesgo de contraer una enfermedad mental y la situación de vida en particular puede desencadenarla.</li>
  <li>Exposición ambiental anterior al nacimiento. La exposición a factores de estrés ambientales, enfermedades inflamatorias, toxinas, drogas o alcohol en el útero puede asociarse, en algunos casos, con la enfermedad mental.</li>
  <li>Química del cerebro. Los neurotransmisores son sustancias químicas que se encuentran naturalmente en el cerebro y que transmiten señales a otras partes del cerebro y del cuerpo. Cuando las redes neuronales que contienen estas sustancias químicas se ven alteradas, la función de los receptores nerviosos y de los sistemas nerviosos cambia, lo que genera depresión y otros trastornos emocionales.</li>
</ul>
<p>Según los Centros para el Control de Enfermedades, los trastornos de salud mental afectan a más del 18 por ciento de los adultos solo en los Estados Unidos.</p>
<p>Y la Organización Mundial de la Salud informa que la depresión es la principal causa de discapacidad en todo el mundo. Aunque se informa que las enfermedades de salud mental no tratadas les cuestan a las empresas estadounidenses alrededor de $500 mil millones en pérdida de productividad, sin embargo, cuando las empresas priorizan la salud mental de sus trabajadores, pueden tener éxito y prosperar en el lugar de trabajo. Los empleadores deben considerar proporcionar recursos sólidos y sistemas de apoyo para los empleados, incluidos los técnicos de mantenimiento. (U.S Centers for Disease Control and Prevention [CDC], 2019).</p>
<p>La relación entre la salud mental y la productividad es innegable. Cuando los colaboradores están mentalmente saludables, tienden a ser más productivos. El estrés, la ansiedad y otros problemas de salud mental pueden afectar negativamente la concentración, la toma de decisiones y la calidad del trabajo.</p>
<p>Además, los problemas de salud mental no tratados pueden llevar a una mayor rotación de personal y ausentismo, lo que interrumpe la continuidad del trabajo y aumenta los costos para la empresa. Por otro lado ésto conlleva a crear estigmas dentro de éste entorno, los estigmas son una asociación de estereotipos negativos a una etiqueta y que discrimina a las personas, para las personas con enfermedades mentales el ser discriminados puede llevarlos a punto inimaginables, es por ello la importancia de estar informados y que ellos den a conocer su enfermedad sin sentir temor.</p>
<p>Para seguir siendo competitivas y ofrecer beneficios integrales, las empresas de mantenimiento deben priorizar la salud mental de sus empleados. Cuando los empleados tienen satisfechas sus necesidades básicas, que incluyen la salud mental, pueden generar más valor para sus organizaciones</p>
""", unsafe_allow_html=True)

# Contenido de la página 5
st.header("Pregunta 1")
st.subheader("¿Cuántas personas en la industria tecnológica tienen una enfermedad mental diagnosticada y, dentro de este grupo, existe algún historial familiar dentro de este ámbito?")

# Crea un selectbox con las opciones
option = st.selectbox('Año de Encuesta:', ['2016', '2017', '2018', '2019'], key='year_selectbox')

if option == '2016':

    #Crear la tabla bivariante con pandas
    Pregunta2016_1 = pd.crosstab(df_2016['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'], 
                        df_2016['Antecedentes Heredofamiliares'], 
                        margins=True, 
                        margins_name='Total')

    # Renombrar el índice
    Pregunta2016_1.index.name = "Antecedentes Heredofamiliares"
    
    # Agregar una fila debajo de los títulos de las columnas 
    Pregunta2016_1.loc['Enfermedad Mental'] = ['', '', '', '']

    Pregunta2016_1 = Pregunta2016_1.reindex(['Enfermedad Mental'] + [i for i in Pregunta2016_1.index if i != 'Enfermedad Mental'])
    
    Pregunta2016_1.rename(columns={'index': 'Enfermedad Mental'})

    st.dataframe(Pregunta2016_1, width=1500, height=177)

elif option == '2017':
    
    #Crear la tabla bivariante con pandas
    Pregunta2017_1 = pd.crosstab(df_2017['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'], 
                        df_2017['Antecedentes Heredofamiliares'], 
                        margins=True, 
                        margins_name='Total')

    # Renombrar el índice
    Pregunta2017_1.index.name = "Antecedentes Heredofamiliares"
    
    # Agregar una fila debajo de los títulos de las columnas 
    Pregunta2017_1.loc['Enfermedad Mental'] = ['', '', '', '']

    Pregunta2017_1 = Pregunta2017_1.reindex(['Enfermedad Mental'] + [i for i in Pregunta2017_1.index if i != 'Enfermedad Mental'])
    
    Pregunta2017_1.rename(columns={'index': 'Enfermedad Mental'})

    Pregunta2017_1 = Pregunta2017_1.reindex(['Enfermedad Mental'] + [i for i in Pregunta2017_1.index if i not in ['Enfermedad Mental', 'No respondió', 'Total']] + ['No respondió'] + ['Total'])
    
    st.dataframe(Pregunta2017_1, width=800, height=212)

elif option == '2018':
    
    #Crear la tabla bivariante con pandas
    Pregunta2018_1 = pd.crosstab(df_2018['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'], 
                        df_2018['Antecedentes Heredofamiliares'], 
                        margins=True, 
                        margins_name='Total')

    # Renombrar el índice
    Pregunta2018_1.index.name = "Antecedentes Heredofamiliares"
    
    # Agregar una fila debajo de los títulos de las columnas 
    Pregunta2018_1.loc['Enfermedad Mental'] = ['', '', '', '']

    Pregunta2018_1 = Pregunta2018_1.reindex(['Enfermedad Mental'] + [i for i in Pregunta2018_1.index if i != 'Enfermedad Mental'])
    
    Pregunta2018_1.rename(columns={'index': 'Enfermedad Mental'})

    Pregunta2018_1 = Pregunta2018_1.reindex(['Enfermedad Mental'] + [i for i in Pregunta2018_1.index if i not in ['Enfermedad Mental', 'No respondió', 'Total']] + ['No respondió'] + ['Total'])
    
    st.dataframe(Pregunta2018_1, width=800, height=212)

elif option == '2019':

    #Crear la tabla bivariante con pandas
    Pregunta2019_1 = pd.crosstab(df_2019['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'], 
                        df_2019['Antecedentes Heredofamiliares'], 
                        margins=True, 
                        margins_name='Total')

    # Renombrar el índice
    Pregunta2019_1.index.name = "Antecedentes Heredofamiliares"
    
    # Agregar una fila debajo de los títulos de las columnas 
    Pregunta2019_1.loc['Enfermedad Mental'] = ['', '', '', '']

    Pregunta2019_1 = Pregunta2019_1.reindex(['Enfermedad Mental'] + [i for i in Pregunta2019_1.index if i != 'Enfermedad Mental'])
    
    Pregunta2019_1.rename(columns={'index': 'Enfermedad Mental'})

    Pregunta2019_1 = Pregunta2019_1.reindex(['Enfermedad Mental'] + [i for i in Pregunta2019_1.index if i not in ['Enfermedad Mental', 'No respondió', 'Total']] + ['No respondió'] + ['Total'])

    st.dataframe(Pregunta2019_1, width=800, height=212)

st.header("Pregunta 2")
st.subheader("¿Cuáles son los 5 estados con mayor registro de enfermedades mentales diagnosticadas y cuál es la enfermedad mental predominante en cada uno? ¿Cuál es la enfermedad mental diagnosticada más común por rango de edad y cuál es el top 5 de enfermedades mentales más comunes por género?")
st.subheader("Mapa General de EEUU con la Enfermedades Mentales Más Comunes")

import plotly.express as px
import pandas as pd

data = pd.DataFrame({
'State': ['Alabama', 'Arizona', "California","Carolina del Norte", "Carolina del Sur", "Connecticut", "Delaware", "Florida","Georgia", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Missouri","Nebraska","Nueva Jersey","Nueva York","Nuevo Hampshire","Ohio","Oklahoma","Oregon","Pensilvania","Rhode Island","Tennessee","Texas","Utah","Vermont","Virginia","Virginia del Oeste","Washington","Wisconsin"],
'Frequency': [2,1,34,8,1,3,1,5,3,2,18,8,2,2,2,2,3,4,12,12,2,2,3,13,1,6,2,11,16,1,6,13,3,1,4,1,10,5]
    })

# Group the data by state and sum the frequencies
data = data.groupby('State')['Frequency'].sum().reset_index()

# Create a column with state abbreviations
data['State Abbrev'] = data['State'].map({
    "Alabama":"AL",
    "Arizona": "AZ",
    "California": "CA",
    "Carolina del Norte": "NC",
    "Carolina del Sur":"SC",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",        
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Missouri": "MO",
    "Nebraska": "NE",
    "Nueva Jersey": "NJ",
    "Nueva York": "NY",
    "Nuevo Hampshire": "NH",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pensilvania": "PA",
    "Rhode Island": "RI",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Virginia del Oeste": "WV",
    "Washington": "WA",
    "Wisconsin": "WI"
    })

# Add a new column with mental health condition information
data['Mental Health Condition'] = data['State'].map({
   "Alabama":"Trastorno del Estado del Ánimo (Depresion, Trastorno Bipolar, etc.)",
    "Arizona": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "California": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Carolina del Norte": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Carolina del Sur":"Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Connecticut": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Delaware": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Florida": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Georgia": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Idaho": "Trastorno del Estado del Ánimo (Depresion, Trastorno Bipolar, etc.)",
    "Illinois": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Indiana": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Kansas": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Kentucky": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Louisiana": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Maine": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Maryland": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Massachusetts": "Trastorno del Estado del Ánimo (Depresion, Trastorno Bipolar, etc.)",
    "Michigan": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Minnesota": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Missouri": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Nebraska": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Nueva Jersey": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Nueva York": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Nuevo Hampshire": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Ohio": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Oklahoma": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Oregon": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Pensilvania": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Rhode Island": "Trastorno Obsesivo-Compulsivo",
    "Tennessee": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Texas": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Utah": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Vermont": "Trastorno de Consumo de Sustancias",
    "Virginia": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Virginia del Oeste": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Washington": "Trastorno de Ansiedad (Genralizado, Social, Fobia, etc.)",
    "Wisconsin": "Trastorno del Estado del Ánimo (Depresion, Trastorno Bipolar, etc.)"
    })

# Create a choropleth map
figp2 = px.choropleth(
        data,
        locations="State Abbrev",  
        locationmode="USA-states",
        color="Frequency",
        scope="usa",
        color_continuous_scale=[
            (0, "lightgray"), 
            (0.2, "lightblue"),  
            (0.4, "skyblue"),  
            (0.6, "blue"), 
            (0.8, "darkblue"),  
            (1, "navy") 
        ],
        hover_name="State",
        hover_data=["Frequency", "Mental Health Condition"],  
        color_continuous_midpoint=data['Frequency'].mean(),  
        title="Frecuencia de Condiciones de Salud Mental por Estado en EE. UU.", 
        )

figp2.update_layout(coloraxis_colorbar=dict(title="Frecuencia de Casos"))

st.write("Se observa en la siguiente gráfica el mapa de EEUU separado en estados y la enfermedad mental diagnosticada más comun.")

st.plotly_chart(figp2, use_container_width=True)

st.header("Pregunta 3")
st.subheader('Según la cantidad de empleados en las empresas tecnológicas ¿Cuál tiene la mayor cantidad con enfermedades mentales? ¿Los empleados conocen los beneficios que ofrece la empresa?')

st.subheader("2016")
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

    st.dataframe(Enfermedades2016_4_1, width=1000, height=528, hide_index=True)

    st.dataframe(Trabajo2016_4_1, width=1000, height=458)

    st.dataframe(Pregunta4_1, width=1000, height=458, hide_index=True)


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

    st.dataframe(Trabajo2016_4_2, width=1000, height=422)

    st.dataframe(Pregunta4_2, width=1000, height=422, hide_index=True)
    
    st.dataframe(Pregunta4_2, width=1000, height=422, hide_index=True)

st.header("Pregunta 5")
st.subheader('¿Cuál es la disposición de los empleados de la industria tecnológica a a hora de hablar sobre su enfermedad mental y cómo creen que serían las reacciones externas?')

st.header("Disposición Para Hablar")
st.subheader("Disposición a la hora de hablar sobre tu salud mental con supervisor")

st.subheader("2016")
filtro_si_diagnosticado = df_2016['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'] == 'Si'
pregunta_5_2016 = pd.crosstab(df_2016[filtro_si_diagnosticado]['Disposición de Hablar de Salud Mental con un Supervisor'], 
                                df_2016[filtro_si_diagnosticado]['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'], margins=True)
pregunta_5_2016 = pregunta_5_2016.rename(columns={'Si': 'Diagnosticado con Enfermedad Mental'})
pregunta_5_2016 = pregunta_5_2016.drop('All', axis=0).drop('All', axis=1)  # Elimina las filas y columnas "All"
st.dataframe(pregunta_5_2016)

st.subheader("Disposición a la hora de hablar sobre tu salud mental con amigos y familiares")

st.subheader("2016")

filtro_si_diagnosticado = df_2016['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'] == 'Si'
pregunta1_5_2016 = pd.crosstab(df_2016[filtro_si_diagnosticado]['Disposición para Hablar Sobre Enfermedad Mental con Familia/Amigos'], 
                                df_2016[filtro_si_diagnosticado]['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'], margins=True)
pregunta1_5_2016 = pregunta1_5_2016.rename(columns={'Si': 'Diagnosticado con Enfermedad Mental'})
pregunta1_5_2016 = pregunta1_5_2016.drop('All', axis=0).drop('All', axis=1)  # Eliminar fila y columna "All"

# Seleccionar las filas que contienen "no dispuesto (a)" y "no estoy dispuesto (a)"
no_dispuestos = pregunta1_5_2016.loc[['No estoy dispuesto(a)', 'No dispuesto(a)']]

# Sumar las filas seleccionadas
no_dispuestos_sum = no_dispuestos.sum()

# Reemplazar las filas originales con la nueva fila sumada
pregunta1_5_2016.loc['No Dispuesto'] = no_dispuestos_sum
pregunta1_5_2016 = pregunta1_5_2016.drop(['No estoy dispuesto(a)', 'No dispuesto(a)'], axis=0)

st.dataframe(pregunta1_5_2016)

st.subheader("¿Crees que los miembros de su Equipo/Compañeros de trabajo te verían o reaccionarían de mala manera si revelas tener una enfermedad mental? (2016-2019)")
st.subheader("2016")

filtro_si_diagnosticado = df_2016['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'] == 'Si'
preguntatrabajo_5_2016 = pd.crosstab(df_2016[filtro_si_diagnosticado]['¿Cree que los Miembros de su Equipo/Compañeros de Trabajo le Verían de Forma más Negativa Si Supieran que Padece una Enfermedad Mental?'], 
                                df_2016[filtro_si_diagnosticado]['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'], margins=True)
preguntatrabajo_5_2016 = preguntatrabajo_5_2016.rename(columns={'Si': ''})
preguntatrabajo_5_2016 = preguntatrabajo_5_2016.drop('All', axis=0).drop('All', axis=1)  # Elimina las filas y columnas "All"
st.dataframe(preguntatrabajo_5_2016)

st.header("Pregunta 6")
st.subheader("¿El nivel de productividad de los trabajadores estadounidenses con enfermedades mentales diagnosticadas varía según su rango de edad?")

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

st.header("Conclusión")
st.write("""
<style>
p {
  text-align: justify;
}
</style>
<ul>
    <li>La enfermedad mental es un problema común en el sector tecnológico estadounidense, que provoca que las personas sufran síntomas como fatiga, falta de concentración y productividad reducida, lo que puede afectar negativamente su desempeño laboral y su bienestar general.
    <li>Las empresas deben velar por la salud mental de sus trabajadores, dado que si tienen empleados sanos la empresa tendrá mejor rendimiento.
    <li>Las empresas generalmente no promueven el sistema de apoyo que ofrecen a sus trabajadores, esto podría ocasionar recortes del presupuesto destinados a programas de salud mental, ocasionando que personas que sí reciban el apoyo puedan perderlo eventualmente.
    <li>El número de personas con enfermedades mentales se mantiene estable a través de los años, esto es un problema ya que de alguna manera no se genera ningún cambio significativo, lo que quiere decir que la situación no mejora.
</ul>
<p>En última instancia, todos somos responsables de crear una cultura laboral que valore la salud mental y promueva el bienestar. Juntos, podemos marcar la diferencia y construir un futuro tecnológico más humano y sostenible.</p>
""", unsafe_allow_html=True)

st.subheader("Recomendaciones")
st.write("""
<style>
p {
  text-align: justify;
}
</style>
<ul>
    <li>Promover la Comunicación Abierta: Establecer un espacio seguro para que los empleados compartan sus preocupaciones y desafíos es fundamental. La comunicación abierta reduce el estrés y fomenta un sentido de comunidad.</p>
    <li>Fomentar el Equilibrio entre el Trabajo y la Vida Personal: Establecer límites claros entre el tiempo de trabajo y el tiempo personal ayuda a los empleados a desconectar y recargar energías, lo que es vital para su bienestar.</p>
<ul>
""", unsafe_allow_html=True)

