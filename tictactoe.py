from enum import Enum
from random import randint
from copy import deepcopy


class Color(Enum):
    N = 0
    X = 1,
    O = 2,
    A = 3


def getOpponent(color: Color):
    return Color.X if color == Color.O else Color.O


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

    def possible_moves(self):
        for x in range(3):
            for y in range(3):
                if self.get_color(x, y) == Color.N:
                    continue
                yield x, y


class SuperTicTacToe:
    def __init__(self):
        self.__board = [[TicTacToe() for _ in range(3)] for _ in range(3)]
        self.__next_move = (-1, -1)
        self.__current_move = Color.X

    def make_move(self, x, y, r, c):
        if (x, y) != self.__next_move and self.__next_move != (-1, -1):
            return False
        if not self.get_game(x, y).make_move(r, c, self.__current_move):
            return False
        winner = self.get_game(x, y).get_winner()
        if winner != Color.N:
            self.__board[x][y] = winner
        if not isinstance(self.get_game(r, c), Color):
            self.__next_move = (r, c)
        else:
            self.__next_move = (-1, -1)
        self.__current_move = getOpponent(self.__current_move)
        return True

    def get_game(self, x, y):
        return self.__board[x][y]

    def getPlayer(self):
        return self.__current_move

    def is_any(self):
        return self.__next_move == (-1, -1)

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

    def get_delta(self, player=Color.X) -> int:
        result = 0
        all_ = 0
        for conf in TicTacToe.get_pos():
            winner = self.check_may_win(conf)
            if winner == Color.N:
                continue
            if winner == Color.A:
                all_ += 1
                continue
            result += +1 if winner == Color.X else -1
        result = 3 * (all_ + (result if player == Color.X else -result))
        for line in self.__board:
            for game in line:
                if isinstance(game, TicTacToe):
                    result += game.get_delta(player)
        return result

    def possible_moves(self):
        if self.__next_move == (-1, -1):
            for x in range(3):
                for y in range(3):
                    if isinstance(self.get_game(x, y), Color):
                        continue
                    for move in self.get_game(x, y).possible_moves():
                        yield (x, y), move
        else:
            for move in self.get_game(*self.__next_move).possible_moves():
                yield self.__next_move, move

    def moveRandom(self):
        moves = list(self.possible_moves())
        if len(moves) == 0:
            return getOpponent(self.__current_move)
        ind = randint(0, len(moves) - 1)
        return self.move(moves[ind])

    def move(self, mv):
        (x, y), (r, c) = mv
        self.make_move(x, y, r, c)
        if self.get_winner() != Color.N:
            return self.__current_move
        moves = list(self.possible_moves())
        if len(moves) == 0:
            return getOpponent(self.__current_move)
        return Color.N

