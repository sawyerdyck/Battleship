# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:18:01 2024

@author: sawye
"""

import random

#reads file information and handles errors
def read():
    file_path = 'HSBattleship.txt'
    try:
        # Attempt to open the file for reading
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        # Handle the case where the file is not found
        print(f"The file '{file_path}' does not exist.")
    except IOError as e:
        # Handle other I/O errors (e.g., permission issues)
        print(f"An I/O error occurred: {e}")
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")
    return content
#writes to file and handles errors
def write(string_to_output):
    output_file_path = 'HSBattleship.txt'
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write(string_to_output)    
    except FileNotFoundError:
            # Handle the case where the file is not found
        print(f"The file '{output_file_path}' does not exist.")
    except IOError as e:
            # Handle other I/O errors (e.g., permission issues)
        print(f"An I/O error occurred: {e}")
    except Exception as e:
            # Catch any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")
#board class controls printing and creation of boards
class Board:
    def __init__(self, size):
        #size of boardcan be changed to alter game experience
        self.size = size
        #creates empty grid (board size x board size)
        self.grid = [['•' for _ in range(size)] for _ in range(size)]
#displays grid with coordinates to aid firing
    def display(self):
        print ("   1 2 3 4 5 6 7 8 9")
        runs = 0
        for row in self.grid:
            runs += 1
            print(f"{0 + runs}  " + " ".join(row))
#player class controls player commands such as retrieving player guesses and displaying high score info
class Player:
    def __init__(self, board_size):
        self.guess_board = Board(board_size)
        
    # allows user to input their shot location
    def get_user_guess(self):
        while True:
            try:
                row = int(input("Enter guess row (1-9): "))
                if 1 <= row <= 9:
                    col = int(input("Enter guess column (1-9): "))
                    if 1 <= col <= 9:
                        return row, col
                    else:
                        print("Please enter valid coordinates (1-9).")
                else:
                    print("Please enter valid coordinates (1-9).")

            except ValueError:
                print("Invalid input. Please enter integers for row and column.")
    #selection sort advanced algorithm which sorts highscores from file
    def selection_sort(array): 
        length = len(array) 
        # Traverse through all elements in the list 
        for i in range(length): 
            # Find the maximum element in the unsorted part of the list 
            max_index = i 
            for check in range(i + 1, length): 
                if int(array[check]) < int(array[max_index]): 
                    max_index = check 
            # Swap the found maximum element with the first element 
            array[max_index], array[i] = array[i], array[max_index] 
        return array
    #interface
    print()
    print ("""        Welcome to Battleship
     To begin placing your ships, """)
#controls interface at endgame, displays round stats, highscore, winner and allows player to continue playing or exit
    def endGame(self, winner, rounds):
        print()
        print(f"{winner[0]} wins with a score of : {winner[1]}, in {rounds} rounds")
        #reads in file containing highscores, splits file, adds new highscore, sorts, displays all-time highscore
        content = read()
        content += (str(winner[1]))
        csv_list = content.split(',')
        csv_list = Player.selection_sort(csv_list)
        
        string_to_output = ''
        for element in csv_list:
            string_to_output += str(element) + ','
        write(string_to_output)
        content = read()
        csv_list = content.split(',')
        max_num = 0
        for i in csv_list:
            if i == '':
                print()
                print(f"highscore : {max_num}")
                break
            else:
                if int(i) > int(max_num):
                    max_num = i
        playAgain = input("Press 1 to play again, 2 to exit : ")
        print()
        if playAgain == '1':
            return True
        elif playAgain == '2':
            return False
#BattleshipGame class controls initial board setup, game interface, records hits and player scores, and all computer aspects of the program
class BattleshipGame:
    def __init__(self, board_size, num_ships):
        self.board_size = board_size
        self.num_ships = num_ships
        self.player = Player(board_size)
        self.board = Board(board_size)
        self.compBoard = Board(board_size)
        self.play = False
#uses previous display method to print each players board with UI
    def print_board(self):
        print("🎖   Battleship   🎖")
        self.player.guess_board.display()
        print("━━━━━━━━━━━━━━━━━━━━━")
        self.board.display()
#randomly fills the enemy board
    def fillEnemyBoard(self):
        directionC = random.choice(['horizontal', 'vertical'])
        if directionC == 'horizontal':
            rowC = random.randint(0, len(self.compBoard.grid) - 1)
            colC = random.randint(0, len(self.compBoard.grid) - self.board_size)
            for i in range(self.board_size):
                self.compBoard.grid[rowC][colC + i] = 'S'
        else:
            rowC = random.randint(0, len(self.compBoard.grid) - self.board_size)
            colC = random.randint(0, len(self.compBoard.grid) - 1)
            for i in range(self.board_size):
                self.compBoard.grid[rowC + i][colC] = 'S'
#controls player ship deployment, horizontal/vertical ship and ship coordinate
    def place_ship(self, board, size, _):
        while True:
            direction = input("Press v for vertical or h for horizontal: ")
            if direction in ('v', 'h'):
                try:
                    if direction == 'h':
                        row = int(input(f"Enter x coordinate for ship {_+1} drop (1-9): "))
                        if 1 <= row <= 9 :
                            col = int(input(f"Enter y coordinate for ship {_+1} drop (1-9): "))
                            if 1 <= col <= 9 and col + 1 <= 9:
                                for i in range(size):
                                    board.grid[row-1][(col + i)-2] = 'S'
                                self.board.display()
                                return
                            else:
                                print("Invalid input. Coordinates are out of range.")
                        else:
                            print("Invalid input. Coordinates are out of range.")
                    elif direction == 'v':
                        row = int(input(f"Enter x coordinate for ship {_+1} drop (1-9): "))
                        if 2 <= row <= 8:
                            col = int(input(f"Enter y coordinate for ship {_+1} drop (1-9): "))
                            if 1 <= col <= 9:
                                for i in range(size):
                                    board.grid[(row + i)-2][col-1] = 'S'
                                self.board.display()
                                return
                            else:
                                print("Invalid input. Coordinates are out of range.")
                        else:
                            print("Invalid input. Coordinates are out of range.")
                except ValueError:
                    print("Invalid input. Please enter integers for row and column.")
            else:
                print("Invalid input. Please enter v or h")
#controls order of operations for the game to flow correctly, fills boards first, then begins rounds
    def start_game(self):
        self.play = True
        for _ in range(self.num_ships):
            self.fillEnemyBoard()
            self.place_ship(self.board, 3, _)
        
        start = input("Press 1 to start : ")
        print()
        
        if start != '1':
            self.play = False
            return False
        self.print_board()
        return True
#continues rounds until all player ships or all enemy ships are sunk, records pointage, rounds, and game winner
    def play_turn(self):
        player_hits = 0
        comp_hits = 0
        rounds = 0
        winner = ''
        while player_hits < 15 and comp_hits < 15:
            rounds +=1
            player_hits += self.player_turn()
            comp_hits += self.comp_turn()
            Ppoints = 500+(player_hits*100)-(rounds*10)
            Cpoints = 500+(comp_hits*100)-(rounds*10)
            print(f"player: {Ppoints} enemy : {Cpoints}")
            self.print_board()
        self.play = False
        if player_hits == 15:
            winner = "player",Ppoints
        elif comp_hits == 15:
            winner = "computer",Cpoints
        playAgain = Player.endGame(self, winner, rounds)
        return playAgain
#allows user to fire shots at enemy territory, checks for hits/misses
    def player_turn(self):
        while True:
            try:
                guess_row, guess_col = self.player.get_user_guess()
                if self.compBoard.grid[guess_row - 1][guess_col - 1] == 'S':
                    print()
                    print("Hit!")
                    self.player.guess_board.grid[guess_row - 1][guess_col - 1] = 'X'
                    return 1
                else:
                    print()
                    print("Miss!")
                    self.player.guess_board.grid[guess_row - 1][guess_col - 1] = '0'
                    return 0
            except IndexError:
                print("Invalid input. Coordinates are out of range.")
#randomly fires computer shots, checks for hits/misses
    def comp_turn(self):
        comp_row = random.randint(1, 9)
        comp_col = random.randint(1, 9)
        if self.board.grid[comp_row - 1][comp_col - 1] == 'S':
            print()
            print("Enemy Hit!")
            print()
            self.board.grid[comp_row - 1][comp_col - 1] = 'X'
            return 1
        else:
            print()
            print("Enemy Miss!")
            print()
            self.board.grid[comp_row - 1][comp_col - 1] = '0'
            return 0
#keeps game running until manually stopped
playAgain = True
while playAgain == True:
    #creates object of game class
    game = BattleshipGame(9, 5)
    #calls start_game class method to begin playing
    playAgain = game.start_game()
    #after all ships are placed, begins rounds
    while game.play == True:
        playAgain = game.play_turn()

print("Exiting Battleship, Goodbye")
