# Función para hacer la entrada más amigable
import numpy as np
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import funciones as fn
import plotly.graph_objects as go
import sympy as sp

def sec(x):
    return 1/np.cos(x)

def csc(x):
    return 1/np.sin(x)

def cot(x):
    return 1/np.tan(x)
def convertir_expresion(expr_str):
    reemplazos = {
        "sen": "sin",
        "arcsen": "asin",
        "arctg": "atan",
        "tg": "tan",
        "ctg": "cot",
        "sec": "sec",
        "csc": "csc",
        "ln": "log",
        "senh": "sinh",
        "tgh": "tanh",
        "cosh": "cosh",
        "pi": "pi",
        "e": "E"
    }
    x = sp.Symbol('x', real=True)
    for esp, eng in reemplazos.items():
        expr_str = expr_str.replace(esp, eng)

    try:
        expr_sym = sp.sympify(expr_str)
        expr_num = sp.lambdify((x, sp.Symbol('n')), expr_sym, 'numpy')
        return expr_num, expr_sym
    except Exception as e:
        st.error(f"Error al convertir la expresión '{expr_str}': {e}")
        return None, None
    
def evaluar_sympy(expr_str):
    try:
        expr_str = expr_str.replace("sen", "sin").replace("ln", "log")
        valor = sp.N(sp.sympify(expr_str))
        return float(valor)
    except Exception as e:
        st.error(f"Error al evaluar '{expr_str}': {e}")
        return None
def evaluar_sympy_a0(expr_str):
    try:
        expr_str = expr_str.replace("sen", "sin").replace("ln", "log")
        expr = sp.sympify(expr_str, evaluate=False)
        expr = sp.simplify(expr)
        return expr  # devolvemos expresión simbólica
    except Exception as e:
        st.error(f"Error al evaluar '{expr_str}': {e}")
        return None


