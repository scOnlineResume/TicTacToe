from random import randint
import os

class Game():
    def __init__(self,choice):
        self.board = "012345678"
        self.playing = True
        self.player = Player(self)
        self.AI = AI_complicated(self) 
        self.turn_counter = choice
        self.game_end = False

    def replace_string(self,board, input_index,required_character):
        new_string = board[:input_index] + required_character + board[(input_index+1):]
        return new_string

    def get_state(self):
        return self.board

    def draw_board(self,input_string):
        print(f"{input_string[0]} | {input_string[1]} | {input_string[2]}")
        print("-   -   -")
        print(f"{input_string[3]} | {input_string[4]} | {input_string[5]}")
        print("-   -   -")
        print(f"{input_string[6]} | {input_string[7]} | {input_string[8]}")

    def show_available_moves(self,input_string):
        available_moves = []
        for kk in range(len(input_string)):
            if (input_string[kk] == "X") == False and (input_string[kk] == "O") == False:
                available_moves.append(kk)
        return available_moves



    def count_x_o(self,input_string):
        x_o_count = 0
        for character in input_string:
            if (character == "X" or character == "O"):
                x_o_count = x_o_count + 1
        return x_o_count

    def check_win(self,input_string,required_character):
        # Check horizontal
        for ii in range(3):
            if (input_string[3*ii] == input_string[3*ii+1] and input_string[3*ii+1] == input_string[3*ii+2]):
                if input_string[3*ii] == required_character:
                    return True
        # Check vertical
        for ii in range(3):
            if (input_string[ii] == input_string[ii+3] and input_string[ii+3] == input_string[ii+6]):
                if input_string[ii] == required_character:
                    return True
        # Check diagonal
        if (input_string[0] == input_string[4] and input_string[4] == input_string[8]):
            if input_string[0] == required_character:
                return True
        if (input_string[2] == input_string[4] and input_string[4] == input_string[6]):
            if input_string[2] == required_character:
                return True
        return False

    def handlePlayer(self):
        if (self.turn_counter%2 == 0):
            return
        take_input = True
        os.system("cls")
        if (self.count_x_o(self.board) == 9):
            take_input = False
        self.draw_board(self.board)
        if take_input == True:
            input_value = self.player.take_input(self.board)
            self.board = self.replace_string(self.board,input_value,"X")
            self.draw_board(self.board)
            if self.check_win(self.board,"X"):
                self.playing = False
            if self.playing:
                self.turn_counter = (self.turn_counter + 1)%2
        else:
            self.playing = False
        os.system("cls")

    def handleAI(self):
        if self.turn_counter%2 == 1:
            return
        if (self.count_x_o(self.board) < 9):
            self.draw_board(self.board)
            computer_move = self.AI.calculate_input(self.board)
            self.board = self.replace_string(self.board,computer_move,"O")
            if self.check_win(self.board,"O"):
                self.playing = False
            if self.playing:
                self.turn_counter = (self.turn_counter + 1)%2

    def update(self):
        if self.playing:
            self.handlePlayer()
        if self.playing:
            self.handleAI()
        if self.playing == False and self.game_end == False:
            self.game_end = True
            os.system("cls")
            self.draw_board(self.board)
            if self.check_win(self.board,"X"):
                print("Player wins")
                exit(1)
            elif self.check_win(self.board,"O"):
                print("AI wins")
                exit(1)
            else:
                print("Draw")
                exit(1)
            


class Player():
    def __init__(self,game):
        self.game = game

    def take_input(self,input_string):
        input_works = False
        player_input = -1
        while (input_works == False):
            try:
                player_input = int(input("Enter position: "))
            except:
                print("Please enter a number between 1 and 9")
                continue
            if (player_input >= 0 and player_input <= 8):
                if ((input_string[player_input] == "X") == False and (input_string[player_input] == "O") == False):
                    input_works = True            
        return player_input



