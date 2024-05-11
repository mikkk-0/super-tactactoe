from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from tictactoe import Color, SuperTicTacToe
from UCT import UCT
from copy import deepcopy


class Game:
    def __init__(self):
        self.__root = self.__buttons = self.__board = self.__frames \
            = self.__game = self.__commands = self.__ex = None
        self.__difficulty = 0

    def changeDiff(self, newVal):
        self.__difficulty = int(float(newVal))
        self.__d_label["text"] = f"Сложность: {self.__difficulty}"

    def process(self):
        self.__root = Tk()
        self.__buttons = []
        self.__board = Frame(self.__root)
        self.__frames = []
        self.__game = SuperTicTacToe()
        self.__commands = ttk.Frame(self.__root, padding=30)
        self.__commands.grid(row=1)

        self.__d_label = ttk.Label(self.__commands, text="Сложность: 0")

        self.__d_label.grid(row = 0)

        self.__d_scale = ttk.Scale(self.__commands, from_=0.0, to=2.9999, length=200, command=self.changeDiff)

        self.__d_scale.grid(row=1)

        self.__ex = ttk.Button(self.__commands, text="RESTART", command=self.restart)

        self.__ex.grid(row=2)

        self.__root.mainloop()

    @staticmethod
    def color_str(winner):
        return 'X' if winner == Color.X else 'O'

    def check_global(self):
        winner = self.__game.get_winner()
        if winner != Color.N:
            for bts in self.__buttons:
                for button in bts:
                    button["command"] = lambda: None
            for frs in self.__frames:
                for frame in frs:
                    frame["relief"] = "flat"
            # print(f"GLOBAL WIN: {Game.color_str(winner)}")
            winner = Game.color_str(winner)
            showinfo(title="GAME OVER", message=f"WINNER: {winner}")
            self.__d_scale = ttk.Scale(self.__commands, from_=0.0, to=2.9999, length=200, command=self.changeDiff)
            self.__d_scale.grid(row=1)
            return True
        return False

    def tap_button(self, x, y, r, c):
        def f():
            if self.__game.make_move(x, y, r, c):
                for frs in self.__frames:
                    for frame in frs:
                        if len(list(frame.winfo_children())) != 1:
                            frame["relief"] = "flat"
                winner = self.__game.get_game(x, y)
                if isinstance(winner, Color):
                    # print(f"WON {Game.color_str(winner)}")
                    for button in self.__buttons[3 * x + y]:
                        button.destroy()
                    self.__buttons[3 * x + y] = []
                    ttk.Label(self.__frames[x][y], text=(Game.color_str(winner)), font=("Arial", 30)).grid(
                        row=x * 4 + 1, column=y * 4 + 1, rowspan=3, columnspan=3)
                    if self.check_global():
                        return
                else:
                    self.__buttons[x * 3 + y][3 * r + c]["text"] = winner.get_color(r, c)
                if self.__game.is_any():
                    for frs in self.__frames:
                        for frame in frs:
                            if len(list(frame.winfo_children())) != 1:
                                frame["relief"] = "sunken"
                else:
                    self.__frames[r][c]["relief"] = "sunken"
            if self.__game.getPlayer() == Color.O:
                (X, Y), (R, C) = UCT(deepcopy(self.__game), self.__difficulty).suggest()
                self.tap_button(X, Y, R, C)()
            # print(self.__game.get_delta(self.__current_move))

        return f

    def restart(self):
        self.__board.destroy()
        self.__game = SuperTicTacToe()
        self.__board = ttk.Frame(self.__root, padding=10, relief="groove")
        self.__board.grid(row=0)
        self.__buttons = []
        self.__frames = []
        self.__d_scale.destroy()
        for c in range(13):
            ttk.Label(self.__board, text=("------" if c % 4 else "+")).grid(column=c, row=0)
        for r in range(13):
            ttk.Label(self.__board, text=("|\n" if r % 4 else "+")).grid(column=0, row=r)

        for row_ in range(3):
            self.__frames.append([])
            for column_ in range(3):
                # in single tictactoe
                self.__buttons.append([])
                self.__frames[-1].append(ttk.Frame(self.__board, padding=5, relief="sunken"))
                self.__frames[-1][-1].grid(column=column_ * 4 + 1, row=row_ * 4 + 1, rowspan=3, columnspan=3)
                for r in range(3):
                    ttk.Label(self.__board, text="|\n").grid(column=column_ * 4 + 4, row=row_ * 4 + r + 1)
                for c in range(3):
                    ttk.Label(self.__board, text="------").grid(column=column_ * 4 + c + 1, row=row_ * 4 + 4)
                ttk.Label(self.__board, text="+").grid(column=column_ * 4 + 4, row=row_ * 4 + 4)
                for r in range(3):
                    for c in range(3):
                        self.__buttons[-1].append(
                            ttk.Button(self.__frames[-1][-1], text="", command=self.tap_button(row_, column_, r, c),
                                       width=3))
                        self.__buttons[-1][-1].grid(column=c, row=r, sticky="NESW")

        # print(games, buttons)
