from enum import Enum


class Color(Enum):
    N = 0
    X = 1,
    O = 2,
    A = 3


class TicTacToe:
    def __init__(self):
        self.__board = [[Color.N for _ in range(3)] for _ in range(3)]

    def make_move(self, x, y, color):
        if self.__board[x][y] != Color.N:
            return False
        self.__board[x][y] = color
        return True

    def get_color(self, x, y):
        return 'X' if self.__board[x][y] == Color.X else ('O' if self.__board[x][y] == Color.O else "")

    @staticmethod
    def get_pos():
        pos = [[(0, 0), (0, 1), (0, 2)],
               [(1, 0), (1, 1), (1, 2)],
               [(2, 0), (2, 1), (2, 2)],
               [(0, 0), (1, 0), (2, 0)],
               [(0, 1), (1, 1), (2, 1)],
               [(0, 2), (1, 2), (2, 2)],
               [(0, 0), (1, 1), (2, 2)],
               [(0, 2), (1, 1), (2, 0)]
               ]
        for conf in pos:
            yield conf

    def check_win(self, conf):
        colors = set()
        for x, y in conf:
            colors.add(self.__board[x][y])
        if len(colors) == 1:
            return list(colors)[0]
        return Color.N

    def check_may_win(self, conf):
        colors = set()
        for x, y in conf:
            colors.add(self.__board[x][y])
        if len(colors) == 1:
            return Color.A
        if len(colors) == 2 and list(colors)[0] == Color.N:
            return list(colors)[1]
        return Color.N

    def get_winner(self):
        for conf in TicTacToe.get_pos():
            winner = self.check_win(conf)
            if winner != Color.N:
                return winner
        return Color.N

    def get_delta(self, move=Color.X):
        result = 0
        all = 0
        for conf in TicTacToe.get_pos():
            winner = self.check_may_win(conf)
            if winner == Color.N:
                continue
            if winner == Color.A:
                all += 1
                continue
            result += +1 if winner == Color.X else -1
        return all + (result if move == Color.X else -result)


class SuperTicTacToe:
    def __init__(self):
        self.__board = [[TicTacToe() for _ in range(3)] for _ in range(3)]

    def make_move(self, x, y, r, c, color):
        if not self.__board[x][y].make_move(r, c, color):
            return False
        winner = self.__board[x][y].get_winner()
        if winner != Color.N:
            self.__board[x][y] = winner
        return True

    def get_game(self, x, y):
        return self.__board[x][y]

    def check_may_win(self, conf):
        colors = set()
        for x, y in conf:
            if isinstance(self.__board[x][y], TicTacToe):
                colors.add(Color.N)
            else:
                colors.add(self.__board[x][y])
        if len(colors) == 1:
            return Color.A
        if len(colors) == 2 and list(colors)[0] == Color.N:
            return list(colors)[1]

    def check_win(self, conf):
        colors = set()
        for x, y in conf:
            if isinstance(self.__board[x][y], TicTacToe):
                colors.add(Color.N)
            else:
                colors.add(self.__board[x][y])
        if len(colors) == 1 and list(colors)[0] != Color.N:
            return list(colors)[0]
        return Color.N

    def get_winner(self):
        for conf in TicTacToe.get_pos():
            winner = self.check_win(conf)
            if winner != Color.N:
                return winner
        return Color.N

    def get_delta(self, move=Color.X):
        result = 0
        all = 0
        for conf in TicTacToe.get_pos():
            winner = self.check_may_win(conf)
            if winner == Color.N:
                continue
            if winner == Color.A:
                all += 1
                continue
            result += +1 if winner == Color.X else -1
        result = 3 * (all + (result if move == Color.X else -result))
        for line in self.__board:
            for game in line:
                if isinstance(game, TicTacToe):
                    result += game.get_delta(move)
        return result
