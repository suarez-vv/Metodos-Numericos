import math
from sympy import symbols, diff, sympify, lambdify
import re

#Funciones de apoyo para manejar y evaluar las ecuaciones

def evaluar(ecuacion, x):
    try:
        super_a_normal = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻ˣ", "0123456789-x")
        ecuacion = ecuacion.translate(super_a_normal)
        
        ecuacion = re.sub(r'ln\(', 'math.log(', ecuacion)
        ecuacion = re.sub(r'log10\(', 'math.log10(', ecuacion)
        ecuacion = re.sub(r'e\^\(([^)]+)\)', r'math.e**(\1)', ecuacion)
        ecuacion = re.sub(r'e\^([^\s\+\-\*/\)]+)', r'math.e**(\1)', ecuacion)
        ecuacion = ecuacion.replace('^', '**')

        ecuacion = re.sub(r'(\d)(x)', r'\1*\2', ecuacion)
        ecuacion = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', ecuacion)

        contexto = {
            "x": x,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "sqrt": math.sqrt,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "math": math
        }
        return eval(ecuacion, {"__builtins__": None}, contexto)
    except Exception:
        return None
    
def derivar(ecuacion):
    x = symbols('x')
    super_a_normal = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻ˣ", "0123456789-x")
    ecuacion = ecuacion.translate(super_a_normal)

    ecuacion = re.sub(r'e\^\(([^)]+)\)', r'exp(\1)', ecuacion)
    #ecuacion = re.sub(r'e\^\(([^)]+)\)', r'math.e**(\1)', ecuacion)
    #ecuacion = re.sub(r'e\^([^\s\+\-\*/\)]+)', r'math.e**(\1)', ecuacion)
    ecuacion = re.sub(r'e\^([^\s\+\-\*/\)]+)', r'exp(\1)', ecuacion)

    ecuacion = ecuacion.replace('^', '**')

    ecuacion = re.sub(r'(\d)(x)', r'\1*\2', ecuacion)
    ecuacion = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', ecuacion)
    ecuacion = re.sub(r'ln\(', 'log(', ecuacion)
    ecuacion = re.sub(r'log10\(', 'log(,10*', ecuacion)
    ecuacion = re.sub(r'log\(\,10\*', 'log(', ecuacion)

    expr = sympify(ecuacion)
    derivada = diff(expr, x)
    return lambdify(x, derivada, 'math'), str(derivada)

#####INICIO DE METODOS ######

#BISECCION

def biseccion(ecuacion, Xi, Xs, Es, pEs, iter):
    resultados = []

    iteracion1 = True
    Ea=tI=fXr= None
    tI = 0

    if Es != None:
        Es = 0.5*10**(2-Es)

    fXi = evaluar(ecuacion, Xi) #Calcular valor de fXi
    fXs = evaluar(ecuacion, Xs) #Calcular valor de fXs

    if fXi is None or fXs is None:
        resultados.append({
            "tipo": "error",
            "mensaje": f"No se pudo evaluar la ecuación.<br>"
                       f"f({Xi}) = {round(fXi, 4)},    f({Xs}) = {round(fXs, 4)}<br>" 
                       f"Revisa la sintaxis (usa ^ para potencias, y 'x' en minúscula)."
        })
        return resultados

    criterios = []
    if pEs:
        criterios.append((f"|Ea| < {Es}%<br>").replace('<', '&lt;').replace('>', '&gt;'))
    if iter:
        criterios.append(f"Número máximo de iteraciones = {iter}<br>")
    criterios.append("Encontrar la raíz exacta es un criterio de paro por defecto.")
    criterios_html = "<br>".join(criterios)
    
    resultados.append({
        "tipo": "datos",
        "mensaje": (
            f"<b>BISECCIÓN</b><br>"
            f"<br><b>Datos iniciales:</b><br>"
            f"f(x) = {ecuacion}<br>"
            f"Xi = {round(Xi, 4)}<br>"
            f"Xs = {round(Xs, 4)}<br>"
            f"<br><b>Criterios de paro:</b><br>"
            f"{criterios_html if criterios else '-'}"
        )
    })
    
    resultados.append({
        "tipo": "info",
        "mensaje": f"<br><b>Evaluación inicial:</b>" f"<br>Xi -> &nbsp;&nbsp;f({Xi}) = {fXi} <br>Xs -> &nbsp;&nbsp;f({Xs}) = {fXs}"
    })

    if fXi * fXs > 0:
        resultados.append({
            "tipo": "error",
            "mensaje": "La raíz no se encuentra entre Xi y Xs, ya que f(Xi) y f(Xs) tienen el mismo signo.<br>"
        })
        return resultados

    return biseccionRecursivo(ecuacion, Xi, Xs, fXi, fXs, fXr, Es, Ea, tI, iter, iteracion1, None, pEs, resultados)


       