class AI_complicated():
    def __init__(self,game):
        self.game = game
    def calculate_input(self,input_string):
        current_game_state = self.game.get_state()
        # Select the middle position if board empty
        if self.game.count_x_o(current_game_state) == 0:
            return 4
        # Start the tree data structure, and use the "min max" algorithm to calculate best move
        root_circle = DecisionCircle(self.game,current_game_state,"computer")
        computer_input = root_circle.calculate_best_move()
        return computer_input


class DecisionCircle():
    def __init__(self,game,state_string,current_player_string, parent = None):
        # Handle to the game
        self.game = game
        # Keeps track of whether current player "computer" or "human"
        self.current_player = current_player_string
        # State string keeps track of the board's state
        self.state_string = state_string
        # Show the next possible moves
        self.next_available_moves = self.game.show_available_moves(self.state_string)
        # The value keeps track of whether "X" win or "O" win or draw
        self.value = None
        self.next_circles = []
        self.start_next_circles()
        self.calculate_value()

    def start_next_circles(self):
        for ii in range(len(self.game.board)): 
            if ii in self.next_available_moves:
                # Start the child tree members
                required_character = "X" if self.current_player == "human" else "O"
                next_state_string = self.game.replace_string(self.state_string,ii,required_character)
                next_player = "human" if self.current_player == "computer" else "computer"
                new_circle = DecisionCircle(self.game,next_state_string,next_player,self)
                self.next_circles.append(new_circle)
            else:
                # Append "None" to the next_circles array
                self.next_circles.append(None)
    
    def calculate_value(self):
        # Check the current state, then:
        # - If "X" wins, return 1
        # - If "O" wins, return -1
        # - If draw, return 0

        x_win = self.game.check_win(self.state_string,"X")
        o_win = self.game.check_win(self.state_string,"O")
        state_board_full = True if self.game.count_x_o(self.state_string) == len(self.state_string) else False
        # Check for X win, or O win or draw
        if x_win:
            self.value =  1
            return
        elif o_win:
            self.value = -1
            return
        elif state_board_full:
            self.value =  0
            return
        

        


        # If no winner and the board's not filled, then calculate the value for each of the "next_circles"

        for next_circle in self.next_circles:
            if next_circle is not None:
                next_circle.calculate_value()        
        # Set self.value based on the values of the "child" values and the current player
        next_circle_values = []
        for ii in range(len(self.next_circles)):
            if self.next_circles[ii]  is None:
                next_circle_values.append(None)
            else:
                next_circle_values.append(self.next_circles[ii].value)               
        self.value = calculate_maximum(next_circle_values) if self.current_player == "human" else calculate_minimum(next_circle_values)
        return

    def calculate_best_move(self):
        # Return the index which would calculate the best value
        # For each move in available moves, calculate which index has minimum score
        self.next_available_moves = self.game.show_available_moves(self.state_string)
        appropriate_index = 0
        appropriate_value = 1
        for ii in range(len(self.next_circles)):
            if self.next_circles[ii] is not None:
                next_circle_value = self.next_circles[ii].value
                if next_circle_value < appropriate_value:
                    appropriate_value = next_circle_value
                    appropriate_index = ii
        return appropriate_index


# Function to calculate the maximum when some values are of type "None"
def calculate_maximum(input_array):
    appropriate_values = []
    for value in input_array:
        if value is not None:
            appropriate_values.append(value)
    return max(appropriate_values)

# Function to calculate the minimum when some values are of type "None"
def calculate_minimum(input_array):
    appropriate_values = []
    for value in input_array:
        if value is not None:
            appropriate_values.append(value)
    return min(appropriate_values)



def main():
    choice_valid = False
    while choice_valid == False:
        try:
            choice = int(input("Enter (1) to play as player 1 or (2) to play as player 2: "))
        except:
            print("Please enter (1) or (2)")
            continue

        if (choice < 1 or choice > 2):
            print("Please enter (1) or (2)")
        else:
            choice_valid = True
    tic_tac_toe = Game(choice)
    while True:
        tic_tac_toe.update()

main()