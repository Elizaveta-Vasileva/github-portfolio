#import the 'random' module to determine which player will go first
#import the tkinter modules for the graphical interface
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

#create a class to group everything related to the tictactoe game
class TicTacToe:
    #the init method will allow us to initialize the board.
    #the board is initially empty. "board" is an attribute of the method.
    #there are initially no players. "players" is an attribute of the method.
    def __init__(self):
        self.board = []
        self.players = {}

    #this method will allow us to create the 3x3 board.
    #each row is initially empty and then added a "-" to represent the number of columns.
    #when the game is being played, a '-' means that no player has chosen this row,column has a space for their symbol.
    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)

    #this method will allow us to randomly determine which player goes first.
    #it will return randomly one of the two players to start the game
    def get_random_first_player(self):
        return random.choice(list(self.players.keys()))

    #this method will allow us to change the '-' to the symbol of the player.
    #this is the method that allows the player to place its move
    #this method will now make sure that a player choses a cell that is empty
    #this method will now make sure that a player adds valid row and column values
    def fix_spot(self, row, col, player):
        while True:
            if 1 <= row <= 3 and 1 <= col <= 3:
                if self.board[row - 1][col - 1] == '-':
                    self.board[row - 1][col - 1] = player
                    break
                else:
                    messagebox.showinfo("Invalid Move", "Spot already occupied. Choose another spot.")
            else:
                messagebox.showinfo("Invalid Move", "Invalid input. Choose row and column numbers within the range of 1 to 3.")

            # Ask the same player for input again until a valid spot is chosen
            row, col = map(int, simpledialog.askstring("Input", f"{self.players[player]}, enter row and column numbers (e.g., 1 2): ").split())

    def is_player_win(self, player):
        win = None
        n = len(self.board)

        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        win = True
        for i in range(n):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win
        return False

    def is_board_filled(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def swap_player_turn(self, player):
        player_list = list(self.players.keys())
        current_index = player_list.index(player)
        next_index = (current_index + 1) % len(player_list)
        return player_list[next_index]

    def show_board(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def get_player_names(self):
        for symbol in ['X', 'O']:
            name = simpledialog.askstring("Input", f"Enter the name for player '{symbol}': ")
            self.players[symbol] = name

    def start(self):
        self.get_player_names()
        self.create_board()

        player = self.get_random_first_player()
        #Tkinter GUI Setup: create the main window of the graphical interface
        root = tk.Tk()
        root.title("Tic Tac Toe")

        label_turn = tk.Label(root, text=f"{self.players[player]}'s turn", font=('normal', 14))
        label_turn.grid(row=0, column=0, columnspan=3)

#Creation of a function on_button_click to handle button clicks and update the board
        def on_button_click(row, col):
            nonlocal player
            if self.board[row][col] == '-':
                self.board[row][col] = player
                button_texts[row][col].set(player)
                if self.is_player_win(player):
                    messagebox.showinfo("Game Over", f"{self.players[player]} wins the game!")
                    root.destroy()
                elif self.is_board_filled():
                    messagebox.showinfo("Game Over", "Match Draw!")
                    root.destroy()
                else:
                    player = self.swap_player_turn(player)
                    label_turn.config(text=f"{self.players[player]}'s turn")

#Creation of a list to store string values that are going to be used during the game.
        button_texts = [[tk.StringVar() for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
              #Creation of the button inside the main window (root).
                button = tk.Button(root, textvariable=button_texts[i][j], font=('normal', 20), width=6, height=2,
                                   command=lambda row=i, col=j: on_button_click(row, col))
                button.grid(row=i + 1, column=j) #Method used to place the button in the specified row and column. +1 for the row to accommodate the label in the first row of the Tkinter grid.

        root.mainloop()

# This is to start the game
tic_tac_toe = TicTacToe()
tic_tac_toe.start()