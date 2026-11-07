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


# Contenido de la página 5
st.header("Pregunta 2")
st.subheader('¿Cuáles son los 5 estados con mayor registro de enfermedades mentales diagnosticadas y cuál es la enfermedad mental predominante en cada uno? ¿Cuál es la enfermedad mental diagnosticada más común por rango de edad y cuál es el top 5 de enfermedades mentales más comunes por género?')

# Crea un selectbox con las opciones
option = st.selectbox('EEUU:', ['General','Estados'])

if option == 'General':
    #Mapa con la enfermedad mas frecuente registrada

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

elif option == 'Estados':

    pregunta_2 = df_2016[df_2016['Enfermedades Mentales Diagnosticadas']!= 'No respondió'].groupby('Ciudad de Residencia (EEUU)')['Enfermedades Mentales Diagnosticadas'].value_counts().nlargest(5).reset_index(name='Frecuencia')

    pregunta_2 = pregunta_2.loc[:, ['Enfermedades Mentales Diagnosticadas', 'Ciudad de Residencia (EEUU)', 'Frecuencia']]  # Reordenar columnas

    pregunta_2.columns = ['Enfermedades Mentales Diagnosticadas', 'Ciudad de Residencia (EEUU)', 'Cantidad de personas']  # Renombrar columnas

    print(pregunta_2.to_string(header=True, index=False))

    #Grafica

    import plotly.express as px
    data = pd.DataFrame({
        'State': ['California', 'California', 'Illinois', 'Pennsylvania', 'New York'],
        'Frequency': [34, 19, 18, 16, 13]
    })


    data = data.groupby('State')['Frequency'].sum().reset_index()


    data['State Abbrev'] = data['State'].map({
        'California': 'CA',
        'Illinois': 'IL',
        'Pennsylvania': 'PA',
        'New York': 'NY'
        })


    data['Mental Health Condition'] = data['State'].map({
        'California': 'Trastorno de Ansiedad (Generalizado,Fobia, Social, Trastorno del Ánimo (Depresión, Trastorno Bipolar, etc))',
        'Illinois': 'Generalizado,Fobia, Social',
        'Pennsylvania': 'Generalizado,Fobia, Social',
        'New York': 'Generalizado,Fobia, Social'
        })


    figp2_1 = px.choropleth(
        data,
        locations="State Abbrev", 
        locationmode="USA-states",
        color="Frequency",
        scope="usa",
        color_continuous_scale="Purples", 
        hover_name="State",
        hover_data=["Frequency", "Mental Health Condition"], 
        color_continuous_midpoint=data['Frequency'].mean(), 
        title="Frecuencia de Condiciones de Salud Mental por Estado en EE. UU.",  
        )

    figp2_1.update_layout(coloraxis_colorbar=dict(title="Frecuencia de Casos"))

    # Show the graph
    figp2_1.show()

    st.write("En el siguiente mapa se puede observar en qué estados hay mayores casos de enfermedades mentales y su diagnóstico, siendo el estado de California el principal de estos con un registro de 53 personas y su respuesta más común el Trastorno de Ansiedad (Depresión, Trastorno Bipolar, etc).")

    st.plotly_chart(figp2_1, use_container_width=True)
    
    st.header("Enfermedad Más Común por Edad")

    #Dado los rangos de edad ¿Cual es la enfermedad mental más frecuente en cada uno? solo 201
    df_20162=df_2016
    # Convertir la columna Edad a tipo numérico, convirtiendo valores no numéricos a NaN
    df_20162['Edad'] = pd.to_numeric(df_20162['Edad'], errors='coerce')

    # Eliminar filas con valores NaN en la columna Edad
    df_20162 = df_20162.dropna(subset=['Edad'])

    # Convertir la columna Edad a tipo entero
    df_20162['Edad'] = df_20162['Edad'].astype(int)

    # Convertir la columna Enfermedades Mentales Diagnosticadas a tipo string
    df_20162['Enfermedades Mentales Diagnosticadas'] = df_20162['Enfermedades Mentales Diagnosticadas'].astype(str)

    # Crear una columna Edad_binned con los rangos de edad
    df_20162['Edad'] = pd.cut(df_20162['Edad'], bins=[18, 25, 32, 38, 44, 50, 56, 66], 
                                 labels=['19-25', '26-32', '33-38', '39-44', '45-50', '51-56', '57-66'],
                                 include_lowest=True)

    # Eliminar filas con "No respondio" en la columna Enfermedades Mentales Diagnosticadas
    df_20162 = df_20162[~df_20162['Enfermedades Mentales Diagnosticadas'].isin(['No respondió'])]

    # Agrupar por Edad y Enfermedades Mentales Diagnosticadas, y contar la frecuencia
    pregunta2_2 = df_20162.groupby(['Edad', 'Enfermedades Mentales Diagnosticadas']).size().reset_index(name='Cantidad de personas')

    # Seleccionar la enfermedad mental más frecuente para cada rango de edad
    pregunta2_2 = pregunta2_2.loc[pregunta2_2.groupby('Edad')['Cantidad de personas'].idxmax()]

    # Reordenar las columnas
    pregunta2_2 = pregunta2_2[['Enfermedades Mentales Diagnosticadas', 'Edad', 'Cantidad de personas']]

    # Mostrar la tabla con la enfermedad mental más frecuente para cada rango de edad
    print(pregunta2_2)

    # Sort the data by 'Cantidad de personas' in ascending order
    pregunta2_2_sorted = pregunta2_2.sort_values(by='Cantidad de personas')

    # Convert the data to a bar chart
    figp2_2 = go.Figure(data=[go.Bar(x=pregunta2_2_sorted['Edad'], 
                             y=pregunta2_2_sorted['Cantidad de personas'],
                             hovertext=pregunta2_2_sorted['Enfermedades Mentales Diagnosticadas'],
                             hovertemplate='Edad: %{x}<br>Frecuencia: %{y}<br>Enfermedad Mental: %{hovertext}<extra></extra>',
                             marker=dict(color=pregunta2_2_sorted['Cantidad de personas'],
                                          colorscale=[[0, 'rgba(0, 0, 64, 0.5)'],
                                                      [1, 'rgba(0, 0, 128, 0.5)']],
                                          showscale=False)
                             )])

    # Customize the plot
    figp2_2.update_layout(title='<b>Distribución de la Edad</b><br>Enfermedad Mental',
                  xaxis_title='Edad',
                  yaxis_title='Frecuencia')

    st.write("En el siguiente gráfico se muestran los rangos de edad de los empleados de la industria tecnológica y qué enfermedad mental tienden a padecer, dando como resultado el Trastorno de Ansiedad (Generalizado, Social, Fobia, etc). El rango de edad más padeciente en esta industria está entre los 26 y 32 años.")

    st.plotly_chart(figp2_2, use_container_width=True)

    st.header("Top 5: Enfermedades Mentales Más Comunes por Género")

    Pregunta2_3 = df_2016.groupby(['Enfermedades Mentales Diagnosticadas', 'Género']).size().reset_index(name='Cantidad de personas')

    Pregunta2_3 = Pregunta2_3[Pregunta2_3['Género']!= 'No respondió']  # Eliminar "No respondió" de la columna "Género"

    top_5_enfermedades = Pregunta2_3.groupby('Enfermedades Mentales Diagnosticadas')['Cantidad de personas'].sum().nlargest(6).index

    Pregunta2_3 = Pregunta2_3[Pregunta2_3['Enfermedades Mentales Diagnosticadas'].isin(top_5_enfermedades)]

    Pregunta2_3 = Pregunta2_3[Pregunta2_3['Enfermedades Mentales Diagnosticadas']!= 'No respondió']

    Pregunta2_3 = Pregunta2_3.pivot_table(index='Enfermedades Mentales Diagnosticadas', columns='Género', values='Cantidad de personas', fill_value=0)

    figp2_3 = go.Figure()
    figp2_3.add_trace(go.Bar(
        x=Pregunta2_3.index,  
        y=Pregunta2_3['Femenino'],  
        name='Femenino',
        marker_color='#938DBB',
        opacity=0.75
        ))
    figp2_3.add_trace(go.Bar(
        x=Pregunta2_3.index,  
        y=Pregunta2_3['Masculino'],
        name='Masculino',
        marker_color= '#7A3586',
        opacity=0.75
        ))
    figp2_3.add_trace(go.Bar(
        x=Pregunta2_3.index,  
        y=Pregunta2_3['Otro'],  
        name='Otro',
        marker_color='#410E48',
        opacity=0.75
        ))

    figp2_3.update_layout(
        title_text='Top 5 Enfermedades Mentales por Género', 
        xaxis_title_text='Enfermedades Mentales',  
        yaxis_title_text='Cantidad de personas', 
        bargap=0.2,  
        bargroupgap=0.1,  
        xaxis=dict(
        showticklabels=False  
        ),
        legend=dict(
        font=dict(
            size=18  
        )
        ),
        width=800,  
        height=600  
        )
    figp2_3.show()

    st.write("A continuación se muestran las 5 enfermedades mentales más comúnes según es el género predominante en la industria, dando como resultado que la mayoria de las personas que padecen el Trastorno de Ansiedad (Generalizado, Social, Fobia, etc) son hombres.")

    st.plotly_chart(figp2_3, use_container_width=True)

    st.write("Nota: Esta pregunta se responde para 2016 debido a que la variable de Enfermedades Mentales Diagnosticadas fue respondida en este año.")
