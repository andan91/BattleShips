from graphics import egi
from point2d import Point2D

class Tile(object):
    """description of class"""
    def __init__(self,type,position,size,owner):
        self.type = type
        self.position = position
        self.radius = 24
        self.owner = owner

    def draw_tile(self):
        egi.set_pen_color(name = "BLUE")
        egi.rect(self.position.x-self.radius,self.position.y+self.radius,
                 self.position.x+self.radius,self.position.y-self.radius,filled = True)
        egi.set_pen_color(name = "WHITE")
        egi.rect(self.position.x-self.radius,self.position.y+self.radius,
                 self.position.x+self.radius,self.position.y-self.radius)

        if self.type == "hit":
            egi.set_pen_color(name = "GREEN")
            egi.circle(self.position,self.radius/2,filled = True)

        if self.type == "miss":
            egi.set_pen_color(name = "RED")
            egi.cross(self.position,self.radius/2)

        #if self.type == "ship":
        #    egi.set_pen_color(name = "YELLOW")
        #    egi.cross(self.position,self.radius/2)

    def is_empty(self):
        if self.type == "empty":
            return True

    def is_hit(self):
        if self.type == "ship":
            return True

    def not_checked(self):
        if self.type == "ship" or self.type == "empty":
            return True

    def is_clickable(self):
        if self.owner == "human":
            return True
        



