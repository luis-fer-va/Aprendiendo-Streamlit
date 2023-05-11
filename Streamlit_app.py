import streamlit as st 
import pandas as pd
import numpy as np 
import altair as alt

#Texto de encabezado
st.header('st.write')

#Crea un texto 'hello', un texto en cursiva 'world!' y una carita feliz, lista de emojis https://share.streamlit.io/streamlit/emoji-shortcodes .
st.write('hello,*world!* :sunglasses:')

#Mostrar numeros
st.write(1234)

#Mostrar dataframe
df=pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40]
     })

#Muestra el texto 'Below..' luego el df y finalmente el 'Above...'
st.write('Below is a Dataframe',df,'Above is a dataframe')

#Imprimir un grafico 
df2=pd.DataFrame(
     np.random.randn(200, 3),
     columns=['a', 'b', 'c'])

c=alt.Chart(df2).mark_circle().encode(
    x='a',y='b',size='c',color='c',tooltip=['a','b','c']
)

st.write(c)

#funcion markdown _convierte a cursiva_ , ** convierte a negrita
st.markdown('streamlit is _really_ **cool.**')
st.markdown(":green[Hola wey] :red[hola rojo] :violet[hola violeta] :+1:")

#Escribir texto en pantalla con otras funciones
st.caption("this is a string")
st.text('Otro string con la funcion text')

#Escribir codigo por pantalla
code='''
def hello():
    print("Hello, Streamlit")'''

st.code(code,language='python')