def biseccionRecursivo(ecuacion, Xi, Xs, fXi, fXs, fXr, Es, Ea, tI, iter, iteracion1, aXr, pEs, resultados):
            
    if tI == iter: 
        resultados.append({
            "tipo": "info",
            "mensaje": "<br><b>Criterio de paro encontrado: Número máximo de iteraciones.</b>"
        })
        return resultados
    
    if pEs is True and Ea is not None and abs(round(Ea, 4)) < Es:
        resultados.append({
            "tipo": "info",
            "mensaje": f"<br><b>Criterio de paro encontrado: |Ea| &lt; Es -> ({round(abs(Ea), 2)}% &lt; {Es}%)</b>"
        })
        return resultados
    if fXr == 0:
        resultados.append({
            "tipo": "info",
            "mensaje": f"<br><b>Criterio de paro encontrado: Raíz exacta encontrada.</b>"
        })
        return resultados
    
    tI += 1 #Aqui variable aumentar una iteracion

    #Obtencion de Xr
    Xr = (Xi+Xs)/2
    fXr = evaluar(ecuacion, Xr)    


    if fXr is None:
        resultados.append({
            "tipo": "error",
            "mensaje": f"No se pudo evaluar f(Xr) en la iteración {tI}"
        })
        return resultados

    if iteracion1 == True: 
        Ea = None
        iteracion1 = False
    else: Ea = ((Xr - aXr)/Xr)*100 


    resultados.append({
        "tipo": "iteracion",
        "mensaje": (
            f"<b>Iteración {tI}:</b><br>"
            f"Xi = {round(Xi, 4)}     &nbsp;&nbsp;&nbsp;&nbsp;f(Xi) = {round(fXi, 4)}<br>"
            f"<br>Xs = {round(Xs, 4)}       &nbsp;&nbsp;&nbsp;&nbsp;f(Xs) = {round(fXs, 4)}<br><br>"
            f"Xr = {round(Xr, 4)}     &nbsp;&nbsp;&nbsp;&nbsp;f(Xr) = {round(fXr, 4)}<br>"
            f"<br>Ea = {'N/A' if Ea is None else str(round(Ea, 2)) + '%'}<br>"
        )
    })


    if (fXs < 0 and fXr < 0) or (fXs > 0 and fXr > 0):
        Xs = Xr
        resultados.append({
            "tipo": "info",
            "mensaje": (f"Como: f(Xi)f(Xr) < 0 &nbsp;&nbsp;-> &nbsp;&nbsp;Xs = Xr").replace('<', '&lt;').replace('>', '&gt;')
        })
    elif (fXi < 0 and fXr < 0) or (fXi > 0 and fXr > 0):
        Xi = Xr
        resultados.append({
            "tipo": "info",
            "mensaje": "Como: f(Xi)f(Xr) > 0  &nbsp;&nbsp;-> &nbsp;&nbsp;Xi = Xr"
        })
    else:
        resultados.append({
            "tipo": "info",
            "mensaje": f"Como: f(Xi)f(Xr) = 0  &nbsp;&nbsp;-> &nbsp;&nbsp;Xr({Xr}) = Raíz."
        })

    aXr = Xr
    fXi = evaluar(ecuacion, Xi)
    fXs = evaluar(ecuacion, Xs)

    return biseccionRecursivo(ecuacion, Xi, Xs, fXi, fXs, fXr, Es, Ea, tI, iter, iteracion1, aXr, pEs, resultados)


