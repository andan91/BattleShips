from graphics import egi, KEY
from point2d import Point2D
from pyglet import window, clock, text
from pyglet.gl import *
from board import Board
from player import Player

#handles all mouse clicks
def on_mouse_press(x, y, button, modifiers):
    if button == 1:
        if player1.turn == True and player1.board.is_board_empty() == False:
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

#handles all keyboard button inputs
def on_key_press(symbol,modifiers):
    #if they press R, reload all the ships on the board for another game
    if symbol == KEY.R:
        for player in players:
            if player.board.is_board_empty():
                for tile in player.board.tiles:
                    tile.color = "BLUE"
                player.board.load_ships(player.ships)



if __name__ == '__main__':
    player1 = Player("human",Board(10,48,48,"human"))
    player2 = Player("AI",Board(10,648,48,"AI"))
    players = [player1,player2]
    for player in players:
        player.board.load_ships(player.ships)
    # create a pyglet window and set glOptions
    win = window.Window(width=1400, height=680, vsync=True, caption = "BattleShips") #1140
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_key_press)
    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for player in players:
            player.board.draw_board()
            player.board.update_enemy_ships()
        win.flip()
        #this controls who's turn it is
        if player1.turn == False:
            if player2.turn_count<100:
                player2.do_move()
                player1.turn = True
                player2.turn_count +=1            
        #checks the players to see if anyone has won yet
        for player in players:
            if player.board.win_condition():
                #if a player has won then reset the boards of both players 
                for player in players:
                    player.board.reset_board()
                    #sets the turns of each player back to 0
                    player.turn_count = 0

