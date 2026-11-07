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
st.header("Pregunta 1")
st.subheader('¿Cuántas personas en la industria tecnológica tienen una enfermedad mental diagnosticada y, dentro de este grupo, existe algún antecedente heredofamiliar dentro de este ámbito?')


# Crea un selectbox con las opciones
option = st.selectbox('Año de Encuesta:', ['Todos','2016', '2017', '2018', '2019'])

if option == 'Todos':
        st.subheader("Gráfica de personas que respondieron la pregunta de enfermedades mentales por año")
    
        data_total1 = {
        2016: [366, 473, 0],
        2017: [4, 244, 249],
        2018: [2, 159, 151],
        2019: [1, 106, 97],
        }

        df_total1 = pd.DataFrame(data_total1,
                index=['No tengo enfermedades mentales', 'Tengo enfermedades mentales', 'No respondió'])

        number_of_bars = len(df_total1.columns)

        fig_total1, axs = plt.subplots(nrows=1, ncols=number_of_bars, figsize=(8,6))

        colors = ['#003d99', '#0066ff', '#6666ff']

        for i, ax in enumerate(axs):
            col_name = df_total1.columns[i]
            values = df_total1[col_name]
    
            total = sum(values)
            normalized_values = [v/total for v in values]
    
            Waffle.make_waffle(
                ax=ax,
                rows=20,
                columns=5,
                values=normalized_values,
                colors=colors
                )

            ax.set_title(str(col_name), fontsize=14)

        legend_handles = [plt.Line2D([0], [0], marker='s', color='w', label='No tengo enfermedades mentales', markerfacecolor=colors[0], markersize=12),
                    plt.Line2D([0], [0], marker='s', color='w', label='Tengo enfermedades mentales', markerfacecolor=colors[1], markersize=12),
                    plt.Line2D([0], [0], marker='s', color='w', label='No respondió', markerfacecolor=colors[2], markersize=12)]

        fig_total1.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3)

        plt.tight_layout(rect=[0, 0, 1, 0.85])

        fig_total1.set_size_inches(10, 4) 
        st.pyplot(fig_total1)

        st.subheader("Gráfica de personas que respondieron la pregunta de antecedentes heredofamiliares por año")

        data_total2 = {
        2016: [240, 453, 146 ],
        2017: [111, 251, 135],
        2018: [71, 172, 69],
        2019: [44, 115, 45],
        }

        df_total2 = pd.DataFrame(data_total2,
                index=['No tengo antecedentes heredofamiliares', 'Tengo antecedentes heredofamiliares', 'No conozco mis antecedentes heredofamiliares'])

        number_of_bars = len(df_total2.columns)

        fig_total2, axs = plt.subplots(nrows=1, ncols=number_of_bars, figsize=(12,8))

        colors = ['#290066', '#5c00e6', '#944dff']

        for i, ax in enumerate(axs):
            col_name = df_total2.columns[i]
            values = df_total2[col_name]
    
            total = sum(values)
            normalized_values = [v/total for v in values]
    
            Waffle.make_waffle(
                ax=ax,
                rows=20,
                columns=5,
                values=normalized_values,
                colors=colors
                )

            ax.set_title(str(col_name), fontsize=14)

        legend_handles = [plt.Line2D([0], [0], marker='s', color='w', label='No tengo antecedentes heredofamiliares', markerfacecolor=colors[0], markersize=12),
                        plt.Line2D([0], [0], marker='s', color='w', label='Tengo antecedentes heredofamiliares', markerfacecolor=colors[1], markersize=12),
                        plt.Line2D([0], [0], marker='s', color='w', label='No conozco mis antecedentes heredofamiliares', markerfacecolor=colors[2], markersize=12)]

        fig_total2.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=2)
        
        plt.tight_layout(rect=[0, 0, 1, 0.85])

        fig_total2.set_size_inches(10, 4) 
        st.pyplot(fig_total2)

        st.write("""
            <p style="text-align: justify;">
                <ul>
                    <li>En la primera gráfica de waffle se ve representado el porcentaje de personas a través de los años y su respuesta a la pregunta de si tienen una enfermedad mental diagnosticada o no. Se puede observar con claridad que el porcentaje de personas con enfermedades mentales no varía mucho (52%-56%) y el porcentaje que va aumentando a través de los años es el de personas que no contestan la interrogante.</li>
                    <li>En la segunda gráfica de waffle se ve representado el porcentaje de personas con antecedentes heredofamiliares a través de los años. El mayor porcentaje de personas tiene antecedentes de enfermedades mentales con un resgistro de entre el 51% (2017) y 58% (2018). Esto podría estar directamente relacionado con la pregunta anterior.</li>
                </ul>
            </p>
        """, unsafe_allow_html=True)

