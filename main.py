"""
Code description:
It's n-by-n tic tac toe woking on terminal.
not including reinforment learning
"""

import numpy as np

class GameBoard():
    def __init__(self,scale):
        self.scale = scale
        self.board = np.zeros((self.scale,self.scale),int)
        self.state = True
        self.win_pattern = np.empty(((self.scale*2+2),self.scale,2),int);
        self.winner_type = 0 # 1=> player, 2=> computer, 3=>draw

    def init_win_pattern(self):
        num = self.scale
        for i in range(num):
            self.win_pattern[num*2][i] = [i,i]
            self.win_pattern[num*2+1][i] = [i,(num-1-i)]
            for j in range(num):
                self.win_pattern[i][j] = [i,j] # lines in row
                self.win_pattern[num+i][j] = [j,i] # lines in column

    def continuation_judgement(self):
        piece_type = 0
        for i in self.win_pattern:
            count = 0
            piece_type = 0
            first = True
            check_win = False
            for j in i: 
                piece = self.board[j[0],j[1]]
                if piece == 0:#not placed
                    break

                if first:
                    first = False
                    piece_type = piece #setting which piece's link we are going to count.

                if piece_type == piece:
                    count +=1 #count number of link    
                    if int(count) == int(self.scale):
                        self.state = False
                        self.winner_type = piece_type # 1 => player won, 2=> computer won
                        check_win = True
                        break 
                else: #different type piece is placed
                    break

            if check_win: # break the parent loop
                break;

        if not check_win:
            if np.any(self.board == 0): # any 0(not placed) remain or not.
                self.state = True # Continue the game
            else:
                self.state = False # finish the game
                winner_type = 3
                self.winner_type = winner_type # draw
    

    
    def show_result(self): # who win or draw
        if self.winner_type == 1:
            print("\033[31m" + "!!!!!!-------Player win--------!!!!!!" + "\033[0m")
        elif self.winner_type ==2:
            print("\033[31m" +"!!!!!!-------computer win-------!!!!!!"+ "\033[0m")
        elif self.winner_type ==3:
            print("\033[31m" +"!!!!!!-----------draw-----------!!!!!!"+ "\033[0m")
        else:
            print("\033[31m" +"!!!!!!-------invalid game-------!!!!!!"+ "\033[0m")
        print('\033[1m' + '\033[35m' + "Thank you for playing" + '\033[0m')

    def check_valid_choice(self,place): # True => pass the validation
        # check invalid data types and out of range.
        if type(place[0]) != int or type(place[1]) != int:
            print("\033[32m"+"---This place can not be available---" + "\033[39m")
            print("\033[31m"+ "Please put two numbers like: 1 0, 1 1" + "\033[39m")
            return False
        if place[0] >= self.scale or place[0] < 0:
            print("\033[32m" + "---This place can not be available---" + "\033[39m")
            print("\033[31m"+ "The input row is out of range. Please input within 0 to{}".format(self.scale-1) + "\033[39m")
            return False
        if place[1] >= self.scale or place[1] < 0:
            print("\033[32m" + "---This place can not be available---" + "\033[39m")
            print("\033[31m"+ "The input column is out of range. Please input within 0 to{}".format(self.scale-1) + "\033[39m")
            return False

        #check the place is not placed
        if self.board[place[0],place[1]] == 0:
            return True
        else:
            print("\033[32m" + "---This place can not be available---" + "\033[39m")
            print("\033[31m"+ "An other piece is already placed" + "\033[39m")
            return False
    
    def show_currentboard(self):
        visualizeboard = self.board.astype(str)
        scale = self.scale
        for i in range(scale):
            for j in range(scale):   
                piece = self.board[i,j]
                if piece == 0:
                    visualizeboard[i,j] = "   "
                if piece == 1:
                    visualizeboard[i,j] = " O "
                if piece == 2:
                    visualizeboard[i,j] = " X "
        
        for i in visualizeboard:
            print("|",end='')
            for j in i:
                print("\033[1m"+ j + "\033[0m" ,end='|')
            print("")


    def set_board(self,place,piece_type): # set a new piece
        self.board[place[0],place[1]] = piece_type



class Human():
    def __init__(self):
        self.piece_type = 1 # 1 is player piece

    def piece_choice(self):
        print("\033[33m" + "---------Player's turn---------" + "\033[39m")
        choice = input("\033[36m" + "where do you place your piece: \n O ... your piece,  X... opponent piece \n example of input 0 1 | 1 2 | row column |\n" + "\033[39m").split()
        if(len(choice) == 2):
            choice[0] = int(choice[0])
            choice[1] = int(choice[1])
        return choice


class Computer():
    def __init__(self):
        self.piece_type = 2 # 2 is player piece

    def piece_choice(self): # not implemented, Now it is same as player. 
        print("\033[34m" + "---------Computer's turn---------" + "\033[39m")
        choice = input("\033[36m" + "where do computer(both sides you play) place your piece: \n O ... your piece,  X... opponent piece \n example of input 0 1 | 1 2 | row column |\n" + "\033[39m").split()
        if len(choice) == 2:
            choice[0] = int(choice[0])
            choice[1] = int(choice[1])
        return choice

#------process of game--------
board_scale = int(input("input a board scale for tic tac toe game[3 to within reason]"))
game_board = GameBoard(board_scale)
human = Human()
computer = Computer()

game_board.init_win_pattern()# setting the win situations.

turn = True # True => human's turn, False => computer's turn

"""
game_board.Train()
"""

#human vs computer
while game_board.state: # True => continuation 
    valid_state = False

    if turn:#human turn
        while valid_state == False:
            game_board.show_currentboard();
            choice = human.piece_choice()
            valid_state = game_board.check_valid_choice(choice)
        game_board.set_board(choice, human.piece_type)

    else:#computer turn
        while valid_state == False:
            game_board.show_currentboard();
            choice = computer.piece_choice()
            valid_state = game_board.check_valid_choice(choice)
        game_board.set_board(choice, computer.piece_type)

    game_board.continuation_judgement()
    turn = not turn

game_board.show_currentboard();
game_board.show_result()