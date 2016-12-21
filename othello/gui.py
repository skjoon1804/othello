//  Copyright © 2016 Oh Jun Kwon. All rights reserved.

import tkinter
import logic
import point


class Othello:
    def __init__(self):
        self.move_list=[]

    def start(self):
        self.user_input()

        self.scoreboard().grid(row=0, column=0,sticky=tkinter.E+tkinter.W+tkinter.S+tkinter.N)
        self.create_board().grid(row=1, column=0, padx=20, pady=20,sticky=tkinter.E+tkinter.W+tkinter.S+tkinter.N)
        self.winner().grid(row=2, column=0,sticky=tkinter.E+tkinter.W+tkinter.S+tkinter.N)
        
        self._root_window.mainloop()


    def user_input(self):
        self.input = Input()
        self.input.start()

        self._row = self.input.row
        self._column = self.input.column
        self._first = self.input.first
        self._arrange = self.input.arrange
        self._rule = self.input.rule

        self.game = logic.Gameboard(self._row, self._column, self._first,
                                    self._arrange, self._rule)


    def scoreboard(self):
        self._root_window = tkinter.Tk()
        self._bscore = tkinter.IntVar()
        self._wscore = tkinter.IntVar()
        self._first = tkinter.StringVar()
        self._winner = tkinter.StringVar()

        self._wscore.set(self.game._wscore)
        self._bscore.set(self.game._bscore)
        
        self._scoreboard = tkinter.Frame(master = self._root_window)


        self.white_label = tkinter.Label(master=self._scoreboard, text='White:', font=('Arial',20))
        self.white_label.grid(row=0, column=0, padx = 10, pady = 10, sticky=tkinter.W)
        self.white_score = tkinter.Label(master=self._scoreboard, textvariable=self._wscore, font=('Arial',20))
        self.white_score.grid(row=0, column=1, padx = 10, pady = 10, sticky=tkinter.W)

        self.black_label = tkinter.Label(master=self._scoreboard, text='Black:', font=('Arial',20))
        self.black_label.grid(row=0, column=3, padx = 10, pady = 10, sticky=tkinter.W)
        self.black_score = tkinter.Label(master=self._scoreboard, textvariable=self._bscore, font=('Arial',20))
        self.black_score.grid(row=0, column=4, padx = 10, pady = 10, sticky=tkinter.W)

        self.first_label = tkinter.Label(master=self._scoreboard, text='Turn:', font=('Arial',20))
        self.first_label.grid(row=0, column=6, sticky=tkinter.E)
        self.first_status = tkinter.Label(master=self._scoreboard, textvariable=self._first, font=('Arial',20))
        self.first_status.grid(row=0, column=7, sticky=tkinter.E)

        return self._scoreboard


    def winner(self):
        self._winner_display = tkinter.Frame(master=self._root_window)
        self.winner_label = tkinter.Label(master=self._winner_display, text='Winner:', font=('Arial',20))
        self.winner_label.grid(row=0, column=0, padx = 10, pady = 10)
        self.winner_status = tkinter.Label(master=self._winner_display, textvariable=self._winner, font=('Arial Black',20))
        self.winner_status.grid(row=0, column=1, padx = 10, pady = 10)

        return self._winner_display


    def create_board(self):
        self._canvas = tkinter.Canvas(master=self._root_window,width=400, height=400)
        self._root_window.rowconfigure(0, weight=1)
        self._root_window.rowconfigure(1, weight=1)
        self._root_window.rowconfigure(2, weight=1)
        self._root_window.columnconfigure(0, weight=1)
  
        self._canvas.bind('<Configure>', self.resize)
        self._canvas.bind('<Button-1>', self.click)

        return self._canvas


    def draw_board(self):
        self._canvas.delete(tkinter.ALL)     
        self.move_list = []

        self.game.track_score()
        self._wscore.set(self.game._wscore)
        self._bscore.set(self.game._bscore)
        self._first.set(self.game._first)

        for row in range (self.game._rows):
            for column in range (self.game._columns):
                
                top_left = point.from_frac(column/self.game._columns, row/self.game._rows)
                bottom_right = point.from_frac((column+1)/self.game._columns, (row+1)/self.game._rows)
                width = self._canvas.winfo_width()
                height = self._canvas.winfo_height()

                top_left_x,top_left_y = top_left.pixel(width,height)
                bottom_right_x,bottom_right_y = bottom_right.pixel(width,height)

                x1, y1 = top_left.frac()
                x2, y2 = bottom_right.frac()
                self.move_list.append([x1,y1,x2,y2,width,height,row,column])
                
                color = ''
                if self.game.board[row][column] == 'Black':
                    color = 'black'
                elif self.game.board[row][column] == 'White':
                    color = 'white'                              
                self._canvas.create_rectangle(top_left_x,top_left_y,bottom_right_x,bottom_right_y,fill = 'green')
                self._canvas.create_oval(top_left_x,top_left_y,bottom_right_x,bottom_right_y,outline="",fill = color)



        if self.game.end_game():
            self._winner.set(self.game.determine_winner())
    
    
    def click(self, event):

        x = event.x
        y = event.y

        for location in self.move_list:
            if location[0]*location[4]<x<location[2]*location[4] and location[1]*location[5]<y<location[3]*location[5]:
                move = self.game.operate_move(location[6],location[7])
                if move!= 'STOP':
                    self.draw_board()
                
        


    def resize(self, event):
        self.draw_board()






