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
    Convierte la expresión del usuario a simbólica:
    - sen -> sin, tg -> tan, j -> I, etc.
    - Sympy conoce todas las funciones necesarias
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

    # Definir todas las funciones que Sympy puede usar
    funciones = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "asin": sp.asin,
        "acos": sp.acos,
        "atan": sp.atan,
        "cot": sp.cot,
        "sec": sp.sec,
        "csc": sp.csc,
        "sinh": sp.sinh,
        "cosh": sp.cosh,
        "tanh": sp.tanh,
        "log": sp.log,
        "sqrt": sp.sqrt,
        "E": sp.E,
        "I": sp.I,
        "pi": sp.pi
    }

    try:
        expr = sp.sympify(expr_str, locals=funciones)
        return expr
    except Exception as e:
        st.error(f"Error simbólico al convertir '{expr_str}': {e}")
        return None

# ==== PARTE NUMÉRICA ====
def convertir_expresion_numerica(expr_str):
    """
    Convierte expresión de usuario a función numérica evaluable con numpy.
    """
    reemplazos = {
        "sen":"sin",
        "arcsen":"arcsin",
        "arctg":"arctan",
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
    
    for k,v in reemplazos.items():
        expr_str = expr_str.replace(k,v)
    
    x = sp.Symbol('x', real=True)
    n = sp.Symbol('n', integer=True)

    try:
        expr_sym = sp.sympify(expr_str, evaluate=False)
        modules_num = {
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "sinh": np.sinh,
            "cosh": np.cosh,
            "tanh": np.tanh,
            "log": np.log,
            "sqrt": np.sqrt,
            "pi": np.pi,
            "E": np.e,
            "I": 1j,
            "exp": np.exp,
            "Exp": np.exp,  # <--- Esto faltaba
            "sec": lambda x: 1/np.cos(x),
            "csc": lambda x: 1/np.sin(x),
            "cot": lambda x: 1/np.tan(x)
        }
        func_num = sp.lambdify((x,n), expr_sym, modules=[modules_num, "numpy"])
        
        # Wrapper que fuerza salida a np.ndarray de tipo complejo
        return lambda x_vals, n_val: np.array(func_num(x_vals,n_val), dtype=np.complex128)

    except Exception as e:
        import streamlit as st
        st.error(f"Error numérico al convertir '{expr_str}': {e}")
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

