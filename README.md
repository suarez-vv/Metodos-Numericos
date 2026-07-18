# Métodos Numéricos

Aplicación desarrollada en **Python** para la resolución de problemas matemáticos mediante métodos numéricos clásicos.

El proyecto implementa algoritmos para la aproximación de raíces de ecuaciones y la solución de sistemas de ecuaciones lineales, permitiendo visualizar iteraciones, errores aproximados y criterios de paro a través de una interfaz gráfica desarrollada con **PySide6**.

La aplicación integra métodos cerrados y abiertos para el cálculo de raíces, así como técnicas iterativas y de factorización para resolver sistemas lineales. Además, incorpora validación de entradas, procesamiento simbólico mediante **SymPy** y herramientas que facilitan el análisis paso a paso de los procedimientos numéricos utilizados.

Con el objetivo de facilitar su distribución y uso en distintos entornos, el proyecto incluye soporte para generación de ejecutables en Linux y Windows, manejo de dependencias mediante entornos virtuales y scripts de automatización para instalación y empaquetado.

<p align="center">
    <img src="screenshots/menu_principal.png" alt="menu_principal" width="50%"><br>
    <em>Figura 1. Menú principal de la aplicación.</em><br>
</p>

## Tecnologías Utilizadas

- Python
- PySide6
- SymPy
- Expresiones Regulares (Regex)
- Programación Orientada a Objetos
- Interfaces Gráficas (GUI)
- PyInstaller
- Compatibilidad Linux/Windows

## Funcionalidades

### Raíces de Ecuaciones

- Método de Bisección.
- Método de Regla Falsa.
- Método de Newton-Raphson.
- Método de la Secante.
- Evaluación automática de funciones.
- Derivación simbólica mediante SymPy.
- Cálculo de error aproximado relativo (Ea).
- Criterios de paro configurables.

<p align="center">
    <img src="screenshots/raices_ecuaciones.png" alt="raices_ecuaciones" width="50%"><br>
    <em>Figura 2. Selección de métodos para el cálculo de raíces de ecuaciones.</em><br>
</p>

### Sistemas de Ecuaciones

- Método de Jacobi.
- Método de Gauss-Seidel.
- Factorización LU mediante Doolittle.
- Resolución de sistemas lineales de tres ecuaciones.
- Visualización paso a paso de iteraciones.
- Cálculo de errores aproximados por variable.

### Interfaz Gráfica

- Menú principal interactivo.
- Configuración personalizada para cada método.
- Teclado matemático integrado.
- Validación de entradas.
- Presentación detallada de resultados.


## Métodos Implementados

### Métodos Cerrados

- Bisección.
- Regla Falsa.

### Métodos Abiertos

- Newton-Raphson.
- Secante.

<p align="center">
    <img src="screenshots/ejemplo_secante.png" alt="ejemplo_secante" width="50%"><br>
    <em>Figura 3. Configuración y ejecución del método de la Secante.</em><br>
</p>


### Sistemas de Ecuaciones

- Jacobi.
- Gauss-Seidel.
- Doolittle.

<p align="center">
    <img src="screenshots/ejemplo_jacobi.png" alt="ejemplo_jacobi" width="50%"><br>
    <em>Figura 4. Resolución de sistemas lineales mediante el método de Jacobi.</em><br>
</p>

## Estructura del Proyecto

```text
Metodos-Numericos/
│
├── screenshots/
│   ├── menu_principal.png
│   ├── raices_ecuaciones.png
│   ├── ejemplo_secante.png
│   └── ejemplo_jacobi.png
│
├── images/
│   ├── App.png
│   └── App.ico
│
├── src/
│   ├── menuMetodos.py         -> Interfaz gráfica principal
│   ├── raicesEcuaciones.py    -> Métodos para raíces de ecuaciones
│   └── sistemasEcuaciones.py  -> Métodos para sistemas de ecuaciones
│
├── requirements.txt          -> Dependencias del proyecto
│
├── build.sh                  -> Instalación de dependencias en Linux
├── build.bat                 -> Instalación de dependencias en Windows
│
├── package.sh                -> Generación de ejecutable para Linux
├── package.bat               -> Generación de ejecutable para Windows
│
├── README.md
└── .gitignore
```

## Instalación

### Linux

Crear el entorno virtual e instalar dependencias:

```bash
chmod +x build.sh

./build.sh
```

### Windows

Ejecutar:

```cmd
build.bat
```


## Dependencias

El proyecto utiliza las siguientes bibliotecas:

```text
PySide6
SymPy
```

Las dependencias se encuentran definidas en:

```text
requirements.txt
```

## Ejecución

### Linux

```bash
source .venv/bin/activate

python src/menuMetodos.py
```

### Windows

```cmd
.venv\Scripts\activate

python src\menuMetodos.py
```

## Generación de Ejecutables

### Linux

```bash
chmod +x package.sh

./package.sh
```

Genera:

```text
Metodos-Numericos
```

### Windows

```cmd
package.bat
```

Genera:

```text
Metodos-Numericos.exe
```

## Compatibilidad

La aplicación fue desarrollada para Windows y posteriormente adaptada para Linux.

La compatibilidad multiplataforma se implementó mediante:

- Uso de rutas relativas para recursos.
- Carga dinámica de archivos mediante `resource_path()`.
- Entornos virtuales de Python.
- Scripts específicos para Linux y Windows.
- Empaquetado mediante PyInstaller.


## Conceptos Aplicados

Durante el desarrollo del proyecto se aplicaron conocimientos en:

- Métodos numéricos.
- Análisis numérico.
- Programación Orientada a Objetos.
- Desarrollo de interfaces gráficas.
- Manejo de expresiones matemáticas.
- Cálculo simbólico.
- Estructuras recursivas.
- Validación de datos.
- Compatibilidad multiplataforma.

## Autor

- Suárez Vega, Vladimir

## Nota

Proyecto desarrollado originalmente con fines académicos y educativos para practicar y fortalecer conocimientos relacionados con análisis numérico, resolución de ecuaciones, sistemas lineales y desarrollo de aplicaciones utilizando Python.

### Historial del Proyecto

* Desarrollo original: **septiembre-noviembre de 2025.**

* Adaptación multiplataforma (Linux/Windows): **julio de 2026.**