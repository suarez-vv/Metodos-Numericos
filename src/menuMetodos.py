#Autor: Suárez, V.V.
import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QCheckBox, QLineEdit, QGridLayout, QSizePolicy, QTextEdit, QMessageBox
from PySide6.QtGui import QIcon, QIntValidator, QDoubleValidator, QFont, QColor, QKeyEvent
from PySide6.QtCore import Qt, QEvent

#Logica de metodos
import raicesEcuaciones
import sistemasEcuaciones

# Permite localizar recursos tanto en ejecución normal como en ejecutables generados con PyInstaller.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

ICONO = resource_path("images/App.png")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Métodos Numéricos")
        self.setGeometry(500, 150, 500, 500)
        self.setWindowIcon(QIcon(ICONO))

        #Widget de cada pantalla
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        #Diccionario para pantallas de configuracion
        self.config_screens = {}

        #Menu dividido
        opciones_raices = [
            ("Métodos Abiertos", "raices_abiertos"),
            ("Métodos Cerrados", "raices_cerrados")
        ]

        opciones_SisEcuaciones = [
            ("Gauss-Seidel", "gauss_seidel"),
            ("Jacobi", "jacobi"),
            ("Factorización con Doolittle", "doolittle")
        ]

        self.menu_raices = SubMenuMetodos("Raíces de Ecuaciones", opciones_raices, self.mostrar_submenu, lambda: self.stacked.setCurrentWidget(self.menu))
        self.menu_sistemas = SubMenuMetodos("Solución a Sistemas de Ecuaciones", opciones_SisEcuaciones, self.mostrar_config, lambda: self.stacked.setCurrentWidget(self.menu))

        #Menu principal
        opciones_principal = [
            ("Raíces de ecuaciones", self.menu_raices),
            ("Solución a Sistemas de Ecuaciones", self.menu_sistemas),
            ("Salir del programa", "salir")
        ]
        self.menu = SubMenuMetodos("Menú Principal", opciones_principal, self.mostrar_submenu, back_callback = None)
        self.stacked.addWidget(self.menu)

        #Menus de raices
        opciones_abiertos = [
            ("Newton-Raphson", "newton_raphson"),
            ("Secante", "secante")
        ]

        opciones_cerrados = [
            ("Bisección", "biseccion"),
            ("Regla Falsa", "regla_falsa")
        ]
        self.menu_abiertos = SubMenuMetodos("Métodos Abiertos", opciones_abiertos, self.mostrar_config, lambda: self.stacked.setCurrentWidget(self.menu_raices))
        self.menu_cerrados = SubMenuMetodos("Métodos Cerrados", opciones_cerrados, self.mostrar_config, lambda: self.stacked.setCurrentWidget(self.menu_raices))

        self.stacked.addWidget(self.menu_raices)
        self.stacked.addWidget(self.menu_sistemas)
        self.stacked.addWidget(self.menu_abiertos)
        self.stacked.addWidget(self.menu_cerrados)

        self.stacked.setCurrentWidget(self.menu)

    def mostrar_menu(self, widget):
        self.stacked.setCurrentWidget(widget)
    
    def mostrar_submenu(self, submenu):
        if submenu == "raices_abiertos":
            self.stacked.setCurrentWidget(self.menu_abiertos)
        elif submenu == "raices_cerrados":
            self.stacked.setCurrentWidget(self.menu_cerrados)
        elif submenu in ["gauss_seidel", "jacobi"]:
            self.mostrar_config(submenu)
        elif submenu == "doolittle":
            self.mostrar_config(submenu)  #Doolittle
        elif submenu in ["regresion_lineal", "regresion_polinomial"]:
            self.mostrar_config(submenu)
        elif isinstance(submenu, QWidget):
            self.stacked.setCurrentWidget(submenu)
        elif submenu == "salir":
            QApplication.quit()
        else:
            self.mostrar_config(submenu)

    def mostrar_config(self, metodo):
        #Muestra la pantalla de configuracion del metodo que se elija

        #Metodos de sistemas de ecuaciones
        if metodo == "gauss_seidel": 
            if metodo in self.config_screens:
                pantalla_vieja = self.config_screens.pop(metodo)
                self.stacked.removeWidget(pantalla_vieja)
                pantalla_vieja.deleteLater()

            pantalla = configSisEcuaciones(self.volver_menu, mainWindow=self, metodo = "gauss_seidel")
            self.config_screens[metodo] = pantalla
            self.stacked.addWidget(pantalla)
            self.stacked.setCurrentWidget(pantalla)
            return

        if metodo == "jacobi":
            if metodo in self.config_screens:
                pantalla_vieja = self.config_screens.pop(metodo)
                self.stacked.removeWidget(pantalla_vieja)
                pantalla_vieja.deleteLater()

            pantalla = configSisEcuaciones(self.volver_menu, mainWindow=self, metodo = "jacobi")
            self.config_screens[metodo] = pantalla
            self.stacked.addWidget(pantalla)
            self.stacked.setCurrentWidget(pantalla)
            return

        if metodo == "doolittle": 
            if metodo in self.config_screens:
                pantalla_vieja = self.config_screens.pop(metodo)
                self.stacked.removeWidget(pantalla_vieja)
                pantalla_vieja.deleteLater()

            pantalla = configSisEcuaciones(self.volver_menu, mainWindow=self, metodo = "doolittle")
            self.config_screens[metodo] = pantalla
            self.stacked.addWidget(pantalla)
            self.stacked.setCurrentWidget(pantalla)
            return

        #Metodos de raices
        if metodo in self.config_screens:
            pantalla_vieja = self.config_screens.pop(metodo)
            self.stacked.removeWidget(pantalla_vieja)
            #Creamos la pantalla si aun no existe
        pantalla = ConfigRaicesEcuaciones(metodo, self.volver_menu, mainWindow=self)
        self.config_screens[metodo] = pantalla
        self.stacked.addWidget(pantalla)
        self.stacked.setCurrentWidget(self.config_screens[metodo])

    def volver_menu(self):
        #Funcion para poder regresar al menu principal
        self.stacked.setCurrentWidget(self.menu)

