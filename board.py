from point2d import Point2D
from tile import Tile
from copy import copy
from random import randint
from graphics import egi

class Board(object):
    """Board of the game battleships"""
    def __init__(self,size,x,y,owner):
        self.size = size
        self.owner = owner
        self.position = Point2D(x,y)
        self.tiles = []
        self.add_tiles(x)
        

    def draw_board(self):
        for tile in self.tiles:
            tile.draw_tile()
        x = copy(self.position.x)
        y = copy(self.position.y)
        for i in range(1,11):
            egi.text_at_pos(x,y - 20,str(i))
            x+= 48
        x = copy(self.position.x)

        for i in range(1,11):
            egi.text_at_pos(x-45,y-50,str(i))
            y-= 48


    
    def add_tiles(self,initial_x):
        for y in range(0,self.size):
            for x in range(0,self.size):
                self.tiles.append(Tile("empty",self.position.copy(),self.size,self.owner))
                self.position.x += 48
            self.position.y+= 48
            self.position.x = initial_x

    def get_tile_by_pos(self,x,y):
        for tile in self.tiles:
            if x < tile.position.x + tile.radius and x>tile.position.x - tile.radius:
                if y <tile.position.y + tile.radius and y > tile.position.y - tile.radius:
                    return tile

    #returns a random tile from the board
    def get_random_tile(self):
        random_move = randint(0,99)
        return self.tiles[random_move]

    def load_ships(self,ships):
        for x in range(len(ships)):
            move = None
            tiles = []
            while True:
                while True:
                    potential_move = self.get_random_tile()
                    if potential_move.is_empty():
                        move = potential_move
                        break
                if move != None:
                    potential_location = self.spawn_ship(ships[x].size,move)
                    if potential_location != None and len(potential_location)>1:
                        tiles = potential_location
                        break

            for tile in tiles:
                tile.type = "ship"

  


    def spawn_ship(self,ship,location):
        tile = location
        if tile.is_empty():
            count = 0
            no_moves = 0
            ship_location = []
            while len(ship_location) < ship-1 and count <ship -1 and no_moves<1:
                temp_tile = copy(tile)
                for location in range(1,ship):       
                    if len(ship_location) == ship:
                        count +=1
                        break             
                    #horizontal check right
                    if self.is_empty_right(temp_tile):
                        ship_location.append(temp_tile)
                        temp_tile = self.get_adjactent_tile(temp_tile,"right")
                        count += 1
                    else:
                        ship_location.clear()
                        count = 0
                        break
                for location in range(1,ship):
                    if len(ship_location) == ship:
                        count +=1
                        break     
                    #horizontal check left
                    if self.is_empty_left(temp_tile):
                        ship_location.append(temp_tile)
                        temp_tile = self.get_adjactent_tile(temp_tile,"left")
                        count += 1
                    else:
                        ship_location.clear()
                        count = 0
                        break
                for location in range(1,ship):
                    if len(ship_location) == ship:
                        count +=1
                        break     
                    #vertical check up
                    if self.is_empty_up(temp_tile):
                        ship_location.append(temp_tile)
                        temp_tile = self.get_adjactent_tile(temp_tile,"up")
                        count += 1
                    else:
                        ship_location.clear()
                        count = 0
                        break
                for location in range(1,ship):
                    if len(ship_location) == ship:
                        count +=1
                        break     
                    #vertical check down
                    if self.is_empty_up(temp_tile):
                        ship_location.append(temp_tile)
                        temp_tile = self.get_adjactent_tile(temp_tile,"down")
                        count += 1
                    else:
                        ship_location.clear()
                        count = 0
                        break
                no_moves += 1

                if ship_location != []:
                    ship_location.insert(0,tile)
                    return ship_location
                else:
                    return []
                    

    def is_empty_right(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x+tile.radius*2,
                                              tile.position.y)
        if potential_tile != None:
            if potential_tile.is_empty():
                return True
    def is_empty_left(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x-tile.radius*2,
                                              tile.position.y)
        if potential_tile != None:
            if potential_tile.is_empty():
                return True
    def is_empty_up(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x,
                                              tile.position.y + tile.radius*2)
        if potential_tile != None:
            if potential_tile.is_empty():
                return True
    def is_empty_down(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x,
                                              tile.position.y - tile.radius*2)
        if potential_tile != None:
            if potential_tile.is_empty():
                return True

    def get_adjactent_tile(self,tile,direction):
        if direction == "right":
            tile = self.get_tile_by_pos(tile.position.x + tile.radius*2,tile.position.y)
            if tile != None:
                return tile
        if direction == "left":
            tile = self.get_tile_by_pos(tile.position.x - tile.radius*2,tile.position.y)
            if tile != None:
                return tile
        if direction == "up":
            tile = self.get_tile_by_pos(tile.position.x, tile.position.y +
                                        tile.radius*2)
            if tile != None:
                return tile
        if direction == "down":
            tile = self.get_tile_by_pos(tile.position.x, tile.position.y -
                                        tile.radius*2)
            if tile != None:
                return tile