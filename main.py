from random import randint

#generates a board of a variable size as a 2d list
def make_board (size):
    board = []
    for x in range(size):
        board.append([])
        for y in range(size):
            board[x].append('.')       
    return board

#prints the board in its current state
def print_board(board):
    if board == []:
        print ([])
        return
    rows = len(board)
    cols = len(board[0])
    for row in range(0,rows):
        print('\n')
        for col in range(0,cols):
            print("{:^4s}".format(board[row][col]),end = " ")
        print('\n')
    print('-----------------------------------------------')


'''This generates a location for each ship to be placed into'''
def spawn_ship(ship,board,location):
    spawn_location = location
    row = spawn_location[0]
    col = spawn_location[1]
    if is_empty(board,spawn_location):

        ship_location = []
        count = 0
        safety = 0 #to ensure that if a spot comes up that doesnt have a possible solution the game will find a new one
        '''loop until a suitable location has been found, safety included so that it will reset if it can't find a valid move'''
        while len(ship_location)< ship-1 and count <ship-1 and safety<100:      
            for location in range(1,ship):
                if len(ship_location) == ship-1:
                    count +=1
                    break
                #horizontal check right
                if is_empty_row_right(board,row+location,col,ship):                
                    ship_location.append([row+location,col])
                    count +=1                    
                else:
                    ship_location.clear()
                    count = 0
                    break
            for location in range(1,ship):
                if len(ship_location) == ship-1:
                    count +=1
                    break
                #horizontal check left
                if is_empty_row_left(board,row-location,col,ship):
                    ship_location.append([row-location,col])
                    count +=1 
                else:
                    ship_location.clear() 
                    count = 0
                    break
            for location in range(1,ship):
                if len(ship_location) == ship-1:
                    count +=1
                    break
                #vertical check up
                if is_empty_col_up(board,row,col+location,ship):                
                    ship_location.append([row,col+location])
                    count +=1 
                else:
                    ship_location.clear() 
                    count = 0
                    break
            for location in range(1,ship): 
                if len(ship_location) == ship-1:
                    count +=1
                    break
                #vertical check down
                if is_empty_col_down(board,row,col-location,ship):
                    ship_location.append([row,col-location])
                    count +=1 
                else:
                    ship_location.clear() 
                    count = 0
                    break
            safety +=1
        
        if ship_location != []:
            ship_location.insert(0,spawn_location)
            return ship_location
        else:
            return []
                     
#Draw the ship given list of points       
def draw_ship(ship_points,board):
    if ship_points != []:
        for coords in ship_points:        
            row = coords[0]
            col = coords[1]
            board[row][col] = 'O'

#check whether the location as a list is empty, where empty is represented as '.'
def is_empty(board,selection):
    row = selection[0] 
    col = selection[1]
    if board[row][col] == '.':
        return True

'''the following functions check the spaces to all sides of the given location'''
#check the the locations on the right side of the location provided (row, column)
def is_empty_row_right(board,rowValue,colValue,ship):
    row = rowValue
    col = colValue
    if row+ship <= 9 and row+ship>=0:
        if board[row+ship][col] == '.':
            return True
#check the the locations on the left side of the location provided (row, column)
def is_empty_row_left(board,rowValue,colValue,ship):
    row = rowValue
    col = colValue
    if row-ship >= 0 and row-ship <=9:
        if board[row-ship][col] == '.':
            return True
#check the locations above the location provded (row, column)
def is_empty_col_up(board,rowValue,colValue,ship):
    row = rowValue
    col = colValue
    if col+ship <= 9 and col+ship >= 0:
        if board[row][col+ship] == '.':
            return True
#check the locations below the location provided (row, column)
def is_empty_col_down(board,rowValue,colValue,ship):
    row = rowValue
    col = colValue
    if col-ship >= 0 and col-ship<=9:
        if board[row][col-ship] == '.':
            return True

#returns a randomly generated list of coords 
def get_random_coord():
    move_coords = []
    for x in range(0,2):
        move = randint(0,9)
        move_coords.append(move)

    return move_coords

''' loops for the number of ships provided in the call. Stores locations and moves in temporary variables until a valid location and move is found
After a valid move and location have been found, for each ship it updates the board with the new ships'''
def load_board(board,ships):
    for i in range(0,len(ships)):
        move = [] 
        ship_loc = []
        while True:
            while True:
                potential_move = get_random_coord() #temporary value
                if is_empty(board,potential_move): #if you find a sucessful move, break the while loop
                    move = potential_move 
                    break
            if move != []:
                potential_location = spawn_ship(ships[i],board,move)
                if spawn_ship != [] and len(potential_location)>1: # if a suitable location for a ship has been found break the while loop
                    ship_loc = potential_location
                    break
        draw_ship(ship_loc,board)
        



if __name__ == '__main__':
    ship_list = [5,4,3,3,2]
    board = make_board(10)
    load_board(board,ship_list)
    print_board(board)
