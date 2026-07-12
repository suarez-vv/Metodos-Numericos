import re
import sympy as sp

#Funciones de apoyo para manejar ecuaciones y matrices
def procesarEcuaciones(texto):
    texto = re.sub(r'(\d)(X\d)', r'\1*\2', texto)
    texto = texto.replace("^", "**")
    return texto

def obtenerFormulas(ecuaciones):
    variables = sp.symbols('X1 X2 X3')
    formulas = []

    for i, texto in enumerate(ecuaciones):
        texto = procesarEcuaciones(texto).strip()
        if "=" not in texto:
            raise ValueError(f"La ecuacion {i+1} no contiene '='")

        izq, der = texto.split("=")
        izq = sp.sympify(izq)
        der = sp.sympify(der)

        var = variables[i] if i < len(variables) else None
        if var is None:
            continue

        coeficienteVar = izq.coeff(var)

        if coeficienteVar == 0:
            continue

        resto = izq - coeficienteVar * var

        exprDerecha = (der - resto)/coeficienteVar
        
        formulas.append(exprDerecha)
    
    return formulas

def formulaUsuario(var, expr):
    expr = sp.together(expr)
    frac = sp.fraction(sp.simplify(expr))
    numerador, denominador = frac

    numeradorString = str(numerador)
    denominadorString = str(denominador)

    if '+' in numeradorString or '-' in numeradorString:
        numeradorString = f"({numeradorString})"
    
    numeradorString = re.sub(r'(\d+)\*X', r'\1X', numeradorString)
    numeradorString = numeradorString.replace('*', '')
    denominadorString = denominadorString.replace('*', '')

    if denominador != 1:
        return f"{var} = {numeradorString}/{denominadorString}"
    else:
        return f"{var} = {numeradorString}"

def formato_datosIniciales(ecuaciones, formulas):

    frm_html = "<b>Ecuaciones:</b><br>"
    for eq in ecuaciones:
        frm_html += f"{eq}<br>"
    
    frm_html += "<br><b>Fórmulas:</b><br>"
    for i, eq in enumerate(formulas, start = 1):
        var = f"<b>X{i}</b>"
        frm_html += formulaUsuario(var, eq) + "<br>"
    
    return frm_html

def formatearMatriz(M):
    maxLen = max(len(str(sp.nsimplify(M[i,j]))) for i in range(3) for j in range(3))
    filas = []
    for i in range(3):
        fila = []
        for j in range(3):
            val = str(sp.nsimplify(M[i,j]))
            fila.append(f"{val:>{maxLen}}")
        filas.append(f"[{' '.join(fila)}]")
    
    return filas

####INiCIO DE METODOS#####

#Gauss-Seidel
def gauss_Seidel(ecuaciones, pEas, Es, iter, x2, x3):
    resultados = []
    tI = 0
    if Es is not None:
        Es = 0.5*10**(2-Es)

    try:
        formulas = obtenerFormulas(ecuaciones)
    except Exception as e:
        resultados.append({
            "tipo": "error",
            "mensaje": f"Error, ecuaciones escritas de forma incorrecta: {str(e)}"
        })
        return resultados

    criterios = []

    if iter:
        criterios.append(f"Número máximo de iteraciones = {iter}")
    if Es is not None:
        criterios.append(f"Error tolerado Es = {Es}%")
    if pEas:
        criterios.append(f"Error (Ea), a calcular para: {', '.join(pEas)}")
    criterios_html = "<br>".join(criterios)

    datosIniciales = formato_datosIniciales(ecuaciones, formulas)

    resultados.append({
        "tipo": "datos",
        "mensaje": (
            f"<b>GAUSS-SEIDEL</b><br>"
            f"<br><b>Datos iniciales:</b><br><br>"
            f"{datosIniciales}"
            f"<br><b>{criterios_html if criterios else '-'}</b>"
        )
    })

    x1 = 0

    return recursivoGauss_Seidel(formulas, pEas, x1, x2, x3, tI, Es, iter, resultados)