class Input:
    def __init__(self):
        self._root_window = tkinter.Tk()     
        self._input = tkinter.Frame(master = self._root_window)

        self._first = tkinter.StringVar()
        self._arrange = tkinter.StringVar()
        self._rule = tkinter.StringVar()

    def start(self):
        self.setup()
        self._root_window.mainloop()

    def setup(self):
        self.layout().grid(row=0, column=0,
                            sticky=tkinter.E+tkinter.W+tkinter.S+tkinter.N)
        self._root_window.rowconfigure(0, weight=1)
        self._root_window.columnconfigure(0, weight=1)

    def layout(self):
        self.welcome = tkinter.Label(master=self._input,
                                     text = 'Welcome to Othello!',
                                     font=('Calibri',15))
        self.welcome.grid(row=0, column=1)
        self.number_setup().grid(row=1, column=0)
        self.string_setup().grid(row=1, column=2)
        
        self.button = tkinter.Button(master = self._input, text='Start',
                                     font=('Arial',20), command=self.run)
        self.button.grid(column=1)

        self._input.rowconfigure(0, weight=1)
        self._input.rowconfigure(1, weight=1)
        self._input.rowconfigure(2, weight=1)
        self._input.columnconfigure(0, weight=1)
        self._input.columnconfigure(1, weight=1)
        self._input.columnconfigure(2, weight=1)  

        return self._input

    def number_setup(self):
        self._numbers = tkinter.Frame(master=self._input)

        self._row_label=tkinter.Label(master=self._numbers, text = 'Rows:')
        self._row_label.grid(row=1, column=0)
        self._row_spinbox = tkinter.Spinbox(master=self._numbers,
                            increment=2, from_=4, to=16)
        self._row_spinbox.grid(row=1, column=1)

        self._column_label=tkinter.Label(master=self._numbers, text='Columns:')
        self._column_label.grid(row=4, column=0)
        self._column_spinbox=tkinter.Spinbox(master=self._numbers,
                            increment=2, from_=4, to=16)
        self._column_spinbox.grid(row=4, column=1)

        return self._numbers

    def string_setup(self):
        self._string = tkinter.Frame(master = self._input)

        self._first_label = tkinter.Label(master = self._string,text = 'First player')
        self._first_label.grid(row=0, column=0)
        self._first_black = tkinter.Radiobutton(master=self._string,
            text='Black', value='Black', variable=self._first).grid(row=0,column=1)
        self._first_white = tkinter.Radiobutton(master=self._string,
            text='White', value='White', variable=self._first).grid(row=1,column=1)


        self._arrange_label = tkinter.Label(master=self._string,text='Upper left player')
        self._arrange_label.grid(row=3, column=0)
        self._arrange_black=tkinter.Radiobutton(master=self._string,
            text='Black', value='Black', variable=self._arrange).grid(row=3,column=1)
        self._arrange_white=tkinter.Radiobutton(master=self._string,
            text='White', value='White', variable=self._arrange).grid(row=4,column=1)


        self._rule_label = tkinter.Label(master=self._string,text='Most win or \nFewest win?')
        self._rule_label.grid(row=6, column=0)
        self._rule_most = tkinter.Radiobutton(master=self._string,
            text='Most', value='Most', variable=self._rule).grid(row=6,column=1)
        self._rule_least = tkinter.Radiobutton(master=self._string,
            text='Least', value='Least', variable=self._rule).grid(row=7,column=1)

        return self._string


    def run(self):
               
        self.row = int(self._row_spinbox.get())
        self.column = int(self._column_spinbox.get())
        self.first = self._first.get()
        self.arrange = self._arrange.get()
        self.rule = self._rule.get()

        if 4<= self.row <=16 and self.row%2==0 and 4<= self.column<=16 and self.column%2==0 and self.first!=''and self.arrange!='' and self.rule!='':
            self._root_window.destroy()
        
        

    def ourNames():
        return ((27062056, "Oh Jun Kwon"))
        


if __name__=='__main__':
    game = Othello()
    game.start()


  
