import pandas as pd
import numpy  as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly as px
import streamlit as st
import requests
from io import StringIO
import plotly.express as px
import requests
import sqlite3
import os
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


st.title("SQL")

@st.cache_resource
def iniciar_conexion():
    url = "https://raw.githubusercontent.com/Marizaf23/..."
    db_file = "mentalhealthti1.sqlite"
    
    # Solo descarga si el archivo no existe
    if not os.path.exists(db_file):
        response = requests.get(url)
        with open(db_file, "wb") as f:
            f.write(response.content)
            
    conn = sqlite3.connect(db_file, check_same_thread=False)
    return conn

# Llamas a la conexión así:
try:
    conn = iniciar_conexion()
    cur = conn.cursor()
except:
    st.error("Error al inicializar la base de datos.")
    st.stop()


st.header("Consulta 1")
st.subheader("Es de interés saber cuál año tuvo más encuestados, su género, la edad promedio, la edad mínima y la edad máxima para cada año, debe estar la descripción de la encuesta")

cur.execute("""
SELECT
    S.SurveyID AS "Año de la Encuesta",
    ROUND(AVG(CASE WHEN A2.AnswerText = 'Masculino' THEN CAST(A.AnswerText AS INTEGER) ELSE NULL END), 2) AS "Edad Promedio (MASC)",
    MIN(CASE WHEN A2.AnswerText = 'Masculino' THEN CAST(A.AnswerText AS INTEGER) ELSE NULL END) AS "Edad Mínima (MASC)",
    MAX(CASE WHEN A2.AnswerText = 'Masculino' THEN CAST(A.AnswerText AS INTEGER) ELSE NULL END) AS "Edad Máxima (MASC)",
				SUM(CASE WHEN A2.AnswerText = 'Masculino' THEN 1 ELSE 0 END) AS "Total Masculino",
    ROUND(AVG(CASE WHEN A2.AnswerText = 'Femenino' THEN CAST(A.AnswerText AS INTEGER) ELSE NULL END), 2) AS "Edad Promedio (FEM)",
    MIN(CASE WHEN A2.AnswerText = 'Femenino' THEN CAST(A.AnswerText AS INTEGER) ELSE NULL END) AS "Edad Mínima (FEM)",
    MAX(CASE WHEN A2.AnswerText = 'Femenino' THEN CAST(A.AnswerText AS INTEGER) ELSE NULL END) AS "Edad Máxima (FEM)",
				SUM(CASE WHEN A2.AnswerText = 'Femenino' THEN 1 ELSE 0 END) AS "Total Femenino",
    ROUND(AVG(CASE WHEN A2.AnswerText = 'Otro' THEN CAST(A.AnswerText AS INTEGER) ELSE NULL END), 2) AS "Edad Promedio (Otro)",
    MIN(CASE WHEN A2.AnswerText = 'Otro' THEN CAST(A.AnswerText AS INTEGER) ELSE NULL END) AS "Edad Mínima (Otro)",
    MAX(CASE WHEN A2.AnswerText = 'Otro' THEN CAST(A.AnswerText AS INTEGER) ELSE NULL END) AS "Edad Máxima (Otro)",
				SUM(CASE WHEN A2.AnswerText = 'Otro' THEN 1 ELSE 0 END) AS "Total Otro",
    COUNT(DISTINCT A.UserID) AS "Total de Encuestados"
FROM Respuestas A
JOIN Survey S ON A.SurveyID = S.SurveyID
JOIN Respuestas A2 ON S.SurveyID = A2.SurveyID AND A2.QuestionID = 2 AND A2.UserID = A.UserID
WHERE A.QuestionID = 1
GROUP BY S.SurveyID;
""")

# Recuperación de los resultados en un Dataframe
Consulta1 = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

st.dataframe(Consulta1)

st.header("Consulta 2")
st.subheader("Se requiere indagar si se puede observar cuántas personas se sienten cómodas hablando de sus problemas mentales con sus compañeros y supervisores")