#REGLA FALSA

def regla_falsa(ecuacion, Xi, Xs, Es, pEs, iter):
    resultados = []

    iteracion1 = True
    Ea=tI=fXr= None
    tI = 0

    if Es != None:
        Es = 0.5*10**(2-Es)

    fXi = evaluar(ecuacion, Xi) #Calcular valor de fXi
    fXs = evaluar(ecuacion, Xs) #Calcular valor de fXs

    if fXi is None or fXs is None:
        resultados.append({
            "tipo":"error",
            "mensaje": f"No se pudo evaluar la ecuación.<br>"
                       f"f({Xi}) = {round(fXi, 4)},   f({Xs}) = {round(fXs, 4)}<br>"
                       f"Revisa la sintaxis (usa ^ para potencias, y 'x' en minúscula)."
        })
        return resultados
    
    criterios = []
    if pEs:
        criterios.append((f"|Ea| < {Es}%").replace('<', '&lt;').replace('>', '&gt;'))
    if iter:
        criterios.append(f"Número máximo de iteraciones = {iter}")
    criterios.append("Encontrar la raíz exacta es un criterio de paro por defecto.")
    criterios_html = "<br>".join(criterios)
    
    resultados.append({
        "tipo": "datos",
        "mensaje": (
            f"<b>REGLA FALSA</b><br>"
            f"<br><b>Datos iniciales:</b><br>"
            f"f(x) = {ecuacion}<br>"
            f"Xi = {round(Xi, 4)}<br>"
            f"Xs = {round(Xs, 4)}<br>"
            f"<br><b>Criterios de paro:</b><br>"
            f"{criterios_html if criterios else '-'}"
        )
    })

    resultados.append({
        "tipo": "info",
        "mensaje": f"<b>Evaluación inicial:</b>" f"<br>Xi -> &nbsp;&nbsp;f({Xi}) = {round(fXi, 4)} <br>Xs -> &nbsp;&nbsp;f({Xs}) = {round(fXs, 4)}"
    })

    if fXi * fXs > 0:
        resultados.append({
            "tipo": "error",
            "mensaje": "La raíz no se encuentra entre Xi y Xs, ya que f(Xi) y  f(Xs) tienen el mismo signo.<br>"
        })
        return resultados

    return reglaFalsa_Recursivo(ecuacion, Xi, Xs, fXi, fXs, fXr, Es, Ea, tI, iter, iteracion1, None, pEs, resultados)

