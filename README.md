# Cn4 - Conecta 4

Este proyecto es un juego de **Conecta 4** desarrollado como **Trabajo de Investigación 3** para el curso de **Programación Lógica y Funcional** en la **Universidad Tecnológica del Perú (UTP)**.  
Autor: **Ernesto Levano U21202486**  

---

## **Descripción del Proyecto**

El proyecto combina **Python** y **Prolog** para implementar un juego de Conecta 4 interactivo.  
- **Python**: Se utiliza para la interfaz gráfica y la interacción con el usuario.
- **Prolog**: Gestiona la lógica de la computadora que juega contra el usuario.

La IA analiza el tablero actual y determina la jugada óptima utilizando reglas lógicas escritas en Prolog.

---

## **Requisitos**

### **Software necesario**
1. **Python** (versión 3.8 o superior).
2. **SWI-Prolog**:
   - Descárgalo desde [swi-prolog.org](https://www.swi-prolog.org/).
3. Bibliotecas de Python:
   - `pyswip` para conectar Python con Prolog.
   - `tkinter` para la interfaz gráfica (generalmente viene preinstalado).

### **Instalación de dependencias**
Si no tienes las dependencias instaladas, ejecútalas en tu terminal:
```bash
pip install pyswip
```

## **Estructura**
```bash
Cn4/
├── conecta4.pl     
├── conecta4.py        
├── requirements.txt  
└── README.md        
```

## **Como ejecutar?**

### **1. Clonar Repo**
Si estás trabajando localmente, asegúrate de que el proyecto esté en tu máquina. Por ejemplo:
```bash
git clone https://github.com/tu-repositorio/cn4.git
cd cn4
```
### **2. Clonar Repo**
Si no has instalado las dependencias necesarias, ejecuta:
```bash 
pip install -r requirements.txt
```
### **3. Ejecutar juego**
En la carpeta principal del proyecto (Cn4), ejecuta:
```bash 
python conecta4.py
```

## **Uso del juego**

1. Inicio del juego:

2. La ventana inicial muestra un tablero vacío y botones para cada columna.
El jugador humano controla las fichas rojas.
Interacción:

3. Haz clic en los botones con flechas ↓ para colocar una ficha en la columna deseada.
El turno alterna entre el jugador humano y la IA.
Condición de victoria:

4. El primer jugador en conectar 4 fichas consecutivas (horizontal, vertical o diagonal) gana.

Haz clic en el botón "🔄 Reiniciar Juego" para empezar una nueva partida.

## **Detalles tecnicos**

### ***Uso de prolog***

- Archivo: conecta4.pl.
- Prolog maneja la lógica de la PC, como:
- Determinar jugadas válidas.
 - Bloquear al jugador humano si está a punto de ganar.
 - Buscar la mejor jugada para ganar.

 ### ***Conexion a Py***

- Utilizamos la biblioteca pyswip para conectar Python con Prolog.

 ### ***Interfaz grafica***
- Desarrollada con tkinter.
- Los elementos principales incluyen:
- Botones para cada columna (↓) alineados con el tablero.
  - Tablero interactivo que muestra las fichas en tiempo real.
  - Botón de reinicio para empezar una nueva partida.