def recursivoGauss_Seidel(formulas, pEas, x1, x2, x3, tI, Es, iter, resultados):

    if tI == iter:
        resultados.append({
            "tipo": "info",
            "mensaje": "<br><b>Criterio de paro encontrado: Número máximo de iteraciones.<b/>"
        })
        return resultados

    tI += 1

    x1N = float(formulas[0].evalf(subs={'X1': x1, 'X2': x2, 'X3': x3}))
    x2N = float(formulas[1].evalf(subs={'X1': x1N, 'X2': x2, 'X3': x3}))
    x3N = float(formulas[2].evalf(subs={'X1': x1N, 'X2': x2N, 'X3': x3}))

    Ea_X1 = Ea_X2 = Ea_X3 = None
    if tI > 1:
        if 'X1' in pEas and x1N != 0:
            Ea_X1 = ((x1N-x1)/x1N)*100
        if 'X2' in pEas and x2N != 0:
            Ea_X2 = ((x2N-x2)/x2N)*100
        if 'X3' in pEas and x3N != 0:
            Ea_X3 = ((x3N-x3)/x3N)*100
    

    #Mensaje de iteracion
    mensaje = (
        f"<br><b>Iteración {tI}:</b><br>"
        f"X1 = {round(x1N, 4)} <br>X2 = {round(x2N, 4)} <br>X3 = {round(x3N, 4)}"
    )

    if Ea_X1 is not None or Ea_X2 is not None or Ea_X3 is not None:
        mensaje += "<br><br><b>Errores aproximados:</b><br>"
        if Ea_X1 is not None:
            mensaje += f"Ea(X1) = {round(Ea_X1, 2)}%<br>"
        if Ea_X2 is not None:
            mensaje += f"Ea(X2) = {round(Ea_X2, 2)}%<br>"
        if Ea_X3 is not None:
            mensaje += f"Ea(X3) = {round(Ea_X3, 2)}%<br>"
        if tI == 1:
            mensaje += f"<br>Ea = N/A"
    
    resultados.append({
        "tipo": "iteracion",
        "mensaje": mensaje
    })

    #Comprobar Ea
    if Es is not None:
        cumplidas = [] 
        for var, ea in zip(['X1', 'X2', 'X3'], [Ea_X1, Ea_X2, Ea_X3]):
            if var in pEas and ea is not None:
                if abs(ea) < Es:
                    cumplidas.append(f"{var} (Ea={round(ea, 2)}% < {Es}%)")
        
        if cumplidas:
            resultados.append({
                "tipo": "info",
                "mensaje": (
                    f"<br><b>Criterio de paro encontrado:</b><br>"
                    f"Error aproximado: {', '.join(cumplidas).replace('<', '&lt;').replace('>', '&gt;')}<br>"
                )
            })

            return resultados


    return recursivoGauss_Seidel(formulas, pEas, x1N, x2N, x3N, tI, Es, iter, resultados)

#JACOBI
def jacobi(ecuaciones, pEas, Es, iter, x1, x2, x3):
    resultados = []
    tI = 0

    if Es is not None:
        Es = 0.5*10**(2-Es)

    try:
        formulas = obtenerFormulas(ecuaciones)
    except Exception as e:
        resultados.append({
            "tipo": "error",
            "mensaje": f"Error, ecuaciones escritas de forma incorrecta: {str(e)}"
        })
        return resultados

    criterios = []

    if iter:
        criterios.append(f"Número máximo de iteraciones = {iter}")
    if pEas:
        criterios.append(f"Error (Ea), a calcular para: {', '.join(pEas)}")
    criterios_html = "<br>".join(criterios)

    datosIniciales = formato_datosIniciales(ecuaciones, formulas)

    resultados.append({
        "tipo": "datos",
        "mensaje": (
            f"<b>JACOBI</b><br>"
            f"<br><b>Datos iniciales:</b><br><br>"
            f"{datosIniciales}"
            f"<br><b>{criterios_html if criterios else '-'}</b>"
        )
    })

    return recursivoJacobi(formulas, pEas, x1, x2, x3, tI, Es, iter, resultados)

