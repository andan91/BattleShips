from board import Board
from ship import Ship
from copy import copy
from random import randint
from graphics import egi
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
        self.enemy_ships = [2,3,3,4,5]

    
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

    #performs checks to return a move that is smarter than just picking out a random
    #square when there are no potential moves
    def calc_best_random(self):
        best_tile = None
        best_value = 0
        for tile in self.board.tiles:
            value = 0
            if tile.not_checked and self.board.is_surrounded(tile):
                for direction in self.board.directions:
                    for x in range(1,2):
                        temp = self.board.get_adjactent_tile(tile,direction,x)
                        if temp.not_checked():
                            value +=1
            if best_value == 0 or best_value< value:
                best_value = value
                best_tile = tile
        return best_tile

    '''Once a ship has been hit, the AI switches into an agressive search mode using data
    to search the surrounding area for more hits before switching back to a randomly 
    chosen move'''
    def get_predicted_move(self):
        highest_value = None
        if self.board.no_hits():
            return self.get_random_move()
        else:
            for tile in self.board.tiles:
                if tile.type == "hit":
                    if highest_value == None:
                        potential_tile = self.check_adjacent_tiles(tile)
                        if potential_tile != None:
                            highest_value = potential_tile
            if highest_value == None:
                #return self.get_random_move()
                while True:
                     potential_move = self.calc_best_random()
                     if not potential_move.not_checked():
                         return self.get_random_move()
                     return potential_move
            return highest_value


    #checks the adjacent tiles                     
    def check_adjacent_tiles(self,tile):
        if tile != None:
            temp_tile = self.board.get_adjactent_tile(tile,"right",1)
            if temp_tile != None and temp_tile.not_checked():
                return self.board.get_adjactent_tile(tile,"right",1)
            temp_tile = self.board.get_adjactent_tile(tile,"left",1)
            if temp_tile != None and temp_tile.not_checked():
                return self.board.get_adjactent_tile(tile,"left",1)
            temp_tile = self.board.get_adjactent_tile(tile,"up",1)
            if temp_tile != None and temp_tile.not_checked():
                return self.board.get_adjactent_tile(tile,"up",1)
            temp_tile = self.board.get_adjactent_tile(tile,"down",1)
            if temp_tile != None and temp_tile.not_checked():
                return self.board.get_adjactent_tile(tile,"down",1)                               


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

    #updates the AI's list of potential ships, and when a ship is sunk it updates its list
    def update_enemy_ships(self):
        if self.enemy_ships.count(2) == 1 and self.board.sunk_ship(2,"patrol") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies patrol")
            self.enemy_ships.remove(2)
        if self.enemy_ships.count(3) == 2 and self.board.sunk_ship(3,"sub") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies sub")
            self.enemy_ships.remove(3)
        if self.enemy_ships.count(3) == 1 and self.board.sunk_ship(3,"sub") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies second sub")
            self.enemy_ships.remove(3)
        if self.enemy_ships.count(4) == 1 and self.board.sunk_ship(4,"battleship") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies battleship")
            self.enemy_ships.remove(4)
        if self.enemy_ships.count(5) == 1 and self.board.sunk_ship(5,"carrier") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies carrier")
            self.enemy_ships.remove(5)




