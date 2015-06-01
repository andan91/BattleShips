from board import Board
from ship import Ship
class Player(object):
    """description of class"""
    def __init__(self,type,board):
        self.type = type
        self.board = board
        self.ships = []
        self.add_ships()
        self.guess_count = 0

    def add_ships(self):
        self.ships.append(Ship(2))
        self.ships.append(Ship(3))
        self.ships.append(Ship(3))
        self.ships.append(Ship(4))
        self.ships.append(Ship(5))

