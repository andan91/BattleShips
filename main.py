from graphics import egi, KEY
from point2d import Point2D
from pyglet import window, clock, text
from pyglet.gl import *
from board import Board
from player import Player


def on_mouse_press(x, y, button, modifiers):
    if button == 1:
        if player1.turn == True:
            if player1.board.get_tile_by_pos(x,y) != None:
                tile = player1.board.get_tile_by_pos(x,y)
                #once a player has clicked on a tile if it is a valid move it will 
                #be registered and then the AI will take it's turn
                if tile.is_clickable():
                    if tile.is_hit():
                        tile.type = "hit"
                        player1.guess_count+=1
                        player1.turn = False #give the turn to the AI
                    elif tile.is_empty():
                        tile.type = "miss"
                        player1.turn = False


if __name__ == '__main__':
    player1 = Player("human",Board(10,48,48,"human"))
    player2 = Player("AI",Board(10,648,48,"AI"))
    players = [player1,player2]
    for player in players:
        player.board.load_ships(player.ships)
    # create a pyglet window and set glOptions
    win = window.Window(width=1140, height=580, vsync=True, caption = "BattleShips")
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers
    win.push_handlers(on_mouse_press)
    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for player in players:
            player.board.draw_board()
        win.flip()
        #this controls who's turn it is
        if player1.turn == False:
            if player2.turn_count<100:
                player2.do_move()
                player1.turn = True
                player2.turn_count +=1
