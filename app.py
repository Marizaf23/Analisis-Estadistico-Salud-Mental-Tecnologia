# %%
import pandas as pd
import numpy  as np
import sqlite3
import streamlit as st
import seaborn   as sns
import matplotlib.pyplot as plt

# Conectar a la base de datos SQLite
conn = sqlite3.connect(r'C:\Users\maria\Documents\UCV MARY\EECA\SEMESTRE 2024-1\SEMESTRE II\COMPUTACIÓN II\TRABAJO FINAL\SALUD MENTAL EN LA INDUSTRIA TECNOLÓGICA 1.sqlite')

cur = conn.cursor()

# %%
# Consultar las tablas en la base de datos
consulta_ntablas = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"

# %%
# Crear consulta para convertir en DF
consulta = "SELECT * FROM Respuestas;"

df_Respuestas = pd.read_sql_query(sql = consulta, con = conn)

conn.close()

# %%
# Filtrado del DF por el año 2016 y Estados Unidos como País para realizar la Investigación
User_ID = df_Respuestas[(df_Respuestas['QuestionID'] == 3) & (df_Respuestas['AnswerText'] == 'Estados Unidos')]['UserID'].unique()

df_Investigacion = df_Respuestas[(df_Respuestas['UserID'].isin(User_ID)) & (df_Respuestas['SurveyID'] == 2016)]

# %%
# Reestructuración del DF para mejor uso de Pandas
df_Investigacion = df_Investigacion.groupby(['UserID', 'QuestionID'])['AnswerText'].first().reset_index()

df_Investigacion = df_Investigacion.pivot_table(index='UserID', columns='QuestionID', values='AnswerText', aggfunc='first')

# %%
# Renombrar las variables
print(df_Investigacion.columns)

df_Investigacion.columns = ['Edad', 'Género', 'País de Residencia', 'Ciudad de Residencia (EEUU)', 'Trabajo Autónomo', 'Historial Familiar', 'Búsqueda de Tratamiento con un Profesional', 'Cantidad de Empleados en la Empresa', 'Beneficios Dentro de Seguro Médico', 'Problemas de Salud Mental en Entrevista Laboral', 'Conocimiento de las Opciones de Cobertura por la Empresa Actual', 'Recursos de la Empresa Para Conocer sobre la Salud Mental y Canales de Ayuda', 'Facilidad de Consulta de Baja Médica en el Trabajo', 'Comodidad para Hablar de una Enfermedad Mental con Compañeros de Trabajo', 'Comodidad para Hablar de una Enfermedad Mental con un Director/Supervisor', 'Cobertura de Salud Mental en Seguro Médico', 'Beneficios de Salud Mental de Empleos Anteriores', 'Conocimiento de las Opciones de Ayuda por el Empleo Anterior', 'Protección de Anonimato Si Se Toma Ventaja de los Recursos de Tratamiento en Empleos Anteriores', 'Disposición de Hablar de Salud Mental con un Supervisor', 'Disposición para Hablar Sobre Enfermedad Mental con Familia/Amigos', 'Seguridad de Revelar Enfermedad Mental Debido a Comentario Sobre Salud Mental de Otra Persona', 'Situación Mental Actual', '¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?', 'Nivel de Interferencia en el Trabajo Cuando Se Está Bajo Tratamiento', 'Nivel de Interferencia en el Trabajo Cuando No Se Está Bajo Tratamiento', 'Disposición a Revelar Enfermedad Mental a Empleados/Compañeros', 'Productividad Afectada Por Enfermedad Mental', 'Porcentaje de Tiempo Afectada Por Enfermedad Mental', '¿Has Observado o Experimentado una Respuesta Insolidaria o Mal Gestionada a un Problema de Salud Mental en tu Lugar de Trabajo Actual o Anterior?', '¿Cree que los Miembros de su Equipo/Compañeros de Trabajo le Verían de Forma más Negativa Si Supieran que Padece una Enfermedad Mental?', 'Enfermedades Mentales Diagnosticadas', 'Enfermedades Mentales No Diagnosticadas', 'Puesto de Trabajo', 'Trabajo Remoto']

# %%
# Reemplazar los NaN

df_Investigacion = df_Investigacion.fillna('No respondió')


# %%
# Título de la aplicación
st.title("Problemáticas y Estigmas de las Enfermedades Mentales en la Industria Tecnológica Estadounidense en el Año 2016")

st.dataframe(df_Investigacion)

# Título de la aplicación
st.title("Análisis del Conjunto de Datos Iris")

st.write("""
## Introducción

""")

# %%

# PREGUNTA #1
#¿Cuántas personas en la industria tecnológica tienen una enfermedad mental diagnosticada y, dentro de este grupo, existe algún historial familiar dentro de este ámbito?

Pregunta1 = pd.crosstab(df_Investigacion['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'], df_Investigacion['Historial Familiar'], 
                              rownames=['Historial Familiar'], 
                              colnames=['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'])
print(Pregunta1.to_string())                            
pd.set_option('display.width', -1)
pd.set_option('display.max_columns', None)
print(Pregunta1)

# Agregar columna de totales
Pregunta1 = Pregunta1.assign(Total=Pregunta1.sum(axis=1))

# Agregar fila de totales
Pregunta1.loc['Total'] = Pregunta1.sum(axis=0)


# %%
Pregunta1 = pd.crosstab(df_Investigacion['¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'], 
                        df_Investigacion['Historial Familiar'], 
                        margins=True, 
                        margins_name='Total')

Pregunta1.index.name = 'Historial Familiar'
Pregunta1.columns.name = '¿Alguna Vez Has Sido Diagnosticado con una Enfermedad Mental?'

print(Pregunta1)

st.table(Pregunta1)