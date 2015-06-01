from graphics import egi, KEY
from point2d import Point2D
from pyglet import window, clock
from pyglet.gl import *
from board import Board
from player import Player


def on_mouse_press(x, y, button, modifiers):
    if button == 1:
        if player1.turn == True:
            if player1.board.get_tile_by_pos(x,y) != None:
                tile = player1.board.get_tile_by_pos(x,y)
                if tile.is_clickable():
                    if tile.is_hit():
                        tile.type = "hit"
                        player1.guess_count+=1
                        player1.turn = False
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
    win = window.Window(width=1140, height=580, vsync=True, resizable=True)
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
        if player1.turn == False:
            if player2.turn_count<100:
                player2.do_move()
                player1.turn = True
                player2.turn_count +=1