def reglaFalsa_Recursivo(ecuacion, Xi, Xs, fXi, fXs, fXr, Es, Ea, tI, iter, iteracion1, aXr, pEs, resultados):

    if tI == iter:
        resultados.append({
            "tipo": "info",
            "mensaje": "<br><b>Criterio de paro encontrado: Número máximo de iteraciones.</b>"
        })
        return resultados
    
    if pEs is True and Ea is not None and abs(round(Ea, 4)) < Es: 
        resultados.append({
            "tipo": "info",
            "mensaje": f"<br><b>Criterio de paro encontrado: |Ea| &lt; Es -> ({round(abs(Ea), 2)}% &lt; {Es}%)</b>"
        })
        return resultados
    
    if fXr == 0:
        resultados.append({
            "tipo": "info",
            "mensaje": f"<br><b>Criterio de paro encontrado: Raíz exacta encontrada.</b>"
        })
        return resultados

    tI += 1 #Aqui variable aumentar una iteracion

    #Obtencion de Xr
    Xr = Xs - ((fXs*(Xi-Xs))/(fXi-fXs))
    fXr = evaluar(ecuacion, Xr)    #Calcular fXr

    #Seleccionar intervalos
    if fXr is None:
        resultados.append({
            "tipo": "error",
            "mensaje": f"No se pudo evaluar f(Xr) en la iteración {tI}"
        })
        return resultados
        
    if iteracion1 == True:
        Ea =  None
        iteracion1 =  False
    else: Ea = ((Xr - aXr)/Xr)*100

    resultados.append({
        "tipo": "iteracion",
        "mensaje": (
            f"<b>Iteración {tI}:</b><br>"
            f"Xi = {round(Xi, 4)}     &nbsp;&nbsp;&nbsp;&nbsp;f(Xi) = {round(fXi, 4)}<br>"
            f"<br>Xs = {round(Xs, 4)}     &nbsp;&nbsp;&nbsp;&nbsp;f(Xs) = {round(fXs, 4)}<br><br>"
            f"Xr = {round(Xr, 4)}     &nbsp;&nbsp;&nbsp;&nbsp;f(Xr) = {round(fXr, 4)}<br>"
            f"<br>Ea = {'N/A' if Ea is None else str(round(Ea, 2)) + '%'}<br>"
        )
    })

    if (fXs < 0 and fXr < 0) or (fXs > 0 and fXr > 0):
        Xs = Xr
        resultados.append({
            "tipo": "info",
            "mensaje": (f"Como: f(Xi)f(Xr) < 0 &nbsp;&nbsp;-> &nbsp;&nbsp;Xs = Xr").replace('<', '&lt;').replace('>', '&gt;')
        })
    elif (fXi < 0 and fXr < 0) or (fXi > 0 and fXr > 0):
        Xi =  Xr
        resultados.append({
            "tipo": "info",
            "mensaje": "Como: f(Xi)f(Xr) > 0  &nbsp;&nbsp;-> &nbsp;&nbsp;Xi = Xr"
        })
    else:
        resultados.append({
            "tipo": "info",
            "mensaje": f"Como: f(Xi)f(Xr) = 0  &nbsp;&nbsp;->&nbsp;&nbsp; Xr({Xr}) = Raíz."
        })

    aXr = Xr  #Definir el Xr anterior para el Ea

    fXi = evaluar(ecuacion, Xi)  #Calcular fxi con la ecuacion y los valores
    fXs = evaluar(ecuacion, Xs)  #Calcular fxs con la ecuacion y los valores

    return reglaFalsa_Recursivo(ecuacion, Xi, Xs, fXi, fXs, fXr, Es, Ea, tI, iter, iteracion1, aXr, pEs, resultados)


#NEWTON-RAPHSON
def newtonRaphson(ecuacion, Xa, Es, pEs, iter):
    resultados = []
    x = symbols('x')

    iteracion1 = True
    Ea=tI= None
    tI = 0

    if Es != None:
        Es = 0.5*10**(2-Es)
    
    derivada_func, derivadaString  = derivar(ecuacion)

    fXa = evaluar(ecuacion, Xa) #Calcular valor de fXa
    fpXa = derivada_func(Xa) #Derivar #Calcular la derivada de f'Xa

    if fXa is None or fpXa is None:
        resultados.append({
            "tipo": "error",
            "mensaje": (
                f"No se pudo evaluar la ecuación o su derivada.<br>"
                f"f({Xa}) = {fXa} <br>f'({Xa}) = {fpXa}<br>"
            )
        })
        return resultados
    
    criterios = []
    if pEs:
        criterios.append((f"|Ea| < {Es}%").replace('<', '&lt;').replace('>', '&gt;'))
    if iter:
        criterios.append(f"Número máximo de iteraciones = {iter}")
    criterios.append("Encontrar la raíz exacta es un criterio de paro por defecto.")
    criterios_html = "<br>".join(criterios)

    resultados.append({
        "tipo": "datos",
        "mensaje": (
            f"<b>NEWTON-RAPHSON</b><br>"
            f"<br><b>Datos iniciales:</b><br>"
            f"f(x) = {ecuacion}<br>"
            f"f'(x) = {derivadaString}<br>"
            f"X0 = {Xa}<br>"
            f"{criterios_html if criterios else '-'}"
        )
    })

    resultados.append({
        "tipo": "info",
        "mensaje": f"<br><b>Evaluación inicial:</b>" f"<br>X0 -> &nbsp;&nbsp;f({Xa}) = {fXa} <br>X0 -> &nbsp;&nbsp;f'({Xa}) = {fpXa}"
    })

    return newtonRaphson_Recursivo(ecuacion, derivada_func, Xa, fXa, fpXa, Es, Ea, tI, iter, iteracion1, pEs, resultados, x)