def recursivoJacobi(formulas, pEas, x1, x2, x3, tI, Es, iter, resultados):

    if tI == iter:
        resultados.append({
            "tipo": "info",
            "mensaje": "<br><b>Criterio de paro encontrado: Número máximo de iteraciones.<b/>"
        })
        return resultados

    tI += 1

    x1N = float(formulas[0].evalf(subs={'X1': x1, 'X2': x2, 'X3': x3}))
    x2N = float(formulas[1].evalf(subs={'X1': x1, 'X2': x2, 'X3': x3}))
    x3N = float(formulas[2].evalf(subs={'X1': x1, 'X2': x2, 'X3': x3}))

    Ea_X1 = Ea_X2 = Ea_X3 = None
    if tI > 1:
        if 'X1' in pEas and x1N != 0:
            Ea_X1 = ((x1N-x1)/x1N)*100
        if 'X2' in pEas and x2N != 0:
            Ea_X2 = ((x2N-x2)/x2N)*100
        if 'X3' in pEas and x3N != 0:
            Ea_X3 = ((x3N-x3)/x3N)*100

    #Mensaje de iteracion
    mensaje = (
        f"<br><b>Iteración {tI}:</b><br>"
        f"X1 = {round(x1N, 4)} <br>X2 = {round(x2N, 4)} <br>X3 = {round(x3N, 4)}"
    )

    if Ea_X1 is not None or Ea_X2 is not None or Ea_X3 is not None:
        mensaje += "<br><br><b>Errores aproximados:</b><br>"
        if Ea_X1 is not None:
            mensaje += f"Ea(X1) = {round(Ea_X1, 2)}%<br>"
        if Ea_X2 is not None:
            mensaje += f"Ea(X2) = {round(Ea_X2, 2)}%<br>"
        if Ea_X3 is not None:
            mensaje += f"Ea(X3) = {round(Ea_X3, 2)}%<br>"
        if tI == 1:
            mensaje += f"<br>Ea = N/A"
    
    resultados.append({
        "tipo": "iteracion",
        "mensaje": mensaje
    })

    #Comprobar Ea
    if Es is not None:
        cumplidas = [] 
        for var, ea in zip(['X1', 'X2', 'X3'], [Ea_X1, Ea_X2, Ea_X3]):
            if var in pEas and ea is not None:
                if abs(ea) < Es:
                    cumplidas.append(f"{var} (Ea={round(ea, 2)}% < {Es}%)")
        if cumplidas:
            resultados.append({
                "tipo": "info",
                "mensaje": (
                    f"<br><b>Criterio de paro encontrado:</b>"
                    f"Error aproximado: {', '.join(cumplidas).replace('<', '&lt;').replace('>', '&gt;')}<br>"
                )
            })

            return resultados


    return recursivoJacobi(formulas, pEas, x1N, x2N, x3N, tI, Es, iter, resultados)

