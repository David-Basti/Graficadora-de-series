#####
import os
def clc():
    os.system('cls' if os.name == 'nt' else 'clear')
clc()
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import funciones as fn
import plotly.graph_objects as go
import sympy as sp

st.set_page_config(
    page_title="Graficadora de Series de Fourier",
    layout="centered"
)

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
    "i": 1j,
    "senh": np.sinh,
    "sinh": np.sinh,
    "cosh": np.cosh,
    "tanh": np.tanh,
    "tgh": np.tanh,
    "asen": np.asin,
    "atg": np.atan,
    "acos": np.acos,
    "ln": np.log,
    "log": np.log
}

col1, col2, col3 = st.columns([0.25,0.25,0.5])
# Parámetros de entrada
with col1:
    expr_xmin = st.text_input("Extremo inferior", value="-pi")
    expr_xmax = st.text_input("Extremo superior", value="pi")
with col2:
    N = st.number_input("Número de términos (N)", min_value=1, value=5)
    expr_a0 = st.text_input("Valor de a0/2", value="0")
x_min = fn.evaluar_sympy(expr_xmin) or -np.pi
x_max = fn.evaluar_sympy(expr_xmax) or np.pi
a0 = fn.evaluar_sympy(expr_a0) or 0
a02=fn.evaluar_sympy_a0(expr_a0) or 0
# Expresión de la serie
x = sp.Symbol('x', real=True)
with col3:
    expr_serie = st.text_input("Expresión de la serie S_n(x)", value="(1/n)*cos(n*x)+(1/n)*sin(n*x)")
    expr_funcion2 = st.text_input("Expresión de g(x) / g(x)+a0/2+S_n(x)", value="0")
    expr_funcion = st.text_input("Expresión de h(x) / h(x)*(g(x)+a0/2+S_n(x))", value="1")
    

# Definimos el símbolo simbólico
x_sym = sp.Symbol('x', real=True)

# Vector de evaluación numérica
x_vals = np.linspace(x_min, x_max, 1000)

# Convertir expresiones del usuario (usando tus funciones auxiliares en fn.py)
# SÍMBOLO
serie_sym = fn.convertir_expresion_simbolica(expr_serie)
g_sym     = fn.convertir_expresion_simbolica(expr_funcion2)
h_sym     = fn.convertir_expresion_simbolica(expr_funcion)

# NUMÉRICA
serie_func = fn.convertir_expresion_numerica(expr_serie)
g_func     = fn.convertir_expresion_numerica(expr_funcion2)
h_func     = fn.convertir_expresion_numerica(expr_funcion)

# Mostrar expresiones simbólicas en LaTeX
n = sp.Symbol('n', integer=True)
S_N_sym = sp.Sum(serie_sym, (n, 1, N))  
st.latex(f"S_N(x) = {sp.latex(sp.nsimplify(h_sym*(a02+g_sym+S_N_sym)))}")
#st.latex(f"g(x) = {sp.latex(g_sym)}")

# Inicializar la serie con a₀/2
y = np.ones_like(x_vals, dtype=np.complex128) * a0

for n_val in range(1, int(N)+1):
    try:
        y += serie_func(x_vals, n_val)  # ya devuelve np.complex128
    except Exception as e:
        st.error(f"Error al evaluar la serie para n={n_val}: {e}")
        break

# Aplicar g(x)
try:
    g = g_func(x_vals,1)
    y = g + y
except Exception as e:
    st.error(f"Error en la fucnion g(x): {e}")
try:
    h = h_func(x_vals, 1)  # aunque no dependa de n, necesita el argumento
    y = h * y
except Exception as e:
    st.error(f"Error en la función h(x): {e}")

# ==== GRÁFICO CON PLOTLY ====

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x_vals,
    y=y.real,
    mode='lines',
    name=f"Serie con N={N}",
    hovertemplate="x = %{x:.3f}<br>f(x) = %{y:.3f}"
))

fig.update_layout(
    xaxis_title="x",
    yaxis_title="f(x)",
    hovermode="x unified",
    template="plotly_white",
    margin=dict(l=40, r=40, t=20, b=40)
)

st.plotly_chart(fig, use_container_width=True)

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
j*exp(j*n*2*pi*x)/(2*n*pi)""")
st.code("""
2*sen((2*n-1)*x)/(pi*(2*n-1))""")
st.code("""
(-1)**n*senh(6)/(36+pi**2*n**2)*(6*cos(n*pi*x/3)-n*pi*sen(n*pi*x/3))""")