def newtonRaphson_Recursivo(ecuacion, derivada_func, Xa, fXa, fpXa, Es, Ea, tI, iter, iteracion1, pEs, resultados, x):
    Xn = None
    #Casos base
    if tI == iter: 
        resultados.append({
            "tipo": "info",
            "mensaje": "<br><b>Criterio de paro encontrado: Número máximo de iteraciones.</b>"
        })
        return resultados

    if pEs is True and Ea is not None and abs(Ea) < Es:
        resultados.append({
            "tipo": "info",
            "mensaje": f"<br><b>Criterio de paro encontrado: |Ea| &lt; Es -> ({round(abs(Ea), 2)}% &lt; {Es}%)</b>"
        })
        return resultados


    if fXa == 0:
        resultados.append({
            "tipo": "info",
            "mensaje": f"<br><b>Criterio de paro encontrado: Raíz exacta encontrada.</b>"
        })
        return resultados
    
    if fpXa == 0:
        resultados.append({
            "tipo": "error",
            "mensaje": "<br><b>Error: Derivada nula, no se puede continuar (divisón entre 0).</b>"
        })
        return resultados

    tI += 1 #Aumentar una iteracion

    #Obtencion de la X siguiente
    Xn = Xa - (fXa/fpXa)


    if iteracion1 == True: 
        Ea = None
        iteracion1 = False
    else: Ea = ((Xn - Xa)/Xn)*100  #Obtener Error relativo aproximado

    resultados.append({
        "tipo": "iteracion",
        "mensaje": (
            f"<b>Iteración {tI}:</b><br>"
            f"X{tI-1} = {round(Xa, 4)}    f(X{tI-1}) = {round(fXa, 4)}<br>" 
            f"X{tI-1} = {round(Xa, 4)}    f'(X{tI-1}) = {round(fpXa, 4)}<br>"
            f"<br>X{tI} = {round(Xn, 4)}"
            f"<br>Ea = {'N/A' if Ea is None else str(round(Ea, 2)) + '%'}<br>"   
        )
    })


    Xa = Xn  #Xn pasa a ser Xa para sigueinte iteracion

    fXa = evaluar(ecuacion, Xa)  #Calcular fxa con la ecuacion y los valores
    fpXa = derivada_func(Xa) #Derivar fXa con la ecuacion y los valores

    return newtonRaphson_Recursivo(ecuacion, derivada_func, Xa, fXa, fpXa, Es, Ea, tI, iter, iteracion1, pEs, resultados, x)