#Doolittle
def doolittle(ecuaciones):
    resultados = []

    x1, x2, x3 =sp.symbols('X1 X2 X3')
    variables = [x1, x2, x3]

    try:
        ecuacionSymp = []
        for i, texto in enumerate(ecuaciones):
            texto = procesarEcuaciones(texto)
            if "=" not in texto:
                raise ValueError(f"La ecuación {i} no contiene '='")
            izq, der = texto.split("=", 1)
            ecuacionSymp.append(sp.Eq(sp.simplify(izq), sp.simplify(der)))
        
        A, B = sp.linear_eq_to_matrix(ecuacionSymp, variables)

        A = sp.Matrix(A)
        B = sp.Matrix(B)

        detA = A.det()

        frm_html = "<b>Matriz A de coeficientes:</b><br>"
        for fila in A.tolist():
            frm_html += str(fila) + "<br>"
        
        frm_html += "<br><b>Vector B de constantes:</b><br>"
        for val in B.tolist():
            frm_html += f"[{float(val[0]):g}]<br>"

        frm_html += f"{'-'*85}"
        frm_html += f"<br><b>|A|</b> = {detA}<br>"

        if detA != 0:
            frm_html += f"<br>Como |A| != 0, por lo tanto A = LU."

            a11, a12, a13 = A[0, 0], A[0, 1], A[0, 2]
            a21, a22, a23 = A[1, 0], A[1, 1], A[1, 2]
            a31, a32, a33 = A[2, 0], A[2, 1], A[2, 2]

            frm_html += "<pre>"
            frm_html += f"    [{a11}  {a12}  {a13}]      [1 0 0] [  {a11}     {a12}     {a13}  ]\n"
            frm_html += f"A = [{a21}  {a22}  {a23}]  =  [a 1 0] [  0     x     y  ]\n"
            frm_html += f"    [{a31}  {a32}  {a33}]     [b c 0] [  0     0     z  ]\n\n"
            frm_html += f"                   [ {a11}     {a12}      {a13}  ]\n"
            frm_html += f"                =  [{'-' if a11 == -1 else ('' if a11 == 1 else a11)}a   {'-' if a12 == -1 else ('' if a12 == 1 else a12)}a+x    {'-' if a13 == -1 else ('' if a13 == 1 else a13)}a+y ]\n"
            frm_html += f"                   [{'-' if a11 == -1 else ('' if a11 == 1 else a11)}b  {'-' if a12 == -1 else ('' if a12 == 1 else a12)}b+cx  {'-' if a13 == -1 else ('' if a13 == 1 else a13)}b+cy+z]\n\n"
            frm_html += "</pre>"

            l21, l31, l32 = sp.symbols('l21 l31 l32')
            u22, u23, u33 = sp.symbols('u22 u23 u33')
            L = sp.Matrix([
                [1, 0, 0],
                [l21, 1, 0],
                [l31, l32, 1]
            ])

            U = sp.Matrix([
                [A[0,0], A[0, 1], A[0,2]],
                [0, u22, u23],
                [0, 0, u33]
            ])

            LU = L*U
            ecuacionesLU = []
            for i in range(3):
                for j in range(3): 
                    if not sp.simplify(LU[i,j] - A[i,j]) == 0: #Solo las ecuaciones que tengan las variables
                        ecuacionesLU.append(sp.Eq(LU[i,j], A[i,j]))

            mapa_var = {
                l21: "a", l31: "b", l32: "c",
                u22: "x", u23: "y", u33: "z"
            }
            for ecu_val in ecuacionesLU:
                ecu_pos = ecu_val
                for var, nombre in mapa_var.items():
                    ecu_pos = ecu_pos.subs(var, sp.symbols(nombre))

            valoresCalc = {}

            frm_html += "<br>Por lo tanto:<br><pre>"

            for ecu_val in ecuacionesLU:
                ecu_sust = ecu_val
                for var, nombre in mapa_var.items():
                    ecu_sust = ecu_sust.subs(var, sp.symbols(nombre))
                
                lhs = sp.simplify(ecu_sust.lhs)
                rhs = sp.simplify(ecu_sust.rhs)
                lhs_str = str(lhs).replace("*", "")
                rhs_str = str(rhs)
                
                for var_sym, val in valoresCalc.items():
                    lhs = lhs.subs(var_sym, val)
                    rhs = rhs.subs(var_sym, val)
                
                variable_sym = list(lhs.free_symbols)[0] if lhs.free_symbols else None
                if variable_sym is not None:
                    valor = sp.solve(lhs - rhs, variable_sym)[0]
                    valor_frac = sp.nsimplify(valor)
                    valoresCalc[variable_sym] = valor_frac
                    variable = mapa_var.get(variable_sym, variable_sym)
                else:
                    variable = "?"
                    valor_frac = "?"
                
                #Ecuacion y resultado despejado
                frm_html += f"{lhs_str:>10} = {rhs_str:<4}<b> ->  </b>{str(variable):<2} = {str(valor_frac):<6}\n"

            frm_html += "</pre>"

            #Matrices L y U con valores finales
            L_var = L.subs(mapa_var)
            U_var = U.subs(mapa_var)

            L_valor = L_var.subs(valoresCalc)
            U_valor = U_var.subs(valoresCalc)

            L_impresion = formatearMatriz(L_valor)
            U_impresion = formatearMatriz(U_valor)

            frm_html += "<br>Por lo tanto:<br><pre>"
            frm_html += f"    {L_impresion[0]}          {U_impresion[0]}\n"
            frm_html += f"L = {L_impresion[1]}      U = {U_impresion[1]}\n"
            frm_html += f"    {L_impresion[2]}          {U_impresion[2]}\n"
            frm_html += "</pre>"

            frm_html += f"<br>{'-'*85}"
            frm_html += f"<br>Entonces:<br>"
            frm_html += f"<pre>  <b>Ux=D</b>     y     <b>LD = B</b><br>"

            D = sp.Matrix(['d1', 'd2', 'd3'])
            D_impresion = [f"[{str(D[i,0]):>3}]" for i in range(3)]
            B_impresion = [f"[{str(float(B[i,0])):>3}]" for i in range(3)]
            

            frm_html += "<pre>"
            frm_html += f"    {L_impresion[0]} {D_impresion[0]}   {B_impresion[0]}\n"
            frm_html += f"L = {L_impresion[1]} {D_impresion[1]} = {B_impresion[1]}\n"
            frm_html += f"    {L_impresion[2]} {D_impresion[2]}   {B_impresion[2]}\n"
            frm_html += "</pre>"

            #LD = B
            frm_html += "<br><b>Por lo tanto:</b><br><pre>"
            d1, d2, d3 = sp.symbols('d1 d2 d3')
            D_vars = [d1, d2, d3]

            ecuacionesD = []
            valoresD = {}

            #Hacer la multiplicacion LD
            for i in range(3):
                eq = sum(L_valor[i,j]*D_vars[j] for j in range(3))
                #rhs_valB = sp.N(B[i,0], 5)
                ecuacionesD.append(sp.Eq(eq, B[i,0]))
            
            for ecu in ecuacionesD:
                lhs = ecu.lhs
                rhs = ecu.rhs

                lhs_parts = []
                for v in D_vars:
                    coef = lhs.coeff(v)
                    if coef != 0:
                        if coef == 1:
                            lhs_parts.append(f"{v}")
                        elif coef == -1:
                            lhs_parts.append(f"-{v}")
                        else:
                            lhs_parts.append(f"{sp.nsimplify(coef)}{v}")
                lhs_str = " + ".join(lhs_parts)
                lhs_str = lhs_str.replace("+ -", "- ")

                for var_d, val_d in valoresD.items():
                    lhs = lhs.subs(var_d, val_d)
                    rhs = rhs.subs(var_d, val_d)
                
                varSymbol = list(lhs.free_symbols)[0] if lhs.free_symbols else None
                if varSymbol is not None:
                    val = sp.solve(lhs-rhs, varSymbol)[0]
                    val_frac = sp.nsimplify(val, rational=True, tolerance=1e-6)
                    val_frac = sp.Rational(val_frac).limit_denominator()
                    valoresD[varSymbol] = val_frac
                else:
                    val_frac = "?"

                rhs_str = str(rhs)
                frm_html += f"{lhs_str:<10} = {rhs_str:<6}  ->  {str(varSymbol)} = {val_frac}\n"
            
            frm_html += "</pre>"

            #Ux=D
            frm_html += "<br><b>Y:</b><br><pre>"
            x_vec = sp.Matrix(['x1', 'x2', 'x3'])
            x_impresion = [f"[{str(x_vec[i,0]):>3}]" for i in range(3)]
            frm_html += f"    {U_impresion[0]} {x_impresion[0]}   {valoresD[d1]}\n"
            frm_html += f"U = {U_impresion[1]} {x_impresion[1]} = {valoresD[d2]}\n"
            frm_html += f"    {U_impresion[2]} {x_impresion[2]}   {valoresD[d3]}\n"
            frm_html += "</pre>"

            frm_html += "<br><b>Por lo tanto:</b><br><pre>"
            x1, x2, x3 = sp.symbols('x1 x2 x3')
            x_vars = [x1, x2, x3]

            ecuacionesX = []
            for i, var_d in enumerate(D_vars):
                eq = sum(U_valor[i,j]*x_vars[j] for j in range(3))
                ecuacionesX.append(sp.Eq(eq, valoresD[var_d]))

            valoresX = {}

            #Hacer el ciclo al reves
            for ecu in reversed(ecuacionesX):
                lhs = sp.expand(ecu.lhs)
                rhs = ecu.rhs

                lhs_parts = []
                for v in x_vars:
                    coef = lhs.coeff(v)
                    if coef != 0:
                        coef_frac = sp.nsimplify(coef, rational=True)  # fuerza fracción
                        if coef_frac == 1:
                            lhs_parts.append(f"{v}")
                        elif coef_frac == -1:
                            lhs_parts.append(f"-{v}")
                        else:
                            lhs_parts.append(f"{coef_frac}{v}")

                constante = lhs - sum(lhs.coeff(v)*v for v in x_vars)
                if constante != 0:
                    constante_frac = sp.nsimplify(constante, rational=True)
                    lhs_parts.append(str(constante_frac))

                lhs_str = " + ".join(lhs_parts)
                lhs_str = lhs_str.replace("+ -", "- ")

                #Sustituir valores
                for var_x, val_x in valoresX.items():
                    lhs = lhs.subs(var_x, val_x)
                    rhs = rhs.subs(var_x, val_x)

                varSymbol = list(lhs.free_symbols)[0] if lhs.free_symbols else None
                if varSymbol:
                    val = sp.solve(lhs - rhs, varSymbol)[0]
                    val_frac = sp.nsimplify(val, rational=True, tolerance=1e-6)
                    val_frac = sp.Rational(val_frac).limit_denominator()
                    valoresX[varSymbol] = val_frac
                else:
                    val_frac = "?"

                rhs_str = str(rhs)
                frm_html += f"{lhs_str:<10} = {rhs_str:<6}  ->  {str(varSymbol)} = {val_frac}\n"
            
            frm_html += f"\n{'-'*80}"
            frm_html += "<br><b>Por lo tanto:</b><br><pre>"
            frm_html += f"<b>X1 = {sp.N(valoresX[x1], 6)};     X2 = {sp.N(valoresX[x2], 6)};    X3 = {sp.N(valoresX[x3], 6)}</b></pre>"
        else:
            frm_html += f"<br>Como |A| = 0, por lo tanto A != LU."

        resultados.append({
            "tipo": "datos",
            "mensaje": frm_html
        })

    except Exception as e:
        resultados.append({
            "tipo": "error",
            "mensaje": f"Error al procesar las ecuaciones: {str(e)}"
        })
    
    return resultados