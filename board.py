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
        self.ship_types = ["patrol","sub","sub","battleship","carrier"]
        self.add_tiles(x)
        self.directions = ['left','right','up','down']
        self.enemy_ships = [2,3,3,4,5]

        
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
        egi.text_at_pos(100,600,"Once game has finished press R to reload the boards")
        self.draw_ship_text()

    
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

    #clears the board by setting all the types to empty
    def reset_board(self):
        for tile in self.tiles:
            tile.type = "empty"
            tile.color = "GREY"
            egi.text_at_pos(530,540,"Press R to reload the board")

    def draw_ship_text(self):
        x = 1150
        if self.owner == "AI": 
            y = 220
            egi.text_at_pos(x,y,"Your Ships")
        else:
            y = 360
            egi.text_at_pos(x,y,"Computer's ships")

        #patrol text
        if self.enemy_ships.count(2) == 1:
            egi.text_at_pos(x,y-20,"Ship: Patrol")
        else:
            egi.set_pen_color(name = "RED")
            egi.line_by_pos(Point2D(x,y-20+5),Point2D(x+90,y-20+5))
            egi.text_at_pos(x,y-20,"Ship: Destroyed")

        #submarine text
        if self.enemy_ships.count(3) == 2:
            egi.text_at_pos(x,y-40,"Ship: Submarine ")  
        else:
            egi.set_pen_color(name = "RED")
            egi.line_by_pos(Point2D(x,y-40+5),Point2D(x+90,y-40+5))
            egi.text_at_pos(x,y-40,"Ship: Destroyed")
        #destoyer text
        if self.enemy_ships.count(3) == 2 or self.enemy_ships.count(3) == 1 :
                egi.text_at_pos(x,y-60,"Ship: Destroyer ")
        else:
            egi.set_pen_color(name = "RED")
            egi.line_by_pos(Point2D(x,y-60+5),Point2D(x+90,y-60+5))
            egi.text_at_pos(x,y-40,"Ship: Destroyed")
        #battleship text
        if self.enemy_ships.count(4) == 1:
            egi.text_at_pos(x,y-80,"Ship: Battleship")
        else:
            egi.set_pen_color(name = "RED")
            egi.line_by_pos(Point2D(x,y-80+5),Point2D(x+90,y-80+5))
            egi.text_at_pos(x,y-80,"Ship: Destroyed") 

        #carrier text
        if self.enemy_ships.count(5) == 1:
            egi.text_at_pos(x,y-100,"Ship: Aircraft Carrier")
        else:
            egi.set_pen_color(name = "RED")
            egi.line_by_pos(Point2D(x,y-100+5),Point2D(x+90,y-100+5))
            egi.text_at_pos(x,y-100,"Ship: Destroyed") 
          

    #check if the board is empty
    def is_board_empty(self):
        count = 0
        for tile in self.tiles:
            if tile.type != "empty":
                count +=1
        #if there are any tiles that are not listed as "empty" then the board is not empty
        if count>0:
            return False
        else:
            return True
    #returns a copy of the board class
    def copy_board(self):
        return copy(self)

    def no_hits(self):
        count = 0
        for tile in self.tiles:
            if tile.type == "hit":
                count += 1
        if count >0:
            return False
        else:
            return True


    '''This controls the loading of the ships. It ensures that no illegal move can be made
    and that all ships will fit into the board in a random fashion
    Uses the spawn ship for each of the players ships'''
    def load_ships(self,ships):
        sub_count = 0
        for x in range(0,len(ships)):
            
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
                
                if len(tiles)-1 == 2:
                    tile.ship_type = "patrol"
                if len(tiles)-1 == 3:
                    if sub_count == 1:
                        tile.ship_type = "destroyer"
                if len(tiles)-1 == 3:
                    if sub_count == 0:
                        tile.ship_type = "sub"
                        sub_count += 1
                if len(tiles)-1 == 4:
                    tile.ship_type = "battleship"
                if len(tiles)-1 == 5:
                    tile.ship_type = "carrier"
                

  

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
                        temp_tile = self.get_adjactent_tile(temp_tile,"right",1)
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
                    if self.is_empty_up(temp_tile):
                        ship_location.append(temp_tile)
                        temp_tile = self.get_adjactent_tile(temp_tile,"up",1)
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
                    if self.is_empty_left(temp_tile):
                        ship_location.append(temp_tile)
                        temp_tile = self.get_adjactent_tile(temp_tile,"left",1)
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
                        temp_tile = self.get_adjactent_tile(temp_tile,"down",1)
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
    def get_adjactent_tile(self,tile,direction,depth):
        #returns the tile on the right
        if direction == "right":
            tile = self.get_tile_by_pos(tile.position.x + tile.radius*(1+depth),tile.position.y)
            if tile != None:
                return tile

        #returns the tile on the left
        if direction == "left":
            tile = self.get_tile_by_pos(tile.position.x - tile.radius*(1+depth),tile.position.y)
            if tile != None:
                return tile

        #returns the tile above
        if direction == "up":
            tile = self.get_tile_by_pos(tile.position.x, tile.position.y +
                                        tile.radius*(1+depth))
            if tile != None:
                return tile

        #returns the tile below 
        if direction == "down":
            tile = self.get_tile_by_pos(tile.position.x, tile.position.y -
                                        tile.radius*(1+depth))
            if tile != None:
                return tile
    '''------------------------------------------------------------------------------'''

    '''------------------------------------------------------------------------------
    This is the condition for the board to have been won by either player. Once all the 
    ships have been hit then the board will reset   
    ---------------------------------------------------------------------------------'''
    def win_condition(self):
        count = 0
        #check for the winner if there is one
        for tile in self.tiles:
            if tile.type == "hit":
                count += 1
        if count >= 17:
            return True
        else:
            return False
    '''------------------------------------------------------------------------------'''

    
    '''------------------------------------------------------------------------------
    This checks for the condition of whether a certain ship has been sunk and then 
    returns true if it has been, letting the players know that the certain ship has been
    sunk
    ---------------------------------------------------------------------------------'''
    def sunk_ship(self,shipLength,shipType):
        sink_count = 0
        for tile in self.tiles:
            if tile.type == "hit":
                #adds to the count to check if a certain ship has been sunk
                if tile.ship_type == shipType:
                    sink_count += 1
        if sink_count == shipLength:
            return True
        else:
            return False
    '''------------------------------------------------------------------------------'''

    '''Following are checks for missed tiles around a certain tile
    ------------------------------------------------------------------------'''
    #check right
    def is_miss_right(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x+tile.radius*2,
                                              tile.position.y)
        if potential_tile != None:
            if potential_tile.is_miss():
                return True
    
    #check left
    def is_miss_left(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x-tile.radius*2,
                                              tile.position.y)
        if potential_tile != None:
            if potential_tile.is_miss():
                return True

    #check above
    def is_miss_up(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x,
                                              tile.position.y + tile.radius*2)
        if potential_tile != None:
            if potential_tile.is_miss():
                return True

    #check below
    def is_miss_down(self,tile):
        potential_tile = self.get_tile_by_pos(tile.position.x,
                                              tile.position.y - tile.radius*2)
        if potential_tile != None:
            if potential_tile.is_miss():
                return True
    '''------------------------------------------------------------------------'''

    #checks to see whether the tile is surrounded
    def is_surrounded(self,tile):
        if self.is_miss_right(tile) and self.is_miss_left(tile) and self.is_miss_up(tile) and self.is_miss_down(tile):
            return True

    def update_enemy_ships(self):
        if self.enemy_ships.count(2) == 1 and self.sunk_ship(2,"patrol") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies patrol")
            self.enemy_ships.remove(2)
        if self.enemy_ships.count(3) == 2 and self.sunk_ship(3,"sub") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies sub")
            self.enemy_ships.remove(3)
        if self.enemy_ships.count(3) == 1 and self.sunk_ship(3,"destroyer") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies second sub")
            self.enemy_ships.remove(3)
        if self.enemy_ships.count(4) == 1 and self.sunk_ship(4,"battleship") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies battleship")
            self.enemy_ships.remove(4)
        if self.enemy_ships.count(5) == 1 and self.sunk_ship(5,"carrier") == True:
            egi.text_at_pos(530,520,"You have sunk the enemies carrier")
            self.enemy_ships.remove(5)

    