#SECANTE
def secante(ecuacion, Xp, Xa, Es, pEs, iter):
    resultados = []

    iteracion1 = True
    Ea=tI= None
    tI = 0

    if Es is not None:
        Es = 0.5*10**(2-Es)

    fXp = evaluar(ecuacion, Xp) #Calcular valor de fX-1
    fXa = evaluar(ecuacion, Xa) #Calcular valor de fX0

    if fXp is None or fXa is None:
        resultados.append({
            "tipo": "error",
            "mensaje": (
                f"No se pudo evaluar la ecuación con X-1 o X0.<br>"
                f"f({Xp}) = {round(fXp)} <br>f'({Xa}) = {round(fXa)}<br>"
            )
        })
        return resultados
    
    criterios = []
    if pEs:
        criterios.append((f"|Ea| < {Es}%").replace('<', '&lt;').replace('>', '&gt;'))
    if iter:
        criterios.append(f"Número máximo de iteraciones = {iter}")
    criterios.append("<br>Encontrar la raíz exacta es un criterio de paro por defecto.")
    criterios_html = "<br>".join(criterios)

    resultados.append({
        "tipo": "datos",
        "mensaje": (
            f"<b>SECANTE</b><br>"
            f"<br><b>Datos iniciales:</b><br>"
            f"f(x) = {ecuacion}<br>"
            f"X-1 = {Xp}<br>"
            f"X0 = {Xa}<br>"
            f"{criterios_html if criterios else '-'}"
        )
    })

    resultados.append({
        "tipo": "info",
        "mensaje": f"<br><b>Evaluación inicial:</b>" f"<br>X-1 -> &nbsp;&nbsp;f({Xp}) = {round(fXp, 4)} <br>X0 -> &nbsp;&nbsp;f({Xa}) = {round(fXa, 4)}"
    })

    return secanteRecursivo(ecuacion, Xp, Xa, fXp, fXa, Es, Ea, tI, iter, iteracion1, pEs, resultados)

def secanteRecursivo(ecuacion, Xp, Xa, fXp, fXa, Es, Ea, tI, iter, iteracion1, pEs, resultados):
    denominador = fXp - fXa
    epsilon = 1e-12
    if abs(denominador) < epsilon:
        resultados.append({
            "tipo": "info",
            "mensaje": f"<br><b>Denominador demasiado pequeño, aproximación final:</b> &nbsp;&nbsp;&nbsp;Xn = {round(Xa, 4)}"
        })
        return resultados
    
    if tI == iter: 
        resultados.append({
            "tipo": "info",
            "mensaje": "<br><b>Criterio de paro encontrado: Número máximo de iteraciones.</b>"
        })
        return resultados
    
    if pEs is True and Ea is not None and abs(Ea) < Es:
        resultados.append({
            "tipo": "info",
            "mensaje": f"<br><b>Criterio de paro encontrado: |Ea| &lt; Es -> ({round(abs(Ea), 2)}% &lt; {Es}%)</b>"
        })
        return resultados
        
    if fXa == 0:
        resultados.append({
            "tipo": "info", 
            "mensaje": (
                f"<br><b>Criterio de paro encontrado: Raíz exacta encontrada.</b>"
                f"<br>X{tI} = {Xa}    &nbsp;&nbsp;f(X{tI}) = {fXa}"
                )
        })
        return resultados

    tI += 1 #Aqui variable aumentar una iteracion

    #Obtencion de X siguiente
    Xn = Xa - (fXa*(Xp-Xa))/(fXp-fXa)

    if iteracion1 == True: 
        Ea = None
        iteracion1 = False
    else: Ea = ((Xn - Xa)/Xn)*100  #Obtener Error relativo aproximado

    resultados.append({
        "tipo": "iteracion",
        "mensaje": (
            f"<b>Iteración {tI}:</b><br>"
            f"X{tI-2} = {round(Xp, 4)}   f(X{tI-2}) = {round(fXp, 4)}<br>" #x-1
            f"<br>X{tI-1} = {round(Xa, 4)}  f(X{tI-1}) = {round(fXa, 4)}<br><br>"
            f"<br>X{tI} = {round(Xn, 4)}"
            f"<br>Ea = {'N/A' if Ea is None else str(round(Ea, 2)) + '%'}<br>"
        )
    })

    Xp = Xa
    Xa = Xn 

    fXp = evaluar(ecuacion, Xp)
    fXa = evaluar(ecuacion, Xa)  

    return secanteRecursivo(ecuacion, Xp, Xa, fXp, fXa, Es, Ea, tI, iter, iteracion1, pEs, resultados)