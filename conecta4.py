import tkinter as tk
from tkinter import messagebox
import os



# Lógica Prolog importada
from pyswip import Prolog

ruta_prolog = os.path.join(os.path.dirname(__file__), "conecta4.pl")


class Conecta4:
    def __init__(self, root):
        self.root = root
        self.prolog = Prolog()
        self.prolog.consult("conecta4.pl")
        self.init_board()
        self.create_widgets()
        self.current_player = 'R'

    def init_board(self):
        list(self.prolog.query("init_board"))

    def create_widgets(self):
        # Crear barra de menús
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Crear sección "Juego"
        self.game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Juego", menu=self.game_menu)
        self.game_menu.add_command(label="Nuevo Juego", command=self.reset_game)
        self.game_menu.add_separator()  # Separador
        self.game_menu.add_command(label="Salir", command=self.root.quit)

        # Crear sección "Ayuda"
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ayuda", menu=self.help_menu)
        self.help_menu.add_command(label="Instrucciones", command=self.show_instructions)
        self.help_menu.add_separator()  # Separador
        self.help_menu.add_command(label="Versión", command=self.show_version)

        # Crear botones del tablero de juego
        self.buttons = []
        for col in range(7):
            button = tk.Button(self.root, text=str(col+1), command=lambda c=col+1: self.player_move(c), font=('Arial', 14), bg='lightblue', fg='black')
            button.grid(row=1, column=col, padx=5, pady=5)
            self.buttons.append(button)

        # Crear el tablero de juego
        self.board_buttons = [[tk.Canvas(self.root, width=60, height=60, bg='blue', highlightthickness=0) for _ in range(7)] for _ in range(6)]
        for r in range(6):
            for c in range(7):
                self.board_buttons[r][c].grid(row=r+2, column=c, padx=5, pady=5)
                self.board_buttons[r][c].create_oval(5, 5, 55, 55, fill='white')

        # Botón de reiniciar
        self.reset_button = tk.Button(self.root, text="Reiniciar", command=self.reset_game, font=('Arial', 14), bg='lightgreen', fg='black')
        self.reset_button.grid(row=8, columnspan=7, pady=10)

    def player_move(self, column):
        if self.current_player == 'R':
            if list(self.prolog.query(f"can_insert_piece({column})")):
                list(self.prolog.query(f"insert_piece({column}, 'R')"))
                self.update_board()
                if list(self.prolog.query("check_winner('R')")):
                    self.end_game("¡Ganaste!")
                else:
                    self.current_player = 'Y'
                    self.root.after(500, self.computer_move)

    def computer_move(self):
        if self.current_player == 'Y':
            list(self.prolog.query("computer_move"))
            self.update_board()
            if list(self.prolog.query("check_winner('Y')")):
                self.end_game("¡Perdiste!")
            else:
                self.current_player = 'R'

    def update_board(self):
        board = list(self.prolog.query("board(B)"))
        if board:
            board = board[0]['B']
            for r in range(6):
                for c in range(7):
                    color = 'white'
                    if board[r][c] == 'R':
                        color = 'red'
                    elif board[r][c] == 'Y':
                        color = 'yellow'
                    self.board_buttons[r][c].create_oval(5, 5, 55, 55, fill=color)

    def end_game(self, message):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        messagebox.showinfo("Fin del juego", message)

    def reset_game(self):
        self.init_board()
        self.update_board()
        for button in self.buttons:
            button.config(state=tk.NORMAL)
        self.current_player = 'R'

    def show_instructions(self):
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instrucciones del Juego")
        instructions_label = tk.Label(instructions_window, text="Instrucciones de Conecta 4:\n\n"
                                                               "1. El objetivo del juego es colocar 4 fichas consecutivas "
                                                               "en una fila, columna o diagonal.\n\n"
                                                               "2. Los jugadores se alternan para colocar fichas en las columnas.\n\n"
                                                               "3. El primer jugador en conseguir 4 fichas consecutivas gana.\n\n"
                                                               "4. El jugador 'R' juega primero.\n\n"
                                                               "5. Si el tablero se llena y nadie ha ganado, el juego termina en empate.",
                                       font=('Arial', 12), padx=20, pady=20)
        instructions_label.pack()

    def show_version(self):
        version_window = tk.Toplevel(self.root)
        version_window.title("Versión")
        version_label = tk.Label(version_window, text="Versión 1.0", font=('Arial', 12), padx=20, pady=20)
        version_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conecta 4")
    game = Conecta4(root)
    root.mainloop()