class SubMenuMetodos(QWidget):
    def __init__(self, titulo, opciones, switch_callback, back_callback):
        super().__init__()
        layout_subMenu = QVBoxLayout()
        self.setLayout(layout_subMenu)

        layout_subMenu.addWidget(QLabel(f"<b>{titulo}</b>"))

        for texto, valor in opciones:
            btn_texto = QPushButton(texto)
            btn_texto.clicked.connect(lambda checked, v=valor: switch_callback(v))
            layout_subMenu.addWidget(btn_texto)

        #Regresar
        if back_callback:
            btn_volver = QPushButton("Volver al menú principal")
            btn_volver.clicked.connect(back_callback)
            layout_subMenu.addWidget(btn_volver)

class ConfigRaicesEcuaciones(QWidget):
    def __init__(self, metodo, back_callback, guardar_callback=None, mainWindow = None):
        super().__init__()
        self.metodo = metodo
        self.back_callback = back_callback
        self.guardar_callback = guardar_callback
        self.mainWindow = mainWindow
        self.init_ui()

    def init_ui(self):
        layoutCM = QVBoxLayout()
        self.setLayout(layoutCM)

        labelCM = QLabel(f"<b>Configuración para el método: {self.metodo.upper()}</b>")
        layoutCM.addWidget(labelCM)

        #Validar que sean números
        val_entero = QIntValidator(1, 9999)
        val_decimal = QDoubleValidator(-9999.0, 9999.0, 10)

        #Mostrar los criterios de paro
        layoutCM.addWidget(QLabel("<b>Criterios de paro:</b>"))

        #Raiz
        layoutCM.addWidget(QLabel("Encontrar la raíz de la función es considerado un criterio de paro por defecto."))

        #Es
        self.checkbox_es = QCheckBox("Error tolerado (Es)")
        self.input_es = QLineEdit()
        self.input_es.setPlaceholderText("Ingresa el número de cifras significativas")
        self.input_es.setEnabled(False)
        self.input_es.setValidator(val_entero)
        self.checkbox_es.toggled.connect(lambda checked: self.input_es.setEnabled(checked))
        layoutCM.addWidget(self.checkbox_es)
        layoutCM.addWidget(self.input_es)

        #Numero de iteraciones
        self.checkbox_iter = QCheckBox("Número máximo de iteraciones")
        self.input_iter = QLineEdit()
        self.input_iter.setPlaceholderText("Ingresa el número máximo de iteraciones")
        self.input_iter.setEnabled(False)
        self.input_iter.setValidator(val_entero)
        self.checkbox_iter.toggled.connect(lambda checked: self.input_iter.setEnabled(checked))
        layoutCM.addWidget(self.checkbox_iter)
        layoutCM.addWidget(self.input_iter)

        #Valores de X
        layoutCM.addWidget(QLabel("<b>Valores iniciales: <b>"))

        if self.metodo in ["biseccion", "regla_falsa"]:
            self.input_xi = QLineEdit()
            self.input_xi.setPlaceholderText("Ingresa el valor de Xi")
            self.input_xi.setValidator(val_decimal)
            self.input_xs = QLineEdit()
            self.input_xs.setPlaceholderText("Ingresa el valor de Xs")
            layoutCM.addWidget(self.input_xi)
            layoutCM.addWidget(self.input_xs)
        
        elif self.metodo == "newton_raphson":
            self.input_x0 = QLineEdit()
            self.input_x0.setPlaceholderText("Ingresa el valor de X0")
            self.input_x0.setValidator(val_decimal)
            layoutCM.addWidget(self.input_x0)

        elif self.metodo == "secante":
            self.input_xl1 = QLineEdit()
            self.input_xl1.setPlaceholderText("Ingresa el valor de X(-1)")
            self.input_xl1.setValidator(val_decimal)
            self.input_x0 = QLineEdit()
            self.input_x0.setPlaceholderText("Ingresa el valor de X0")
            self.input_x0.setValidator(val_decimal)
            layoutCM.addWidget(self.input_xl1)
            layoutCM.addWidget(self.input_x0)

        #Etiqueta exponenetes
        layoutCM.addWidget(QLabel("<br><b>Para usar exponentes escriba porfavor: ^(2), ^(x), ^(2x), ^(-x), ^(10), etc...</b><br>"))

        #Campo para la ecuacion
        layoutCM.addWidget(QLabel("<b>Ecuación:</b>"))
        self.input_ecuacion = QLineEdit()
        self.input_ecuacion.setPlaceholderText("Escribe la ecuación")
        font = QFont("Consolas, 12")
        self.input_ecuacion.setFont(font)
        layoutCM.addWidget(self.input_ecuacion)

        self.input_ecuacion.installEventFilter(self)

        #Teclado
        teclado_layout = QGridLayout()
        botones = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('+', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('-', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('*', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('/', 3, 2), ('^', 3, 3),
            ('x', 4, 0), ('e', 4, 1), ('ln', 4, 2), ('log10', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('⌫', 5, 2), ('→', 5, 3)
        ]
        
        for texto, fila, col in botones:
            btn_tec = QPushButton(texto)
            btn_tec.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if texto == '→':
                btn_tec.setStyleSheet("background-color: lightgreen; font-weight: bold;")
            elif texto == '⌫':
                btn_tec.setStyleSheet("background-color: lightcoral; font-weight: bold;")
            else:
                btn_tec.setStyleSheet("font-size: 14px;")

            btn_tec.clicked.connect(lambda checked, t=texto: self.tecla_presionada(t))
            teclado_layout.addWidget(btn_tec, fila, col)

        layoutCM.addLayout(teclado_layout)

        btnVolver = QPushButton("Volver al menú principal")
        btnVolver.clicked.connect(self.back_callback)
        layoutCM.addWidget(btnVolver)

    def tecla_presionada(self, tecla):
        texto = self.input_ecuacion.text()

        if tecla == '⌫':
            self.input_ecuacion.setText(texto[:-1])
            return
        elif tecla == '→':
            if not self.camposObligatorios():    
                return
            resumen = self.mostrarDatos()
            self.mainWindow.stacked.addWidget(resumen)
            self.mainWindow.stacked.setCurrentWidget(resumen)
        elif tecla == '^':
            texto += '^'
        elif tecla in ('ln', 'log10'):
            texto += tecla + '('
        else:
            if tecla.isalpha() and tecla not in ('x', 'e'):
                return
            texto += tecla
        
        self.input_ecuacion.setText(self.superIndice(texto))
    
    def superIndice(self, texto):
        mapa_super = str.maketrans('0123456789+-x', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ˣ')
        resultado = ""
        i=0
        while i < len(texto):
            if texto[i] == '^':
                i += 1
                exp = ""

                if i >= len(texto):
                    resultado += '^'
                    break

                if texto[i] in "+-":
                    exp += texto[i]
                    i += 1

                while i < len(texto) and texto[i].isdigit():
                    exp += texto[i]
                    i+=1
                #Positivo o negativo en el exponente
                if i < len(texto) and texto[i] == "x":
                    exp += 'x'
                    i += 1

                if exp == "" and i < len(texto) and texto[i] == '^':
                    i += 1
                    exp = ""
                    if i < len(texto) and texto[i] in "+-":
                        exp += texto[i]
                        i += 1
                    while i < len(texto) and texto[i].isdigit():
                        exp += texto[i]
                        i += 1
                    if i < len(texto) and texto[i] == 'x':
                        exp += 'x'
                        i += 1
                if exp:
                    resultado += exp.translate(mapa_super)
                else:
                    resultado += '^'

            else:
                resultado += texto[i]
                i+=1
        return resultado
    
    def camposObligatorios(self):
        valido = True
        if self.checkbox_es.isChecked() and not self.input_es.text():
            self.input_es.setStyleSheet("border: 1px solid red;")
            valido = False
        if self.checkbox_iter.isChecked() and not self.input_iter.text():
            self.input_iter.setStyleSheet("border: 1px solid red;")
            valido = False
        
        #Valores de cada metodo
        if self.metodo in ["biseccion", "regla_falsa"]:
            if not self.input_xi.text():
                self.input_xi.setStyleSheet("border: 1px solid red;")
                valido = False
            if not self.input_xs.text():
                self.input_xs.setStyleSheet("border: 1px solid red;")
                valido = False
        elif self.metodo == "newton_raphson" and not self.input_x0.text():
            self.input_x0.setStyleSheet("border: 1px solid red;")
            valido =  False
        elif self.metodo == "secante":
            if not self.input_xl1.text():
                self.input_xl1.setStyleSheet("border: 1px solid red;")
                valido = False
            if not self.input_x0.text():
                self.input_x0.setStyleSheet("border: 1px solid red;")
                valido = False
        
        return valido
    
    def iniciar_iteraciones(self):
        ecuacion = self.input_ecuacion.text()
        metodo = self.metodo
        Es = float(self.input_es.text()) if self.checkbox_es.isChecked() and self.input_es.text() else None
        iteraciones = int(self.input_iter.text()) if self.checkbox_iter.isChecked() and self.input_iter.text() else None

        pEs = self.checkbox_es.isChecked()

        if metodo == "biseccion":
            Xi = float(self.input_xi.text())
            Xs = float(self.input_xs.text())
            resultados = raicesEcuaciones.biseccion(ecuacion, Xi, Xs, Es, pEs, iteraciones)
            texto = self.formatear_resultados(resultados)
        
        elif metodo == "regla_falsa":
            Xi = float(self.input_xi.text())
            Xs = float(self.input_xs.text())
            resultados = raicesEcuaciones.regla_falsa(ecuacion, Xi, Xs, Es, pEs, iteraciones)
            texto = self.formatear_resultados(resultados)
        
        elif metodo == "newton_raphson":
            Xa = float(self.input_x0.text())
            resultados = raicesEcuaciones.newtonRaphson(ecuacion, Xa, Es, pEs, iteraciones)
            texto = self.formatear_resultados(resultados)
        elif metodo == "secante":
            Xp = float(self.input_xl1.text())
            Xa = float(self.input_x0.text())
            resultados = raicesEcuaciones.secante(ecuacion, Xp, Xa, Es, pEs, iteraciones)
            texto = self.formatear_resultados(resultados)

        resultado_widget = QWidget()
        layout_resultado = QVBoxLayout()
        resultado_widget.setLayout(layout_resultado)

        label_result = QLabel("<b>Resultados:</b>")
        layout_resultado.addWidget(label_result)

        area = QTextEdit()
        area.setReadOnly(True)
        area.setHtml(texto)
        layout_resultado.addWidget(area)

        btn_volver = QPushButton("Volver al menú principal")
        btn_volver.clicked.connect(self.back_callback)
        layout_resultado.addWidget(btn_volver)

        self.mainWindow.stacked.addWidget(resultado_widget)
        self.mainWindow.stacked.setCurrentWidget(resultado_widget)
    
    def mostrarDatos(self):
        self.datos_widget = QWidget()
        layout_datos = QVBoxLayout()
        self.datos_widget.setLayout(layout_datos)

        #Nombre del metodo
        layout_datos.addWidget(QLabel(f"<b> Resumen del método: {self.metodo.upper()}</b>"))

        #Ecuacion
        layout_datos.addWidget(QLabel(f"<b>Ecuación:</b> {self.input_ecuacion.text()}"))

        #Valores de cada metodo
        layout_datos.addWidget(QLabel("<b> Valores iniciales:</b>"))
        if self.metodo in ["biseccion", "regla_falsa"]:
            layout_datos.addWidget(QLabel(f"Xi = {self.input_xi.text()}"))
            layout_datos.addWidget(QLabel(f"Xs = {self.input_xs.text()}"))
        elif self.metodo == "newton_raphson":
            layout_datos.addWidget(QLabel(f"X0 = {self.input_x0.text()}"))
        elif self.metodo == "secante":
            layout_datos.addWidget(QLabel(f"X(-1) = {self.input_xl1.text()}"))
            layout_datos.addWidget(QLabel(f"X0 = {self.input_x0.text()}"))
        
        #Criterios de paro seleccionado
        layout_datos.addWidget(QLabel("<b>Criterios de paro seleccionados:</b>"))
        if self.checkbox_es.isChecked():
            layout_datos.addWidget(QLabel(f"|Ea| < Es"))
        if self.checkbox_iter.isChecked():
            layout_datos.addWidget(QLabel(f"Número de iteraciones = {self.input_iter.text()}"))

        btn_iniciar = QPushButton("Iniciar iteraciones")
        btn_iniciar.clicked.connect(self.iniciar_iteraciones)
        layout_datos.addWidget(btn_iniciar)

        btnVolver = QPushButton("Volver al menú principal")
        btnVolver.clicked.connect(self.back_callback)
        layout_datos.addWidget(btnVolver)

        return self.datos_widget
    
    def formatear_resultados(self, resultados):
        texto = ""
        mostradoDatos = False

        for item in resultados:
            tipo = item.get("tipo", "")
            mensaje = item.get("mensaje", "")

            if tipo == "datos":
                if not mostradoDatos:
                    texto += f"<br>{mensaje}<br>"
                    texto += f"<b>{'-'*85}</b><br>"
                    mostradoDatos = True
                continue    
            if tipo == "error":
                texto += f"<br><b>{mensaje}</b><br>"
            elif tipo == "info":
                texto += f"{mensaje}<br>"
            elif tipo == "iteracion":
                texto += f"<b>{'-'*85}</b><br><br>"
                texto += f"{mensaje}<br>"
            elif tipo == "resultado":
                texto += f"<b>{'-'*85}</b><br><br>"
                texto += f"<br>--- {mensaje} ---<br>"
            else:
                texto += f"{mensaje}\n"

        return texto
    
    def keyPressEvent(self, event):
        texto = self.input_ecuacion.text()
        tecla = event.text()

        if tecla.isdigit() or tecla in ['+', '-', '*', '/', '.', '(', ')', '^']:
            self.input_ecuacion.setText(self.superIndice(texto + tecla))
        elif tecla in ['x', 'e']:
            self.input_ecuacion.setText(texto + tecla)
        elif event.key() == Qt.Key_Backspace:
            self.input_ecuacion.setText(texto[:-1])
        elif event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            print("Ecuación final:", self.input_ecuacion.text())
        else:
            event.ignore

    def eventFilter(self, obj, event):
        if(obj == self.input_ecuacion and event.type() == QEvent.KeyPress):
            tecla = event.text()

            if tecla.isdigit() or tecla in ['+', '-', '*', '/', '.', '(', ')', '^']:
                return False
            elif tecla in ['x', 'e']:
                return False
            elif event.key() in [Qt.Key_Backspace, Qt.Key_Return, Qt.Key_Enter]:
                return False
            else:
                return True
        
        return super().eventFilter(obj, event)
    
            
class configSisEcuaciones(QWidget):
    def __init__(self, back_callback, mainWindow = None, metodo = None):
        super().__init__()
        self.back_callback = back_callback
        self.mainWindow = mainWindow
        self.metodo = metodo
        self.num_ecuaciones = 3
        self.linea_activa = None
        self.init_ui()

    def init_ui(self):
        self.layout_sisEcu = QVBoxLayout()
        self.setLayout(self.layout_sisEcu)
    
        self.layout_sisEcu.addWidget(QLabel("<b>Sistema de 3 ecuaciones:</b>"))

        if self.metodo != "doolittle":
            #Criterios de paro
            self.layout_sisEcu.addWidget(QLabel("<b> Criterios de paro: </b>"))

            #Es (Error tolerado)
            self.checkbox_es = QCheckBox("Error tolerador (Es)")
            self.input_es = QLineEdit()
            self.input_es.setValidator(QIntValidator(1, 9999))
            self.input_es.setEnabled(False)
            self.input_es.setPlaceholderText("Número de cifras significativas")
            self.checkbox_es.toggled.connect(lambda checked: self.input_es.setEnabled(checked))
            self.layout_sisEcu.addWidget(self.checkbox_es)
            self.layout_sisEcu.addWidget(self.input_es)

            #Error Ea a calcular
            self.layout_sisEcu.addWidget(QLabel("<b> Error Ea a calcular: </b>"))
            self.layout_sisEcu.addWidget(QLabel("<b> Selecciona al menos un Ea para calcular</b>"))
            layout_ea = QHBoxLayout()
            self.checkbox_eaX1 = QCheckBox("Ea para X1")
            self.checkbox_eaX2 = QCheckBox("Ea para X2")
            self.checkbox_eaX3 = QCheckBox("Ea para X3")

            layout_ea.addWidget(self.checkbox_eaX1)
            layout_ea.addWidget(self.checkbox_eaX2)
            layout_ea.addWidget(self.checkbox_eaX3)

            self.layout_sisEcu.addLayout(layout_ea)

            #Numero de iteraciones
            self.layout_sisEcu.addWidget(QLabel("<br>"))
            self.checkbox_iter = QCheckBox("Número máximo de iteraciones")
            self.input_iter = QLineEdit()
            self.input_iter.setValidator(QIntValidator(1, 9999))
            self.input_iter.setEnabled(False)
            self.input_iter.setPlaceholderText("Número máximo de iteraciones")
            self.checkbox_iter.toggled.connect(lambda checked: self.input_iter.setEnabled(checked))
            self.layout_sisEcu.addWidget(self.checkbox_iter)
            self.layout_sisEcu.addWidget(self.input_iter)

        #Valores iniciales
        if self.metodo in ["gauss_seidel", "jacobi"]:
            self.layout_sisEcu.addWidget(QLabel("<b>Valores iniciales:</b>"))
            layout_valIni = QHBoxLayout()

            if self.metodo == "jacobi":
                self.input_X1 = QLineEdit(); self.input_X1.setPlaceholderText("X1")
                self.input_X2 = QLineEdit(); self.input_X2.setPlaceholderText("X2")
                self.input_X3 = QLineEdit(); self.input_X3.setPlaceholderText("X3")
                layout_valIni.addWidget(self.input_X1)
                layout_valIni.addWidget(self.input_X2)
                layout_valIni.addWidget(self.input_X3)
            else:
                self.input_X2 = QLineEdit(); self.input_X2.setPlaceholderText("X2")
                self.input_X3 = QLineEdit(); self.input_X3.setPlaceholderText("X3")
                layout_valIni.addWidget(self.input_X2)
                layout_valIni.addWidget(self.input_X3)
            
            self.layout_sisEcu.addLayout(layout_valIni)
        
        if self.metodo == "doolittle":
            self.layout_sisEcu.addWidget(QLabel("<br><br><br><br><br>"))
            
            

        #Ecuaciones
        self.layout_sisEcu.addWidget(QLabel("<b> Escribe las ecuaciones (Después de aplicar pivoteo, si es necesario):</b>"))
        self.input_ecuaciones = []

        for i in range(3):
            linea = QLineEdit()
            linea.setPlaceholderText(f"Ecuación {i+1}")
            font = QFont("Consolas", 12)
            linea.setFont(font)
            self.layout_sisEcu.addWidget(linea)
            self.input_ecuaciones.append(linea)
            linea.installEventFilter(self)

        #Teclado
        self.layout_sisEcu.addWidget(QLabel("<b> Teclado: </b>"))

        layout_teclado = QGridLayout()

        botones = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('+', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('-', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('=', 2, 3),
            ('0', 3, 0), ('X1', 3, 1), ('X2', 3, 2), ('X3', 3, 3),
                         ('.', 4, 1), ('⌫', 4, 2), ('→', 4, 3)  
        ]
        
        for texto, fila, col in botones:
            btn_tecla = QPushButton(texto)
            btn_tecla.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if texto == '→':
                btn_tecla.setStyleSheet("background-color: lightgreen; font-weight: bold;")
            elif texto == '⌫':
                btn_tecla.setStyleSheet("background-color: lightcoral; font-weight: bold;")
            else:
                btn_tecla.setStyleSheet("font-size: 14px")
            btn_tecla.setFocusPolicy(Qt.NoFocus)
            btn_tecla.clicked.connect(lambda checked, t=texto: self.tecla_presionada(t))
            layout_teclado.addWidget(btn_tecla, fila, col)
        
        self.layout_sisEcu.addLayout(layout_teclado)

        #Volver al menu
        btn_volver = QPushButton("Volver al menú principal")
        btn_volver.clicked.connect(self.back_callback)
        self.layout_sisEcu.addWidget(btn_volver)

    def tecla_presionada(self, tecla):
        foco = QApplication.focusWidget()
        target = None

        if isinstance(foco, QLineEdit):
            target = foco
        elif self.linea_activa is not None:
            target = self.linea_activa
        elif self.input_ecuaciones: 
                target = self.input_ecuaciones[0]

        if target is None:
            return
        
        texto = target.text()

        if tecla == '⌫':
            target.setText(texto[:-1])
        elif tecla == '→':
            if not self.camposObligatorios():
                return
            resumen = self.mostrarDatos()
            self.mainWindow.stacked.addWidget(resumen)
            self.mainWindow.stacked.setCurrentWidget(resumen)
            
        else:
            texto += tecla
            target.setText(texto)

    def camposObligatorios(self):
        valido = True
        metodo = getattr(self, "metodo", None)
        faltantes = []

        if metodo != "doolittle":  
            if self.checkbox_es.isChecked() and not self.input_es.text():
                self.input_es.setStyleSheet("border: 1px solid red;")
                valido = False
            if self.checkbox_iter.isChecked() and not self.input_iter.text():
                self.input_iter.setStyleSheet("border: 1px solid red;")
                valido = False
        
        for i, line in enumerate(self.input_ecuaciones, start=1):
            if not line.text().strip():
                line.setStyleSheet("border: 1px solid red;")
                valido = False
                faltantes.append(f"Ecuación {i}")
        
        if metodo in ("gauss_seidel", "jacobi") and not( 
            self.checkbox_eaX1.isChecked() or self.checkbox_eaX2.isChecked() or self.checkbox_eaX3.isChecked()
        ):
            QMessageBox.warning(self, "Error", "Selecciona al menos un Ea a calcular (X1, X2 o X3).")
            valido =  False
        
        if metodo == "gauss_seidel":
            if not self.input_X2.text().strip():
                faltantes.append("X2 incial")
            if not self.input_X3.text().strip():
                faltantes.append("X3 incial")
        
        elif metodo == "jacobi":
            if not self.input_X1.text().strip():
                faltantes.append("X1 incial")
            if not self.input_X2.text().strip():
                faltantes.append("X2 incial")
            if not self.input_X3.text().strip():
                faltantes.append("X3 incial")
        
        elif metodo == "doolittle":
            pass
        
        if faltantes:
            QMessageBox.warning(
                self,
                "Campos incompletos",
                f"Por favor completa los siguientes campos: <br><br>- " + "<br>- ".join(faltantes)
            )
            valido =  False

        return valido
    
    def iniciar_iteraciones(self):
        metodo = self.metodo

        if metodo != "doolittle":
            ea_sel = []
            if self.checkbox_eaX1.isChecked():
                ea_sel.append("X1")
            if self.checkbox_eaX2.isChecked():
                ea_sel.append("X2")
            if self.checkbox_eaX3.isChecked():
                ea_sel.append("X3")
            
            Es = float(self.input_es.text()) if self.checkbox_es.isChecked() and self.input_es.text() else None
            iteraciones = int(self.input_iter.text()) if self.checkbox_iter.isChecked() and self.input_iter.text() else None
            
        ecuaciones = [line.text() for line in self.input_ecuaciones]
        
            
        if metodo == "gauss_seidel":
            x2Ini = float(self.input_X2.text()) if self.input_X2.text() else 0.0
            x3Ini = float(self.input_X3.text()) if self.input_X3.text() else 0.0
            resultados = sistemasEcuaciones.gauss_Seidel(ecuaciones, ea_sel, (Es), iteraciones, x2Ini, x3Ini)

        elif metodo == "jacobi":
            x1Ini = float(self.input_X1.text()) if self.input_X1.text() else 0.0
            x2Ini = float(self.input_X2.text()) if self.input_X2.text() else 0.0
            x3Ini = float(self.input_X3.text()) if self.input_X3.text() else 0.0
            resultados = sistemasEcuaciones.jacobi(ecuaciones, ea_sel, (Es), iteraciones, x1Ini, x2Ini, x3Ini)

        else:
            resultados = sistemasEcuaciones.doolittle(ecuaciones)
        
        texto = self.formatear_resultados(resultados)

        resultado_widget = QWidget()
        layout_resultado = QVBoxLayout()
        resultado_widget.setLayout(layout_resultado)

        label_result = QLabel("<b>Resultados:</b>")
        layout_resultado.addWidget(label_result)

        area = QTextEdit()
        area.setReadOnly(True)
        area.setHtml(texto)
        layout_resultado.addWidget(area)

        btn_volver = QPushButton("Volver al menú principal")
        btn_volver.clicked.connect(self.back_callback)
        layout_resultado.addWidget(btn_volver)

        self.mainWindow.stacked.addWidget(resultado_widget)
        self.mainWindow.stacked.setCurrentWidget(resultado_widget)
    
    def mostrarDatos(self):
        metodo = self.metodo
        self.datos_widget = QWidget()
        layout_datos = QVBoxLayout()
        self.datos_widget.setLayout(layout_datos)

        #Nombre del metodo
        layout_datos.addWidget(QLabel(f"<b> Resumen del método: {metodo.upper()}</b>"))

        #Ecuacion
        layout_datos.addWidget(QLabel(f"<b>Ecuaciones:</b>"))
        ecuaciones = []

        for line in self.input_ecuaciones:
            if isinstance(line, QLineEdit):
                texto = line.text().strip()
                if texto:
                    ecuaciones.append(texto)

        if ecuaciones:
            for eq_texto in ecuaciones:
                layout_datos.addWidget(QLabel(eq_texto))

        else:
                layout_datos.addWidget(QLabel("<b>No se ingresaron las ecuaciones</b>"))

        if metodo != "doolittle":
            #Valores de cada metodo
            layout_datos.addWidget(QLabel("<b> Valores iniciales:</b>"))
            if metodo == "gauss_seidel":
                layout_datos.addWidget(QLabel(f"X2 = {self.input_X2.text()}"))
                layout_datos.addWidget(QLabel(f"X3 = {self.input_X3.text()}"))
            elif metodo == "jacobi":
                layout_datos.addWidget(QLabel(f"X1 = {self.input_X1.text()}"))
                layout_datos.addWidget(QLabel(f"X2 = {self.input_X2.text()}"))
                layout_datos.addWidget(QLabel(f"X3 = {self.input_X3.text()}"))
            else:
                pass
            
            #Criterios de paro seleccionado
            layout_datos.addWidget(QLabel("<b>Criterios de paro seleccionados:</b><br>"))
            if self.checkbox_es.isChecked():
                Es = float(self.input_es.text()) if self.checkbox_es.isChecked() and self.input_es.text() else None

            
                if hasattr(self, "checkbox_eaX1") and self.checkbox_eaX1.isChecked():
                    layout_datos.addWidget(QLabel(f"|Ea| < Es ({(0.5*10**(2-Es))}%) - Para X1"))
                if hasattr(self, "checkbox_eaX2") and self.checkbox_eaX2.isChecked():
                    layout_datos.addWidget(QLabel(f"|Ea| < Es ({(0.5*10**(2-Es))}%) - Para X2"))
                if hasattr(self, "checkbox_eaX3") and self.checkbox_eaX3.isChecked():
                    layout_datos.addWidget(QLabel(f"|Ea| < Es ({(0.5*10**(2-Es))}%) - Para X3"))


            if self.checkbox_iter.isChecked():
                valorIter = self.input_iter.text() if hasattr(self, 'input_iter') else ""
                layout_datos.addWidget(QLabel(f"Número máximo de iteraciones = {valorIter}"))

        if metodo == "doolittle":
            btn_iniciar = QPushButton("Iniciar método")
        else:
            btn_iniciar = QPushButton("Iniciar iteraciones")

        
        btn_iniciar.clicked.connect(self.iniciar_iteraciones)
        layout_datos.addWidget(btn_iniciar)

        btnVolver = QPushButton("Volver al menú principal")
        btnVolver.clicked.connect(self.back_callback)
        layout_datos.addWidget(btnVolver)

        return self.datos_widget
    
    def formatear_resultados(self, resultados):
        texto = ""
        mostradoDatos = False

        for item in resultados:
            tipo = item.get("tipo", "")
            mensaje = item.get("mensaje", "")

            if tipo == "datos":
                if not mostradoDatos:
                    texto += f"<br>{mensaje}<br>"
                    texto += f"<b>{'-'*64}</b><br>"
                    mostradoDatos = True
                continue    
            if tipo == "error":
                texto += f"<br><b>{mensaje}</b><br>"
            elif tipo == "info":
                texto += f"{mensaje}<br>"
            elif tipo == "iteracion":
                texto += f"{mensaje}<br>"
                texto += f"<b>{'-'*70}</b><br><br>"
            elif tipo == "resultado":
                texto += f"<b>{'-'*70}</b><br><br>"
                texto += f"<br>--- {mensaje} ---<br>"
            else:
                texto += f"{mensaje}\n"

        return texto
    
    def eventFilter(self, obj, event):
        if isinstance(obj, QLineEdit):
            if event.type() == QEvent.FocusIn:
                self.linea_activa = obj
            elif event.type() == QEvent.FocusOut:
                pass
            
            if event.type() == QEvent.KeyPress:
                tecla = event.text()
                if tecla.isdigit() or tecla in ['+', '-', '.', 'x', '=']:
                    return False
                elif event.key() in [Qt.Key_Backspace, Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab]:
                    return False
                
                elif tecla in ["0123456789"]:
                    return False
                
                elif tecla.upper() in ["X", "X1", "X2","X3"]:
                    return False
                
                else: return True
                
        
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())