elif option == '2016':

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

    # Crear la figura
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[170, 76, 120],
        name='No tengo enfermedades mentales',
        orientation='h',
        marker=dict(
        color='rgb(77, 148, 255)',
        line=dict(color='rgb(77, 148, 255)', width=2)
        )
        ))
    fig.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[70, 70, 333],
        name='Tengo enfermedades mentales',
        orientation='h',
        marker=dict(
        color='rgb(0, 102, 255)',
        line=dict(color='rgb(0, 102, 255)', width=2)
        )
        ))

    fig.update_layout(
    barmode='stack',
    font=dict(
        color='rgb(0, 0, 0)'
        )
        )

    # Mostrar la figura en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>Como anteriormente se suponía, el mayor número de personas con enfermedades mentales tiene antecedentes heredofamiliares con 333 registros.</li>
                <li>Aunque hay 473 personas con enfermedades mentales registradas en el 2016, no existe mucha diferencia entre esta cifra y la correspondiente a las personas que no tienen enfermedades mentales (366 respuestas).</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)

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

    # Crear la figura
    fig2017_1 = go.Figure()

    fig2017_1.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[0, 1, 3],
        name='No tengo enfermedades mentales',
        orientation='h',
        marker=dict(
        color='rgb(0, 61, 153)',
        line=dict(color='rgb(0, 61, 153)', width=2)
        )   
        ))

    fig2017_1.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[26, 55, 163],
        name='Tengo enfermedades mentales',
        orientation='h',
        marker=dict(
        color='rgb(77, 148, 255)',
        line=dict(color='rgb(77, 148, 255)', width=2)
        )
        ))

    fig2017_1.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[85, 79, 85],
        name='No respondio',
        orientation='h',
    marker=dict(
        color='rgb(0, 102, 255)',
        line=dict(color='rgb(0, 102, 255)', width=2)
        )
        ))

    fig2017_1.update_layout(barmode='stack')

    # Mostrar la figura en Streamlit
    st.plotly_chart(fig2017_1, use_container_width=True)

    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>En el 2017 se mantiene la situación con 163 personas en la industria tecnólogica con enfermedades mentales y antecedentes heredofamiliares.</li>
                <li>Se puede evidenciar el aumento personas que no contestan la pregunta de enfermedades mentales . Esto podría deberse al estigma.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)

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

    # Crear la figura
    fig2018_1 = go.Figure()

    fig2018_1.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[1, 0, 1],
        name='No tengo enfermedades mentales',
        orientation='h',
        marker=dict(
        color='rgb(0, 61, 153)',
        line=dict(color='rgb(0, 61, 153)', width=2)
        )   
        ))

    fig2018_1.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[11, 35, 113],
        name='Tengo enfermedades mentales',
        orientation='h',
        marker=dict(
        color='rgb(77, 148, 255)',
        line=dict(color='rgb(77, 148, 255)', width=2)
        )
        ))

    fig2018_1.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[59, 34, 58],
        name='No respondio',
        orientation='h',
    marker=dict(
        color='rgb(0, 102, 255)',
        line=dict(color='rgb(0, 102, 255)', width=2)
        )
        ))

    fig2018_1.update_layout(barmode='stack')

    # Mostrar la figura en Streamlit
    st.plotly_chart(fig2018_1, use_container_width=True)

    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>Para el 2018, el mayor número de individuos en la industria tecnólogica tiene enfermedades mentales y antecedentes heredofamiliares con 113 respuestas, seguido por las 59 personas que no tienen antecedentes y a su vez no contestaron la pregunta.</li>
                <li>Aquí la cantidad de personas que no respondieron la pregunta disminuye al igual que la cantidad que contestó la encuesta en comparación con los años anteriores. Sin embargo, la proporción sigue siendo muy alta pues casi un 50% no contestó la interrogante.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)

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

            # Crear la figura
    fig2019_1 = go.Figure()

    fig2019_1.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[0, 1, 0],
        name='No tengo enfermedades mentales',
        orientation='h',
        marker=dict(
        color='rgb(0, 61, 153)',
        line=dict(color='rgb(0, 61, 153)', width=2)
        )   
        ))

    fig2019_1.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[9, 25, 72],
        name='Tengo enfermedades mentales',
        orientation='h',
        marker=dict(
        color='rgb(77, 148, 255)',
        line=dict(color='rgb(77, 148, 255)', width=2)
        )
        ))

    fig2019_1.add_trace(go.Bar(
        y=['No tengo antecedentes heredofamiliares', 'No conozco mis antecedentes familiares', 'Tengo antecedentes familiares'],
        x=[35, 19, 43],
        name='No respondio',
        orientation='h',
    marker=dict(
        color='rgb(0, 102, 255)',
        line=dict(color='rgb(0, 102, 255)', width=2)
        )
        ))

    fig2019_1.update_layout(barmode='stack')

    # Mostrar la figura en Streamlit
    st.plotly_chart(fig2019_1, use_container_width=True)

    st.write("""
        <p style="text-align: justify;">
            <ul>
                <li>El 2019 es el año con menor cantidad de personas en la industria tecnológica que contestaron la encuesta con una muestra de 204 individuos.</li>
                <li>El número de personas que no tienen enfermedades mentales disminuye al mínimo con una sola respuesta. Ya observando la ocurrencia de todos los años en la investigación, se puede decir que normalmente las personas con enfermedades mentales diagnosticadas tienen algún antecedente heredofamiliar en este ámbito.</li>
            </ul>
        </p>
    """, unsafe_allow_html=True)
