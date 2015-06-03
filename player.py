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

    
    #The list of ships used in the battleships game
    def add_ships(self):
        self.ships.append(Ship(2))
        self.ships.append(Ship(3))
        self.ships.append(Ship(3))
        self.ships.append(Ship(4))
        self.ships.append(Ship(5))

    #used for the AI that will select a random move everytime it is its turn
    def get_random_move(self):
        while True:
            random_move = randint(0,len(self.board.tiles)-1)
            if self.board.tiles[random_move].not_checked():
                break
        return random_move

    def get_predicted_move(self):
        board = self.board
        highest_value = None
        if board.no_hits():
            return self.get_random_move()
        else:
            for tile in self.board.tiles:
                if tile.type == "hit":
                    if highest_value == None:
                        potential_tile = self.check_adjacent_tiles(tile)
                        if potential_tile != None:
                            highest_value = potential_tile
            if highest_value == None:
                return self.get_random_move()
            return highest_value


                        
    def check_adjacent_tiles(self,tile):
        board = self.board
        if board.get_adjactent_tile(tile,"right").not_checked():
            return board.get_adjactent_tile(tile,"right")
        if board.get_adjactent_tile(tile,"left").not_checked():
            return board.get_adjactent_tile(tile,"left")
        if board.get_adjactent_tile(tile,"up").not_checked():
            return board.get_adjactent_tile(tile,"up")
        if board.get_adjactent_tile(tile,"down").not_checked():
            return board.get_adjactent_tile(tile,"down")


                                


    #used for the AI to complete it's move based off of a move it has recieved
    def do_move(self):
        move = self.get_predicted_move()
        if type(move)== int:
            if self.board.tiles[move].is_empty():
                self.board.tiles[move].type = "miss"
            elif self.board.tiles[move].is_hit():
                self.board.tiles[move].type = "hit"
        else:
            if self.board.tiles[self.board.tiles.index(move)].is_empty():
                self.board.tiles[self.board.tiles.index(move)].type = "miss"
            elif self.board.tiles[self.board.tiles.index(move)].is_hit():
                self.board.tiles[self.board.tiles.index(move)].type = "hit"