cur.execute("""
SELECT 
  CASE 
    WHEN R1.questionid = 18 THEN 'Compañeros' 
    WHEN R1.questionid = 19 THEN 'Supervisores' 
  END AS 'Comodidad para Hablar', 
  COUNT(DISTINCT R1.userid) AS 'Cantidad de Personas'
FROM 
  Respuestas R1
WHERE 
  R1.questionid IN (18, 19) AND R1.AnswerText = 'Si'
GROUP BY 
  CASE 
    WHEN R1.questionid = 18 THEN 'Compañeros' 
    WHEN R1.questionid = 19 THEN 'Supervisores' 
  END
UNION ALL
SELECT 
  'Total', 
  SUM(sub.Cantidad_de_Personas)
FROM 
  (
    SELECT 
      COUNT(DISTINCT R1.userid) AS Cantidad_de_Personas
    FROM 
      Respuestas R1
    WHERE 
      R1.questionid IN (18, 19) AND R1.AnswerText = 'Si'
    GROUP BY 
      CASE 
        WHEN R1.questionid = 18 THEN 'Compañeros' 
        WHEN R1.questionid = 19 THEN 'Supervisores' 
      END
  ) sub
""")

# Recuperación de los resultados en un Dataframe
Consulta2 = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

st.dataframe(Consulta2)

st.header("Consulta 3")
st.subheader("Es de interés indagar si las empresas con más de 100 empleados tienen mayor cantidad de personas con problemas de salud mental, ¿Estas empresas tienen algún plan o apoyo para estos empleados?")

cur.execute("""
WITH
  "Empresas con más de 100 Empleados" AS (
    SELECT R1.AnswerText AS 'Tamaño de la Empresa', COUNT(DISTINCT R2.userid) AS "Empleados con Enfermedades Mentales"
    FROM Respuestas R1
    INNER JOIN Respuestas R2 ON R1.userid = R2.userid
    WHERE R1.questionid = 8 AND R1.AnswerText IN ('100-500', '500-1000', 'Más de 1000')
    AND R2.questionid = 34 AND R2.AnswerText = 'Si'
    GROUP BY R1.AnswerText
),
"Conoce del Apoyo" AS (
SELECT 
  R3.AnswerText AS "Tamaño de la Empresa", 
  COUNT(DISTINCT R1.userid) AS "Empleados con Enfermedades Mentales"
FROM 
  Respuestas R1
  INNER JOIN Respuestas R2 ON R1.userid = R2.userid
  INNER JOIN Respuestas R3 ON R1.userid = R3.userid
WHERE 
  R1.questionid = 14 AND R1.AnswerText = 'Si'
  AND R2.questionid = 34 AND R2.AnswerText = 'Si'
  AND R3.questionid = 8 AND R3.AnswerText IN ('100-500', '500-1000', 'Más de 1000')
GROUP BY 
  R3.AnswerText
),
"No Conoce del Apoyo" AS (
SELECT 
  R3.AnswerText AS "Tamaño de la Empresa", 
  COUNT(DISTINCT R1.userid) AS "Empleados con Enfermedades Mentales"
FROM 
  Respuestas R1
  INNER JOIN Respuestas R2 ON R1.userid = R2.userid
  INNER JOIN Respuestas R3 ON R1.userid = R3.userid
WHERE 
  R1.questionid = 14 AND R1.AnswerText = 'No'
  AND R2.questionid = 34 AND R2.AnswerText = 'Si'
  AND R3.questionid = 8 AND R3.AnswerText IN ('100-500', '500-1000', 'Más de 1000')
GROUP BY 
  R3.AnswerText
)

SELECT 
  e."Tamaño de la Empresa", 
  a."Empleados con Enfermedades Mentales" AS "Conoce del Apoyo", 
  na."Empleados con Enfermedades Mentales" AS "No Conoce del Apoyo", 
  e."Empleados con Enfermedades Mentales" - COALESCE(a."Empleados con Enfermedades Mentales", 0) - COALESCE(na."Empleados con Enfermedades Mentales", 0) AS "No Sabe",
  e."Empleados con Enfermedades Mentales"
FROM 
  "Empresas con más de 100 Empleados" e
LEFT JOIN "Conoce del Apoyo" a ON e."Tamaño de la Empresa" = a."Tamaño de la Empresa"
LEFT JOIN "No Conoce del Apoyo" na ON e."Tamaño de la Empresa" = na."Tamaño de la Empresa"

UNION ALL

SELECT 
  'Total', 
  SUM(a."Empleados con Enfermedades Mentales") AS "Conoce del Apoyo", 
  SUM(na."Empleados con Enfermedades Mentales") AS "No Conoce del Apoyo", 
  SUM(e."Empleados con Enfermedades Mentales" - COALESCE(a."Empleados con Enfermedades Mentales", 0) - COALESCE(na."Empleados con Enfermedades Mentales", 0)) AS "No Sabe",
  SUM(e."Empleados con Enfermedades Mentales")
FROM 
  "Empresas con más de 100 Empleados" e
LEFT JOIN "Conoce del Apoyo" a ON e."Tamaño de la Empresa" = a."Tamaño de la Empresa"
LEFT JOIN "No Conoce del Apoyo" na ON e."Tamaño de la Empresa" = na."Tamaño de la Empresa"
""")

