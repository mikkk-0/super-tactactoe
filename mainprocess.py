from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from tictactoe import Color, SuperTicTacToe


class Game:
    def __init__(self):
        self.__root = self.__buttons = self.__board = self.__frames \
            = self.__game = self.__next_move = self.__current_move \
            = self.__commands = self.__ex = None

    def process(self):
        self.__root = Tk()
        self.__buttons = []
        self.__board = Frame(self.__root)
        self.__frames = []
        self.__game = SuperTicTacToe()
        self.__next_move = (-1, -1)
        self.__current_move = Color.X
        self.__commands = ttk.Frame(self.__root, padding=30)
        self.__commands.grid(row=1)

        self.__ex = ttk.Button(self.__commands, text="EXIT", command=self.restart)

        self.__ex.grid()

        self.restart()

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
            return True
        return False

    def tap_button(self, x, y, r, c):
        def f():
            if self.__next_move != (-1, -1) and (x, y) != self.__next_move:
                return
            if self.__game.make_move(x, y, r, c, self.__current_move):
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
                self.__current_move = Color.O if self.__current_move == Color.X else Color.X
                if isinstance(self.__game.get_game(r, c), Color):
                    self.__next_move = (-1, -1)
                    for frs in self.__frames:
                        for frame in frs:
                            if len(list(frame.winfo_children())) != 1:
                                frame["relief"] = "sunken"
                else:
                    self.__next_move = (r, c)
                    self.__frames[r][c]["relief"] = "sunken"
            # print(self.__game.get_delta(self.__current_move))

        return f

    def restart(self):
        self.__board.destroy()
        self.__game = SuperTicTacToe()
        self.__next_move = (-1, -1)
        self.__current_move = Color.X
        self.__board = ttk.Frame(self.__root, padding=10, relief="groove")
        self.__board.grid(row=0)
        self.__buttons = []
        self.__frames = []
        for c in range(13):
            ttk.Label(self.__board, text=("------" if c % 4 else "+")).grid(column=c, row=0)
        for r in range(13):
            ttk.Label(self.__board, text=("|" if r % 4 else "+")).grid(column=0, row=r)

        for row_ in range(3):
            self.__frames.append([])
            for column_ in range(3):
                # in single tictactoe
                self.__buttons.append([])
                self.__frames[-1].append(ttk.Frame(self.__board, padding=5, relief="sunken"))
                self.__frames[-1][-1].grid(column=column_ * 4 + 1, row=row_ * 4 + 1, rowspan=3, columnspan=3)
                for r in range(3):
                    ttk.Label(self.__board, text="|").grid(column=column_ * 4 + 4, row=row_ * 4 + r + 1)
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
