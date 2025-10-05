# Función para hacer la entrada más amigable
import numpy as np
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import funciones as fn
import plotly.graph_objects as go
import sympy as sp


# Funciones especiales numéricas
def sec(x): return 1/np.cos(x)
def csc(x): return 1/np.sin(x)
def cot(x): return 1/np.tan(x)

# ==== PARTE SIMBÓLICA ====
def convertir_expresion_simbolica(expr_str):
    """
    Convierte una expresión ingresada por el usuario a expresión simbólica de Sympy.
    - Reemplaza funciones comunes (sen, tg, ln, etc.)
    - Convierte j → I para números imaginarios
    - Mantiene pi, e, senh, tgh, cosh
    """
    reemplazos = {
        "sen":"sin",
        "arcsen":"asin",
        "arctg":"atan",
        "tg":"tan",
        "ctg":"cot",
        "sec":"sec",
        "csc":"csc",
        "ln":"log",
        "senh":"sinh",
        "tgh":"tanh",
        "cosh":"cosh",
        "pi":"pi",
        "e":"E",
        "j":"I"
    }

    for k, v in reemplazos.items():
        expr_str = expr_str.replace(k, v)

    try:
        expr = sp.sympify(expr_str, evaluate=False)
        return expr
    except Exception as e:
        st.error(f"Error simbólico al convertir '{expr_str}': {e}")
        return None

# ==== PARTE NUMÉRICA ====
def convertir_expresion_numerica(expr_str):
    reemplazos = {
        "sen":"sin","tg":"tan","senh":"sinh","tgh":"tanh",
        "ctg":"cot","sec":"sec","csc":"csc","ln":"log","pi":"np.pi","e":"np.e","j":"1j"
    }
    modules_num = [{"sin": np.sin, "cos": np.cos, "tan": np.tan,
                "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
                "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
                "sec": sec, "csc": csc, "cot": cot,
                "pi": np.pi, "I": 1j, "i": 1j,}, "numpy"]
    for k,v in reemplazos.items(): expr_str = expr_str.replace(k,v)
    try:
        def f(x,n):
            return eval(expr_str)
        return f
    except Exception as e:
        st.error(f"Error numérico '{expr_str}': {e}")
        return None

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

