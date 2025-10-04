####
import os
def clc():
    os.system('cls' if os.name == 'nt' else 'clear')
clc()
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import funciones as fn
#
st.title("Graficadora de Series")

funciones = {
    "sin": np.sin,
    "sen": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "tg": np.tan,
    "exp": np.exp,
    "pi": np.pi,
    "sec": fn.sec,
    "csc": fn.csc,
    "cot": fn.cot,
    "sqrt": np.sqrt,
    "i": 1j
}

col1, col2 = st.columns([0.2,0.8])
# Parámetros de entrada
with col1:
    x_min = st.number_input("Extremo inferior del intervalo", value=-np.pi)
    x_max = st.number_input("Extremo superior del intervalo", value=np.pi)
    N = st.number_input("Número de términos (N)", min_value=1, value=5)
    a0 = st.number_input("Valor de a0/2", value=0.0)

# Expresión de la serie
#expr_cos = st.text_input("Expresión de los coeficientes coseno (en función de n y x)", value="(1/n)*np.cos(n*x)")
#expr_sin = st.text_input("Expresión de los coeficientes seno (en función de n y x)", value="(1/n)*np.sin(n*x)")
expr_serie = st.text_input("Expresión de la serie en función de x y n", value="(1/n)*cos(n*x)+(1/n)*sin(n*x)")
# Vector x
x = np.linspace(x_min, x_max, 1000)
y = np.ones_like(x,dtype=complex) * a0

# Construcción de la serie
for n in range(1, int(N)+1):
    try:
        y += eval(expr_serie, funciones, {"x": x, "n": n})
    except Exception as e:
        st.error(f"Error en la expresión: {e}")
        break

# Gráfico
with col2:
    fig, ax = plt.subplots()
    ax.plot(x, y.real, label=f"Serie con N={N}")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    #ax.legend()
    st.pyplot(fig)

st.markdown("**Algunas series:**")

st.code("""
-4/pi*(-1)**(n)/(2*n-1)*cos((2*n-1)*x)""")
st.code("""
sin(n*pi*x)/(n*pi)""")
st.code("""
4*sin((2*n-1)*x)/(pi*(2*n-1))""")
st.code("""
-2*sin(x*(2*n-1))/((2*n-1)*pi)""")
st.code("""
i*exp(i*n*2*pi*x)/(2*n*pi)""")


