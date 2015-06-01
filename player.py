from board import Board
from ship import Ship
from random import randint
class Player(object):
    """description of class"""
    def __init__(self,type,board):
        self.type = type
        self.board = board
        self.ships = []
        self.add_ships()
        self.guess_count = 0
        self.turn = True
        self.turn_count = 0

    def add_ships(self):
        self.ships.append(Ship(2))
        self.ships.append(Ship(3))
        self.ships.append(Ship(3))
        self.ships.append(Ship(4))
        self.ships.append(Ship(5))

    def get_move(self):
        while True:
            random_move = randint(0,len(self.board.tiles)-1)
            if self.board.tiles[random_move].not_checked():
                break
        return random_move

    def do_move(self):
        move = self.get_move()
        if self.board.tiles[move].is_empty():
            self.board.tiles[move].type = "miss"
        elif self.board.tiles[move].is_hit():
            self.board.tiles[move].type = "hit"



