from math import sqrt, log
from tictactoe import Color, SuperTicTacToe, getOpponent
from random import randint
from datetime import datetime
from copy import deepcopy


class UCTNode:
    def __init__(self, player: Color, move: tuple[tuple[int, int], tuple[int, int]]):
        self.__children: list[UCTNode] = []
        self.__player = player
        self.__visits = 1
        self.__score = 0
        self.__move = move

    def play(self, game: SuperTicTacToe):
        return game.move(self.__move)

    def changeScore(self, dx: int):
        self.__score += dx

    def visit(self):
        self.__visits += 1

    def getOpponent(self):
        return getOpponent(self.__player)

    def getUCB(self, coeff: float) -> float:
        return self.__score / self.__visits + sqrt(coeff / self.__visits)

    def expand(self, game: SuperTicTacToe):
        for move in game.possible_moves():
            self.__children.append(UCTNode(self.getOpponent(), move))

    def findBestChild(self):
        coeff = log(self.__visits)
        best_score = -1e9
        best_child = None
        for child in self.__children:
            if child.getUCB(coeff) > best_score:
                best_score = child.getUCB(coeff)
                best_child = child
        return best_child

    def leaf(self):
        return len(self.__children) == 0

    def getVisits(self):
        return self.__visits

    def getChildren(self):
        for child in self.__children:
            yield child

    def getMove(self):
        return self.__move


class UCT:
    def __init__(self, game: SuperTicTacToe, difficulty: int):
        self.__root = UCTNode(Color.O, ((-1, -1), (-1, -1)))
        self.__game: SuperTicTacToe = game
        self.__root.expand(self.__game)
        self.__maxTime: int = 0
        self.__nodes: dict[int, UCTNode] = {0: self.__root}
        if difficulty == 1:
            self.__maxTime = 1
        elif difficulty == 2:
            self.__maxTime = 5

    def __playout(self, game: SuperTicTacToe) -> Color:
        N = 0
        while N <= 70:
            result = game.moveRandom()
            if result != Color.N:
                return result
            N += 1
        score1 = game.get_delta(Color.X)
        score2 = game.get_delta(Color.O)
        if score1 > score2:
            return Color.X
        if score1 < score2:
            return Color.O
        return Color.N

    def run(self):
        depth = 1
        game = deepcopy(self.__game)
        node = self.__root
        winner = Color.N
        svoConst = 200
        while True:
            if node.leaf():
                if node.getVisits() >= svoConst:
                    node.expand(game)
                    if node.leaf():
                        winner = node.getOpponent()
                        self.__nodes[depth] = node
                        depth += 1
                        break
                    continue
                winner = self.__playout(game)
                break
            node = node.findBestChild()
            self.__nodes[depth] = node
            depth += 1
            if node.play(game) != Color.N:
                winner = game.getPlayer()
                break
        for i in range(depth):
            node = self.__nodes[i]
            node.visit()
            node.changeScore(-1 if winner == node.getOpponent() else 1)

    def suggest(self) -> tuple[tuple[int, int], tuple[int, int]]:
        if self.__maxTime == 0:
            moves = list(self.__game.possible_moves())
            if len(moves) != 0:
                ind = randint(0, len(moves) - 1)
                return moves[ind]
        start = datetime.now()

        while True:
            elapsed = None
            for i in range(500):
                self.run()
                elapsed = datetime.now() - start
                if elapsed.seconds >= self.__maxTime:
                    break
            if elapsed.seconds >= self.__maxTime:
                break

        best = None
        best_score = -1e9
        for child in self.__root.getChildren():
            if child.getVisits() > best_score:
                best = child
                best_score = best.getVisits()

        return best.getMove()