# Recuperación de los resultados en un Dataframe
Consulta3 = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

st.write("NOTA: SE REALIZÓ LA COLUMNA 'NO SABE' MEDIANTE UNA DIFERENCIA DEBIDO A QUE EXISTÍAN VALORES NULOS Y -1 QUE AL HACER EL UPDATE FUERON ELIMINADOS, POR ESTO NO HACÍA EL CONTEO COMPLETO")

st.write("NOTA: NO SE PUDO AGREGAR LA QUESTION_ID 94 PARA EVALUAR OTROS OPOYOS DEBIDO A QUE ESTA PREGUNTA SOLO SE RESPONDE EN SURVEY_ID 2014 Y NO TIENE RELACION ALGUNA CON LA PREGUNTA DE LAS ENFERMEDADES MENTALES")

st.dataframe(Consulta3)

st.header("Consulta 4")
st.subheader("Según los diferentes periodos de la encuesta existe un cambio significativo para el género según la industria tecnológica. ¿En cantidad y por año quienes se declararon con problemas mentales?")

cur.execute("""
SELECT 
  R3.AnswerText AS 'Puesto de Trabajo',
  SUM(CASE WHEN R1.AnswerText = 'Femenino' AND R2.AnswerText = 'Si' THEN 1 ELSE 0 END) AS 'Femenino con Enfermedad Mental',
  SUM(CASE WHEN R1.AnswerText = 'Masculino' AND R2.AnswerText = 'Si' THEN 1 ELSE 0 END) AS 'Masculino con Enfermedad Mental',
  SUM(CASE WHEN R1.AnswerText = 'Otro' AND R2.AnswerText = 'Si' THEN 1 ELSE 0 END) AS 'Otro con Enfermedad Mental',
  SUM(CASE WHEN R2.AnswerText = 'Si' THEN 1 ELSE 0 END) AS 'Total'
FROM 
  Respuestas R1
  INNER JOIN Respuestas R2 ON R1.userid = R2.userid
  INNER JOIN Respuestas R3 ON R1.userid = R3.userid
WHERE 
  R1.questionid = 2
  AND R2.questionid = 34
  AND R3.questionid = 117
GROUP BY 
  R3.AnswerText

UNION ALL

SELECT 
  'Total',
  SUM(CASE WHEN R1.AnswerText = 'Femenino' AND R2.AnswerText = 'Si' THEN 1 ELSE 0 END),
  SUM(CASE WHEN R1.AnswerText = 'Masculino' AND R2.AnswerText = 'Si' THEN 1 ELSE 0 END),
  SUM(CASE WHEN R1.AnswerText = 'Otro' AND R2.AnswerText = 'Si' THEN 1 ELSE 0 END),
  SUM(CASE WHEN R2.AnswerText = 'Si' THEN 1 ELSE 0 END)
FROM 
  Respuestas R1
  INNER JOIN Respuestas R2 ON R1.userid = R2.userid
  INNER JOIN Respuestas R3 ON R1.userid = R3.userid
WHERE 
  R1.questionid = 2
  AND R2.questionid = 34
  AND R3.questionid = 117
""")

# Recuperación de los resultados en un Dataframe
Consulta4 = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

st.write("NOTA: NO EXISTE PREGUNTA QUE RESPONDA EL TIPO DE INDUSTRIA TECNOLÓGICA ASÍ QUE SE TOMÓ PUESTO DE TRABAJO COMO VARIABLE PARA REALIZAR LA CONSULTA")
		
