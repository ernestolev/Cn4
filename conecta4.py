# conecta4.py
import tkinter as tk
from tkinter import messagebox
from pyswip import Prolog

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
        self.buttons = []
        for col in range(7):
            button = tk.Button(self.root, text=str(col+1), command=lambda c=col+1: self.player_move(c), font=('Arial', 14), bg='lightblue', fg='black')
            button.grid(row=0, column=col, padx=5, pady=5)
            self.buttons.append(button)
        
        self.board_buttons = [[tk.Canvas(self.root, width=60, height=60, bg='blue', highlightthickness=0) for _ in range(7)] for _ in range(6)]
        for r in range(6):
            for c in range(7):
                self.board_buttons[r][c].grid(row=r+1, column=c, padx=5, pady=5)
                self.board_buttons[r][c].create_oval(5, 5, 55, 55, fill='white')

        self.reset_button = tk.Button(self.root, text="Reiniciar", command=self.reset_game, font=('Arial', 14), bg='lightgreen', fg='black')
        self.reset_button.grid(row=7, columnspan=7, pady=10)

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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conecta 4")
    game = Conecta4(root)
    root.mainloop()
