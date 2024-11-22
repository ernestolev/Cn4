import tkinter as tk
from tkinter import messagebox
from logic.ai_logic import Conecta4AI
from prolog_bridge import PrologBridge


class Conecta4App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conecta 4")
        self.geometry("600x650")
        self.resizable(False, False)  # Ajustar altura para incluir botones y tablero

        # Crear tablero vacío
        self.tablero = [[" " for _ in range(7)] for _ in range(6)]
        self.turno = "rojo"  # Turno inicial

        # Opciones de IA: Python o Prolog
        self.ia_python = True  # Cambia a False para usar Prolog
        if self.ia_python:
            self.ia = Conecta4AI(color="amarillo")  # IA en Python
        else:
            self.ia = PrologBridge()  # IA en Prolog

        # Configuración de las columnas del grid
        for col in range(7):
            self.columnconfigure(col, weight=1)

        # Crear botón de reinicio
        self.boton_reiniciar = tk.Button(self, text="🔄 Reiniciar Juego", command=self.resetear_juego, bg="red", fg="white", font=("Arial", 12))
        self.boton_reiniciar.grid(row=0, column=0, columnspan=7, pady=10)

        # Crear botones de las columnas (↓)
        self.crear_botones()

        # Crear el canvas del tablero
        self.canvas = tk.Canvas(self, width=600, height=600)
        self.canvas.grid(row=2, column=0, columnspan=7, pady=10)  # Tablero ocupa 7 columnas
        self.dibujar_tablero()

    def dibujar_tablero(self):
        """Dibuja el tablero base."""
        for i in range(7):
            for j in range(6):
                self.canvas.create_oval(
                    i * 85 + 10, j * 85 + 10,
                    i * 85 + 75, j * 85 + 75,
                    outline="black", width=2
                )

    def dibujar_fichas(self):
        """Dibuja las fichas actuales."""
        self.canvas.delete("ficha")  # Elimina fichas previas
        for i in range(6):
            for j in range(7):
                color = "red" if self.tablero[i][j] == "rojo" else "yellow"
                if self.tablero[i][j] != " ":
                    self.canvas.create_oval(
                        j * 85 + 10, (5 - i) * 85 + 10,
                        j * 85 + 75, (5 - i) * 85 + 75,
                        fill=color, outline="black", tags="ficha"
                    )

    def crear_botones(self):
        """Crea botones para cada columna."""
        for i in range(7):
            boton = tk.Button(self, text="↓", command=lambda col=i: self.colocar_ficha(col), bg="Black", fg="white", font=("Arial", 14))
            boton.grid(row=1, column=i, padx=5, pady=5)  # Alinear con las columnas del tablero

    def colocar_ficha(self, columna):   
        """Coloca una ficha en la columna seleccionada."""
        for fila in range(5, -1, -1):
            if self.tablero[fila][columna] == " ":
                self.tablero[fila][columna] = self.turno
                self.dibujar_fichas()
                if self.verificar_ganador(fila, columna):
                    return
                self.turno = "amarillo" if self.turno == "rojo" else "rojo"
                break
        else:
            messagebox.showwarning("Columna llena", "Esa columna está llena.")

        if self.turno == "amarillo":
            self.jugada_ia()

    def verificar_ganador(self, fila, columna):
        """Verifica si hay un ganador."""
        jugador = self.tablero[fila][columna]
        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            line = self.obtener_linea_ganadora(fila, columna, jugador, dx, dy)
            if line:
                self.resaltar_linea(line)
                messagebox.showinfo("¡Ganador!", f"El jugador {jugador} ha ganado!")
                return True
        return False

    def obtener_linea_ganadora(self, fila, columna, jugador, dx, dy):
        """Obtiene las fichas de una línea ganadora si existe."""
        line = []
        for step in range(-3, 4):
            x, y = fila + step * dx, columna + step * dy
            if 0 <= x < 6 and 0 <= y < 7 and self.tablero[x][y] == jugador:
                line.append((x, y))
                if len(line) == 4:
                    return line
            else:
                line = []
        return None

    def resaltar_linea(self, line):
        """Cambia el color de las fichas ganadoras a azul."""
        for x, y in line:
            self.canvas.create_oval(
                y * 85 + 10, (5 - x) * 85 + 10,
                y * 85 + 75, (5 - x) * 85 + 75,
                fill="blue", outline="black", tags="ficha"
            )


    def check_line(self, fila, columna, jugador, dx, dy):
        """Verifica líneas de 4 fichas consecutivas en una dirección."""
        count = 0
        for step in range(-3, 4):
            x, y = fila + step * dx, columna + step * dy
            if 0 <= x < 6 and 0 <= y < 7 and self.tablero[x][y] == jugador:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    def resetear_juego(self):
        """Reinicia el juego."""
        self.tablero = [[" " for _ in range(7)] for _ in range(6)]
        self.turno = "rojo"
        self.dibujar_tablero()
        self.dibujar_fichas()

    def jugada_ia(self):
        """Realiza la jugada de la IA con un retraso."""
        if self.ia_python:
            columna = self.ia.obtener_jugada(self.tablero)
        else:
            resultado = self.ia.jugada_ia(self.tablero, "amarillo")
            columna = resultado[0] if resultado else None

        if columna is not None:
            def realizar_jugada():
                for fila in range(5, -1, -1):
                    if self.tablero[fila][columna] == " ":
                        self.tablero[fila][columna] = "amarillo"
                        self.dibujar_fichas()
                        if self.verificar_ganador(fila, columna):
                            return
                        self.turno = "rojo"
                        break
                else:
                    messagebox.showerror("Error de IA", "La IA no pudo realizar una jugada.")

            self.after(500, realizar_jugada)        
