import streamlit as st
import numpy as np
import pandas as pd
import pickle

modelo = pickle.load(open('./data/modeloSerializado.pkl', 'rb'))
scaler = pickle.load(open('./data/scalerSerializado.pkl', 'rb'))
# pickle.dump(finalModel, open('modeloSerializado.pkl', 'wb'))
# pickle.dump(finalScaler, open('scalerSerializado.pkl', 'wb'))


def loan_score_generator(prediction_probability):
  min_prob_limit = 0.0000000001
  max_prob_limit = 0.9999999999
  min_score = 300
  max_score = 850
  conversion_factor = (max_score - min_score) / (max_prob_limit - min_prob_limit)
  return int((prediction_probability - min_prob_limit) * conversion_factor + min_score)

# '''
# Función para mapear person_home_ownership
# '''
def sut_d(person_home_ownership):
  if person_home_ownership == 'RENT':
    return 0
  elif person_home_ownership == 'OWN':
    return 1
  elif person_home_ownership == 'MORTGAGE':
    return 2
  elif person_home_ownership == 'OTHER':
    return 3

# '''
# Función para mapear loan_intent
# '''
def sut_g(loan_intent):
  if loan_intent == 'PERSONAL':
    return 0
  elif loan_intent == 'EDUCATION':
    return 1
  elif loan_intent == 'MEDICAL':
    return 2
  elif loan_intent == 'VENTURE':
    return 3
  elif loan_intent == 'HOMEIMPROVEMENT':
    return 4
  elif loan_intent ==  'DEBTCONSOLIDATION':
    return 5

# '''
# Función para mapear cb_person_default_on_file
# '''
def sut_a(cb_person_default_on_file):
  if cb_person_default_on_file == 'N':
    return 0
  elif cb_person_default_on_file == 'Y':
    return 1

# '''
# Función para procesar los inputs con sus tipos de datos adecuados.
# Retorna el Score como 0 o 1
# '''
def process_inputs():
  person_age = int(input_person_age)
  person_income = int(input_person_income)
  person_home_ownership = int(sut_d(input_person_home_ownership))
  person_emp_length = float(input_person_emp_length)
  loan_intent = int(sut_g(input_loan_intent))
  loan_amnt = int(input_loan_amnt)
  loan_int_rate = float(input_loan_int_rate)
  cb_person_default_on_file = 0 #int(sut_a(input_cb_person_default_on_file))

  x_data_0 = [[
    person_age,
    person_income,
    person_home_ownership,
    person_emp_length,
    loan_intent,
    0, #loan_grade 5
    loan_amnt,
    loan_int_rate,
    0, #loan_status 8
    0, #loan_percent_income 9
    cb_person_default_on_file
  ]]
  x_data_1 = scaler.transform(x_data_0)
  x_data = x_data_1[:, [0, 1, 2, 3, 4, 6, 7, 10]]


  print(x_data_0)
  print(x_data)

  probabilidad = modelo.predict_proba(x_data)[0][1]
  score = loan_score_generator(probabilidad)
  print(probabilidad, score)
  return score


####################
### INTRODUCTION ###
####################

acc = 0

####################

col1, col2 = st.columns(2)
mainTitle = st.empty()

with col1:
  mainTitle.title('Llena los datos para conocer tu resultado')
st.video('https://www.youtube.com/watch?v=E3AGEPO8xBs')



###############
### SIDEBAR ###
###############

st.sidebar.title('Super App para conseguir crédito!')
st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')

input_person_age = st.sidebar.number_input("Edad", 18, 90)
input_person_income = st.sidebar.number_input("Ingreso anual (USD)", 0)
input_person_emp_length = st.sidebar.number_input("Tiempo en empleo (Años)", 0, 72)
input_loan_amnt = st.sidebar.number_input("Monto del crédito (USD)", 1)
input_loan_int_rate = st.sidebar.number_input("Tasa de interés (0.00% - 100.00%)", 0.0, 100.0)
input_person_home_ownership = st.sidebar.selectbox('Tipo de vivienda', ['RENT', 'OWN', 'MORTGAGE', 'OTHER'])
input_loan_intent = st.sidebar.selectbox('Destino del crédito', ['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION'])
# input_cb_person_default_on_file = st.sidebar.selectbox('¿Ha incurrido en mora?', ['N','Y'])

if st.sidebar.button('Voy a tener suerte!'):
  acc = process_inputs()
  print(acc)
  if acc > 500:
    with col1:
      mainTitle.title(':green[Felicitaciones! puedes pedir tu crédito!]')
      st.subheader(f'{acc}')
  else:
    with col1:
      mainTitle.title(':red[Lamentablemente, aún no puedes solicitar un crédito]')
      st.subheader(f'{acc}')

with st.expander('¿Qué es el Score crediticio?'):
  st.write('El score crediticio es una evaluación numérica que representa la solvencia crediticia de un individuo o entidad. Calculado por agencias de crédito, este puntaje se basa en la información de historial crediticio, incluyendo préstamos, tarjetas de crédito y otros compromisos financieros. El objetivo es proporcionar a los prestamistas una rápida y cuantificable medida del riesgo asociado a otorgar crédito a una persona específica. Un score crediticio más alto sugiere una mayor confiabilidad y capacidad de pago, mientras que un puntaje más bajo indica un mayor riesgo crediticio. Este puntaje influye significativamente en la capacidad de obtener préstamos y créditos, así como en las tasas de interés asociadas a los mismos.')
st.link_button('Ir al reporte técnico', 'https://unal-fundamentos-analitica-g1-2023-2s.github.io/Analitica-Modelos-de-riesgo-de-credito/')
