import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time

modelo = pickle.load(open('./data/modeloSerializado.pkl', 'rb'))
scaler = pickle.load(open('./data/scalerSerializado.pkl', 'rb'))
# pickle.dump(modelo, open('modeloSerializado.pkl', 'wb'))
# pickle.dump(scaler, open('scalerSerializado.pkl', 'wb'))


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
  cb_person_default_on_file = int(sut_a(input_cb_person_default_on_file))

  x_data_0 = [[
    person_age,
    person_income,
    person_home_ownership,
    person_emp_length,
    loan_intent,
    loan_amnt,
    loan_int_rate,
    cb_person_default_on_file
  ]]

  x_data = scaler.transform(x_data_0)
  y_data = [0]
  #
  print(x_data_0)
  print(x_data)
  return modelo.score(x_data, y_data)


####################
### INTRODUCTION ###
####################

acc = 0

####################

col1, col2 = st.columns(2)
mainTitle = st.empty()

with col1:
  mainTitle.title('Llena los datos para conocer tu resultado')



###############
### SIDEBAR ###
###############

st.sidebar.title('Super App para conseguir crédito!')
st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')

input_person_age = st.sidebar.number_input("Edad", 18, 90)
input_person_income = st.sidebar.number_input("Ingreso anual", 0)
input_person_emp_length = st.sidebar.number_input("Tiempo en empleo", 0, 72)
input_loan_amnt = st.sidebar.number_input("Monto del crédito", 1)
input_loan_int_rate = st.sidebar.number_input("Tasa de interés", 0.0, 100.0)
input_person_home_ownership = st.sidebar.selectbox('Tipo de vivienda', ['RENT', 'OWN', 'MORTGAGE', 'OTHER'])
input_loan_intent = st.sidebar.selectbox('Destino del crédito', ['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION'])
input_cb_person_default_on_file = st.sidebar.selectbox('¿Ha incurrido en mora?', ['N','Y'])

if st.sidebar.button('Voy a tener suerte!'):
  acc = process_inputs()
  print(acc)
  if acc > 0.7:
    with col1:
      mainTitle.title(':green[Felicitaciones! puedes pedir tu crédito!]')
      st.subheader(f'{acc}')
  else:
    with col1:
      mainTitle.title(':red[Lamentablemente, aún no puedes solicitar un crédito]')
      st.subheader(f'{acc}')
