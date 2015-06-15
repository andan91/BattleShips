from graphics import egi
from point2d import Point2D

class Tile(object):
    """An idividual tile, with a type (empty, ship, hit, miss), a position in the form
    of a Point2D, and a radius to deteremine the size of the tile created"""
    def __init__(self,type,position,size,owner):
        self.type = type
        self.position = position
        self.radius = 24
        self.owner = owner
        self.color = "BLUE"
        self.ship_type = None

    '''Draws the individual tile. Using the raidus to draw a proper rectangle
    if the type of the tile is different or is changed at some point due to
    a player or AI choosing it, then the additional draw information is layed over
    the top.'''
    def draw_tile(self):
        egi.set_pen_color(name = self.color)
        egi.rect(self.position.x-self.radius,self.position.y+self.radius,
                 self.position.x+self.radius,self.position.y-self.radius,filled = True)
        egi.set_pen_color(name = "WHITE")
        egi.rect(self.position.x-self.radius,self.position.y+self.radius,
                 self.position.x+self.radius,self.position.y-self.radius)

        #if the tile has been hit
        if self.type == "hit":
            egi.set_pen_color(name = "GREEN")
            egi.circle(self.position,self.radius/2,filled = True)
            '''Easy identification of tile types
            --------------------------------------------------------------------------
            ENABLE THIS IF YOU WISH TO SEE THE TILES OF THE SHIPS AS THEY ARE REVEALED
            -----------------------------------------------------------------------'''
            #if self.ship_type == "patrol":
            #    self.color = "PINK"
            #elif self.ship_type == "sub":
            #    self.color = "YELLOW"
            #elif self.ship_type == "destroyer":
            #    self.color = "RED"
            #elif self.ship_type == "battleship":
            #    self.color = "BLACK"
            #elif self.ship_type == "carrier":
            #    self.color = "GREEN"

        #if the tile was hit but missed
        if self.type == "miss":
            egi.set_pen_color(name = "RED")
            egi.cross(self.position,self.radius/2)

    #returns true if the tile is an empty tile
    def is_empty(self):
        if self.type == "empty":
            return True

    #returns true if the tile chosen is a ship tile
    def is_hit(self):
        if self.type == "ship":
            return True

    #used by the AI to select a move that it has not yet chosen
    def not_checked(self):
        if self.type == "ship" or self.type == "empty":
            return True

    #Used by the human player, will return true if the area they have
    #clicked on is a tile.
    def is_clickable(self):
        if self.owner == "human":
            return True

    def is_miss(self):
        if self.type == "miss":
            return True
        



