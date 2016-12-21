//  Copyright © 2016 Oh Jun Kwon. All rights reserved.

class Gameboard:
    def __init__(self, _rows, _columns, _first, _arrange, _rule):
        self._rows = _rows
        self._columns = _columns
        self._first = _first
        self._arrange = _arrange
        self._rule = _rule
        self._urows = _rows-1
        self._ucolumns = _columns-1
        
        self.board = self.start_board()

        self._bscore=0
        self._wscore=0


    def start_board(self):
        '''set up board according to user input of rows, columns, and top left corner'''
        board = []
        for row in range(self._rows):
            board.append([])
            for column in range(self._columns):
                board[-1].append(' ')
                
        board[int(self._rows/2)-1][int(self._columns/2)-1] = self._arrange
        board[int(self._rows/2)-1][int(self._columns/2)] = self.change_player(self._arrange)
        board[int(self._rows/2)][int(self._columns/2)] = self._arrange
        board[int(self._rows/2)][int(self._columns/2)-1] = self.change_player(self._arrange)

        return board

    def change_player(self, player):
        '''switch active player'''
        if player=='Black':
            return 'White'
        elif player=='White':
            return 'Black'


    def display_board(self):
        '''show current board status for user'''
        self.track_score()  
        board=''
        for column in range(self._rows):
            for row in range(self._cols):
                if self.board[column][row] == ' ':
                    board += '.'
                elif self.board[column][row] == 'Black':
                    board += 'Black'
                elif self.board[column][row] == 'White':
                    board += 'White'
            board += '\n'


        return board


    def track_score(self):
        '''keep track of the scores according to the number of pieces on the board'''
        black = 0
        white = 0
        for row in range(self._rows):
            for col in range(self._columns):
                if self.board[row][col]=='Black':
                    black+=1
                elif self.board[row][col]=='White':
                    white+=1

        self._bscore = black
        self._wscore = white
        
        return (black, white)

    def determine_winner(self):
        '''determine the winner according to the number of pieces'''
        black, white = self.track_score()
        winner =''
        if self._rule == 'Most':
            if black > white:
                winner="Black"
            elif black < white:
                winner= "White"
            else:
                winner= "NONE"
        elif self._rule == "Least":
            if black <white:
                winner= 'Black'
            elif black > white:
                winner= 'White'
            else:
                winner= 'NONE'
        return winner

            
    def change_first(self):
        '''change the player's turn'''
        if "Black" == self._first:
            self._first = "White"
        elif "White" == self._first:
            self._first = "Black"


    def operate_move(self, row, column):
        '''carry out the move on the board'''
        if (not self.open_space(row,column) or
            not self.existing_adjacent(row,column) or
            self.check_all_directions(row,column)==[]):

            return 'STOP'
        
        try:
            self.disc_flip(row, column)
            self.board[row][column] = self._first
            self.change_first()
        except:
            pass



    def disc_flip(self, row, column):       
        '''flip available discs according to the move'''
        flip_list = []
        for direction in self.check_all_directions(row, column):
            
            try:            
                if self.recursive_check(row,column,direction)[-1] == "FLIP":
                    flip_list.append("FLIP")
                    element = self.recursive_check(row, column, direction)[:-1]
                    for i in range(len(element)):
                        element1 = element[i]
                        self.board[element1[0]][element1[1]] = self._first
            except:
                pass

        if any(s in "FLIP" for s in flip_list):
            return  self.board
        else:
            raise Error()

            



    def check_all_directions(self, row, column):
        '''check all directions and see which direction is available to make move'''
        check_list = []
        for row1, column1 in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
            check_row = row+row1
            check_column = column+column1
            
            if 0 <= check_row <= self._urows and 0 <= check_column <= self._ucolumns :
                if self.change_player(self._first) == self.board[check_row][check_column]:
                    direction = row1, column1
                    check_list.append(direction)
        return check_list



    def recursive_check(self,row,column,direction):
        '''loop through all the index in the given location and direction for valid response'''
        recursive_list=[]
        row1, column1 = direction
        check_row = row+row1
        check_column = column+column1

        if 0 <= check_row <= self._urows and 0 <= check_column <= self._ucolumns :

            if self._first == self.board[check_row][check_column]:
                recursive_list.append("FLIP")
                
                return recursive_list

            
            if self.change_player(self._first) == self.board[check_row][check_column]:
                x = check_row, check_column
                recursive_list.append(x)     
                recursive_list += self.recursive_check(check_row, check_column, direction)
                return recursive_list

            else:
                return recursive_list


    def end_game(self):
        '''check if the game is over and check on the opposite turn'''

        check_one = self.check_all_spaces()
        self._first = self.change_player(self._first)
        
        check_two = self.check_all_spaces()
        self._first = self.change_player(self._first)

        
        if not check_one and not check_two :
            return True
        else:
            return False


            

    def check_all_spaces(self):
        '''check for valid moves on all spaces'''
        for row in range(self._rows):
            for column in range(self._columns):
                if self.different_cases(row,column):
                    return True

        return False

    
    def different_cases(self,row,column):
        '''check for valid move in various cases'''
        if (not self.open_space(row,column) or
            not self.existing_adjacent(row,column) or
            self.check_all_directions(row,column)==[]):

            return False
        else:
            return True

        
    def open_space(self,row,column):
        '''check if there is any open spaces'''
        if self.board[row][column] ==' ':
            return True
        else:
            return False


    def existing_adjacent(self,row,column):
        '''check the surrounding space of the chosen space'''
        counter = 0

        for row1, column1 in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
            nrow, ncolumn = row+row1, column+column1
            try:
                if nrow < 0 or ncolumn < 0 :
                    counter+=0
                space = self.board[nrow][ncolumn]
                if space == self.change_player(self._first):
                    counter+=1
                else:
                    counter+=0
            except:
                counter+=0
                
        if counter==0:
            return False
        else:
            return True

 

