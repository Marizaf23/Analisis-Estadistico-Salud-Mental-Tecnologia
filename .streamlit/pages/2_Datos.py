import pandas as pd
import numpy  as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly as px
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


# Título de la aplicación
st.title("Problemáticas y Estigmas de las Enfermedades Mentales en la Industria Tecnológica Estadounidense 2016-2019")


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

st.write('<p style="text-align: justify;">Adjunto a esta app se muestra la base de datos debidamente depurada y estructurada para los años a estudiar en esta investigación (2016-2019). No se trabajó con la data cruda obtenida de Kaggle (banco de datasets en línea) debido a que la información proviene de encuestas online realizadas por la organización OSMI (Open Sourcing Mental Illness) de forma anónima para estudiar el conocimiento y aceptación de las enfermedades mentales en la industria tecnológica a través de los años. Estas se estructuran en forma de preguntas y algunas van cambiando con el tiempo, por lo que algunas variables sólo estarán disponibles para un año en específico. Se decide estudiar este periodo de cuatro años, que justamente transcurren justo antes de la pandemia, porque sería interesante ver un panorama antes de está época cuando la salud mental no era tan publicitada o tomada en cuenta como lo es hoy. Además, la data solo contenía estos años con el 2014; el cual no fue tomado en cuenta debido a que no respondía a la mayoría de las variables en cuestión. Para poder llevar a cabo la investigación se seleccionaron las variables que indicaban diagnóstico y creencia de enfermedades mentales con su debido antecedente heredofamiliar, el puesto de trabajo de los empleados de la indistria tecnológica con la información en cuanto a si trabajan remotamente o no, la cantidad de empleados en la empresa, los recursos y canales de apoyo que proporciona, la percepción de enfermedades mentales desde el punto de vista externo con los afectados, el género y su edad. Como más del 60% de la informacion fue recaudada en Estados Unidos y la organización proviene de allá, se tomaron esta y la cuidad de residencia de los encuestados. Haber llevado a cabo este formato de presentación de datos fue un arduo trabajo debido a que las tablas en SQLite no estaban normalizadas, el formato y las respuestas eran en inglés y aún limpiando, filtrando y depurando la data, quedaron variables nulas que fueron reemplazadas por un no respondió en casi todas. Las herramientas utilizadas para llevar a cabo esta investigación fueron SQLite, Python y PowerBi, con algunos paquetes específicos como Streamlit.</p>', unsafe_allow_html=True)


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

st.write('<p style="text-align: justify;">Para el 2016 se tienen 836 datos a considerar ya que originalmente eran 839. Esto se debe a que tres personas no contestaron su edad y para esta variable tuvieron que ser excluídos. La edad promedio de los trabajadores que contestaron esta encuesta y pertenecen a la industria tecnológica es de 35 años con una desviación estándar de 8,36; donde el 25% de los individuos tiene 29 años, el 50% tiene 33 y el 75% tiene 39 años. El trabajador más joven tiene 19 años, y el mayor tiene 66 años.</p>', unsafe_allow_html=True)
st.write('<p style="text-align: justify;">Para el 2017, 497 individuos que contestaron la encuesta. La edad promedio de los trabajadores que pertenecen a la industria tecnológica es de 36 años con una desviación estándar de 8,39; donde el 25% de los individuos tiene 30 años, el 50% tiene 35 y el 75% tiene 40 años. El trabajador más joven tiene 21 años, y el mayor tiene 67 años.</p>', unsafe_allow_html=True)
st.write('<p style="text-align: justify;">Para el 2018, 312 personas contestaron la encuesta. La edad promedio de los trabajadores que pertenecen a la industria tecnológica es de 35 años con una desviación estándar de 8; donde el 25% de los individuos tiene 29 años, el 50% tiene 34 y el 75% tiene 39 años. El trabajador más joven tiene 19 años, y el mayor tiene 67 años.</p>', unsafe_allow_html=True)
st.write('<p style="text-align: justify;">Para el 2019 se tienen 203 datos a considerar ya que originalmente eran 204. Esto se debe a que una persona no contestó su edad y para esta variable tuvo que ser excluído. La edad promedio de los trabajadores que contestaron esta encuesta y pertenecen a la industria tecnológica es de 36 años con una desviación estándar de 8,82; donde el 25% de los individuos tiene 29 años, el 50% tiene 35 y el 75% tiene 41 años. El trabajador más joven tiene 19 años, y el mayor tiene 63 años.</p>', unsafe_allow_html=True)

# Drop unnecessary columns
Edad_inv_graph = Edad_inv.drop(['Muestra', 'SD'], axis=1)

# Renombrar las columnas
Edad_inv_graph.columns = ['mean', '50%', 'min', 'max', '25%', '75%']

fig_edad = px.box(Edad_inv_graph, x=Edad_inv_graph.index, y=Edad_inv_graph.columns, 
                 title='Distribución de Edades por Año', 
                 color_discrete_sequence=['#0033cc'])

fig_edad.update_layout(
    xaxis_title="Año",
    yaxis_title="Edades"
)

st.plotly_chart(fig_edad, use_container_width=True)

st.write('<p style="text-align: justify;">No existe mayor cambio entre las características de las edades de los trabajadores de la industria tecnológica a través de los años. Cada año contiene un dato atípico representado por la persona con mayor de edad en la industria. Las cajas están mas concentradas hacia el tercer cuartil, lo que podría estar indicando que la mayoría tiene edades más cercanas a ella.</p>', unsafe_allow_html=True)