st.write("NOTA: NO SE PUDO CALCULAR EL INCREMENTO POR AÑO SEGÚN LOS PERIODOS DE TIEMPO PORQUE LA PREGUNTA DE LOS PUESTOS DE TRABAJO SÓLO SE RESPONDE EN EL SURVEY_ID 2016")

st.dataframe(Consulta4)

st.header("Consulta 5")
st.subheader("Se requiere saber si se ha normalizado la aceptación de los problemas mentales para los diferentes años de la encuesta y ha cambiado su tendencia con respecto a la opinión de la efectividad laboral al momento de declarar que se posee una enfermedad mental")

cur.execute("""
SELECT 
  R1.SurveyID AS Año,
  SUM(CASE 
    WHEN R1.questionid = 114 AND R1.AnswerText IN ('No, no lo hacen', 'No, pienso que no lo harían') THEN 1
    WHEN R1.questionid = 102 AND R1.AnswerText = 'No' THEN 1
    WHEN R1.questionid = 81 AND R1.AnswerText IN ('Me apoya(n) mucho', 'Bien', 'Muy bien', 'Me entiende(n)', 'Me apoya(n)') THEN 1
    ELSE 0
  END) AS Aceptación,
  SUM(CASE 
    WHEN R1.questionid = 114 AND R1.AnswerText IN ('Tal vez', 'Si lo hacen', 'Si, pienso que lo harían') THEN 1
    WHEN R1.questionid = 81 AND R1.AnswerText IN ('Normal', 'No creo que le(s) importe', 'Sin comentarios', 'Muy mal', 'Indiferente', 'Mal') THEN 1
    WHEN R1.questionid = 102 AND R1.AnswerText = 'Si' THEN 1
    ELSE 0
  END) AS "No Aceptación",
  R2."Personas Efectivas con Enfermedad Mental",
  R2."Personas No Efectivas con Enfermedad Mental",
  R2."Personas con Enfermedad Mental"
FROM 
  Respuestas R1
JOIN (
  SELECT 
    SurveyID,
    COUNT(DISTINCT UserID) AS "Personas con Enfermedad Mental",
    COUNT(DISTINCT CASE 
      WHEN (questionid = 92 AND AnswerText IN ('Raramente', 'A veces', 'Nunca')) 
         OR (questionid = 49 AND AnswerText IN ('A veces', 'Raramente', 'A menudo', 'Nunca'))
      THEN UserID
    END) AS "Personas Efectivas con Enfermedad Mental",
    COUNT(DISTINCT UserID) - COUNT(DISTINCT CASE 
      WHEN (questionid = 92 AND AnswerText IN ('Raramente', 'A veces', 'Nunca')) 
         OR (questionid = 49 AND AnswerText IN ('A veces', 'Raramente', 'A menudo', 'Nunca'))
      THEN UserID
    END) AS "Personas No Efectivas con Enfermedad Mental"
  FROM 
    Respuestas
  WHERE 
    (UserID IN (
      SELECT UserID
      FROM Respuestas 
      WHERE questionid = 7 AND AnswerText = 'Si' AND SurveyID = 2014
    ) 
    OR 
    UserID IN (
      SELECT UserID
      FROM Respuestas 
      WHERE questionid = 34 AND AnswerText = 'Si' AND SurveyID IN (2016, 2017, 2018, 2019)
    ))
    AND SurveyID IN (2014, 2016, 2017, 2018, 2019)
  GROUP BY 
    SurveyID
) R2 ON R1.SurveyID = R2.SurveyID
WHERE 
  R1.SurveyID IN (2014, 2016, 2017, 2018, 2019) 
  AND R1.UserID IN (
    SELECT UserID
    FROM Respuestas 
    WHERE questionid IN (114, 102, 81)
    GROUP BY UserID 
  )
GROUP BY 
  R1.SurveyID, R2."Personas Efectivas con Enfermedad Mental", R2."Personas No Efectivas con Enfermedad Mental", R2."Personas con Enfermedad Mental"
UNION ALL
SELECT 
  'Total' AS Año,
  SUM(Aceptación) AS Aceptación,
  SUM("No Aceptación") AS "No Aceptación",
  SUM("Personas Efectivas con Enfermedad Mental") AS "Personas Efectivas con Enfermedad Mental",
  SUM("Personas No Efectivas con Enfermedad Mental") AS "Personas No Efectivas con Enfermedad Mental",
  SUM("Personas con Enfermedad Mental") AS "Personas con Enfermedad Mental"
FROM (
  SELECT 
    R1.SurveyID AS Año,
    SUM(CASE 
      WHEN R1.questionid = 114 AND R1.AnswerText IN ('No, no lo hacen', 'No, pienso que no lo harían') THEN 1
      WHEN R1.questionid = 102 AND R1.AnswerText = 'No' THEN 1
      WHEN R1.questionid = 81 AND R1.AnswerText IN ('Me apoya(n) mucho', 'Bien', 'Muy bien', 'Me entiende(n)', 'Me apoya(n)') THEN 1
      ELSE 0
    END) AS Aceptación,
    SUM(CASE 
      WHEN R1.questionid = 114 AND R1.AnswerText IN ('Tal vez', 'Si lo hacen', 'Si, pienso que lo harían') THEN 1
      WHEN R1.questionid = 81 AND R1.AnswerText IN ('Normal', 'No creo que le(s) importe', 'Sin comentarios', 'Muy mal', 'Indiferente', 'Mal') THEN 1
      WHEN R1.questionid = 102 AND R1.AnswerText = 'Si' THEN 1
      ELSE 0
    END) AS "No Aceptación",
    R2."Personas Efectivas con Enfermedad Mental",
    R2."Personas No Efectivas con Enfermedad Mental",
    R2."Personas con Enfermedad Mental"
  FROM 
    Respuestas R1
  JOIN (
    SELECT 
      SurveyID,
      COUNT(DISTINCT UserID) AS "Personas con Enfermedad Mental",
      COUNT(DISTINCT CASE 
        WHEN (questionid = 92 AND AnswerText IN ('Raramente', 'A veces', 'Nunca')) 
           OR (questionid = 49 AND AnswerText IN ('A veces', 'Raramente', 'A menudo', 'Nunca'))
        THEN UserID
      END) AS "Personas Efectivas con Enfermedad Mental",
      COUNT(DISTINCT UserID) - COUNT(DISTINCT CASE 
        WHEN (questionid = 92 AND AnswerText IN ('Raramente', 'A veces', 'Nunca')) 
           OR (questionid = 49 AND AnswerText IN ('A veces', 'Raramente', 'A menudo', 'Nunca'))
        THEN UserID
      END) AS "Personas No Efectivas con Enfermedad Mental"
    FROM 
      Respuestas
    WHERE 
      (UserID IN (
        SELECT UserID
        FROM Respuestas 
        WHERE questionid = 7 AND AnswerText = 'Si' AND SurveyID = 2014
      ) 
      OR 
      UserID IN (
        SELECT UserID
        FROM Respuestas 
        WHERE questionid = 34 AND AnswerText = 'Si' AND SurveyID IN (2016, 2017, 2018, 2019)
      ))
      AND SurveyID IN (2014, 2016, 2017, 2018, 2019)
    GROUP BY 
      SurveyID
  ) R2 ON R1.SurveyID = R2.SurveyID
  WHERE 
    R1.SurveyID IN (2014, 2016, 2017, 2018, 2019) 
    AND R1.UserID IN (
      SELECT UserID
      FROM Respuestas 
      WHERE questionid IN (114, 102, 81)
      GROUP BY UserID 
    )
  GROUP BY 
    R1.SurveyID, R2."Personas Efectivas con Enfermedad Mental", R2."Personas No Efectivas con Enfermedad Mental", R2."Personas con Enfermedad Mental"
) AS subquery
""")

# Recuperación de los resultados en un Dataframe
Consulta5 = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

st.write("NOTA: SE ESCOGEN LAS PREGUNTAS 81, 102 Y 114 PARA RESPONDER EL APARTADO DE ACEPTACIÓN Y LUEGO HACER LA COMPARATIVA DE TODOS LOS AÑOS")

st.write("NOTA: EN EL CASO DE LAS PERSONAS CON ENFERMEDAD MENTAL Y SU EFECTIVIDAD, SE USARON LAS PREGUNTAS 48, 49 Y 92")

st.dataframe(Consulta5)

conn.close()

st.write("Funciones aplicadas para realizar las consultas: CTE (Common Table Expressions), UNION ALL, Subquery")
