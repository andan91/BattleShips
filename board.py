from point2d import Point2D
from tile import Tile
from copy import copy
from random import randint
from graphics import egi

class Board(object):
    """Board of the game battleships, it has a size (represents the 
    size of the board, an owner which determines whether the player
    is human or AI, a list of Tiles that i can draw using an initial
    position to draw the tiles"""
    def __init__(self,size,x,y,owner):
        self.size = size
        self.owner = owner
        self.position = Point2D(x,y)
        self.tiles = []
        self.add_tiles(x)
        
    #draws the board as well as the axes on the board
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

        if self.owner == "human":
            egi.text_at_pos(220,550,"Your Board")
            egi.line_by_pos(Point2D(220,547),Point2D(290,547))
        else:
            egi.text_at_pos(840,550,"AI's Board")
            egi.line_by_pos(Point2D(840,547),Point2D(910,547))
        egi.text_at_pos(550,560,"YOUR TURN!")

    
    #add all the tiles required for the board
    '''loop through all the tiles in the list and increase the x and y
    values of the position after each tile is added.
    This will draw the tiles in a grid like fashion'''
    def add_tiles(self,initial_x):
        for y in range(0,self.size):
            for x in range(0,self.size):
                self.tiles.append(Tile("empty",self.position.copy(),self.size,self.owner))
                self.position.x += 48
            self.position.y+= 48
            self.position.x = initial_x

    '''Returns the tile by its position value as a point2D'''
    def get_tile_by_pos(self,x,y):
        for tile in self.tiles:
            if x < tile.position.x + tile.radius and x>tile.position.x - tile.radius:
                if y <tile.position.y + tile.radius and y > tile.position.y - tile.radius:
                    return tile

    #returns a random tile from the board
    def get_random_tile(self):
        random_move = randint(0,99)
        return self.tiles[random_move]


    '''This controls the loading of the ships. It ensures that no illegal move can be made
    and that all ships will fit into the board in a random fashion
    Uses the spawn ship for each of the players ships'''
    def load_ships(self,ships):
        for x in range(len(ships)):
            move = None
            tiles = []
            #loop until a good location is found
            while True:
                #loop until a good initial move is found
                while True:
                    potential_move = self.get_random_tile()
                    if potential_move.is_empty():
                        move = potential_move #if a move is found break
                        break
                if move != None:
                    potential_location = self.spawn_ship(ships[x].size,move)
                    if potential_location != None and len(potential_location)>1:
                        tiles = potential_location
                        break

            for tile in tiles:
                tile.type = "ship"

  

    '''locates a location that a ship of a certain lenght will fit in.
    Checks all possible directions for the ship to be placed, as long as the move is legal it 
    will be allowed.
    This will return an array of tiles that have been found suitable for the ship location
    --------------------------------------------------------------------------------------'''
    def spawn_ship(self,ship,location):
        tile = location
        #check that the initial tile is empty
        if tile.is_empty():
            count = 0
            no_moves = 0 #will check if there are no possible moves remaining
            ship_location = []
            #loop whilst seacrhing for a full location
            while len(ship_location) < ship-1 and count <ship -1 and no_moves<1:
                temp_tile = copy(tile)
                for location in range(1,ship):
                    #if the amount of ships has been reached break from the loop       
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
                    #if the amount of ships has been reached break from the loop  
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
                    #if the amount of ships has been reached break from the loop  
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
                    #if the amount of ships has been reached break from the loop  
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
                    #once a good location has been found insert the original move at 
                    #the front of the array of tiles
                    ship_location.insert(0,tile)
                    return ship_location
                else:
                    return []

    '''-----------------------------------------------------------------------------------'''
                    
    '''Following are checks for empty tiles around a certain tile
    ------------------------------------------------------------------------'''
    #check right
    def is_empty_right(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x+tile.radius*2,
                                              tile.position.y)
        if potential_tile != None:
            if potential_tile.is_empty():
                return True
    
    #check left
    def is_empty_left(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x-tile.radius*2,
                                              tile.position.y)
        if potential_tile != None:
            if potential_tile.is_empty():
                return True

    #check above
    def is_empty_up(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x,
                                              tile.position.y + tile.radius*2)
        if potential_tile != None:
            if potential_tile.is_empty():
                return True

    #check below
    def is_empty_down(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x,
                                              tile.position.y - tile.radius*2)
        if potential_tile != None:
            if potential_tile.is_empty():
                return True
    '''------------------------------------------------------------------------'''


    '''Following functions return the adjacent tile in all directions of the given tile
    ---------------------------------------------------------------------------------'''
    def get_adjactent_tile(self,tile,direction):
        #returns the tile on the right
        if direction == "right":
            tile = self.get_tile_by_pos(tile.position.x + tile.radius*2,tile.position.y)
            if tile != None:
                return tile

        #returns the tile on the left
        if direction == "left":
            tile = self.get_tile_by_pos(tile.position.x - tile.radius*2,tile.position.y)
            if tile != None:
                return tile

        #returns the tile above
        if direction == "up":
            tile = self.get_tile_by_pos(tile.position.x, tile.position.y +
                                        tile.radius*2)
            if tile != None:
                return tile

        #returns the tile below 
        if direction == "down":
            tile = self.get_tile_by_pos(tile.position.x, tile.position.y -
                                        tile.radius*2)
            if tile != None:
                return tile
    '''------------------------------------------------------------------------------'''