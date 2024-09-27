import tkinter as tk
import socket
import threading

import pygame

from tkinter import Tk
from tkinter import messagebox

from pygame import mixer
from PIL import Image, ImageTk

# from game import TicTacToeGame
# from ui import TicTacToeUI
# from online_ui import OnlineUI
# from home_screen import HomeScreen

PORT = 1000       #port for the server 
SERVER = socket.gethostbyname(socket.gethostname()) # basiclly gets the ip of the local laptop 
ADDR = (SERVER, PORT) # combines server and port   
FORMAT = 'utf-8'      
HEADER = 64
DISCONNECT_MESSAGE = "D"  # message for disconnetion sent to the server 
GAME_OVER_MESSAGE = "GAME_OVER" # message when the game is over 

class TicTacToeGame:
    def __init__(self, ai_enabled=False):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.ai_enabled = ai_enabled
        self.game_over = False  # Attribute to track if the game is over

    def check_winner(self, mark):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] == mark:
                return True
        return False

    def board_full(self):
        return " " not in self.board

    def minimax(self, board, depth, is_maximizing, max_depth=3):
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if self.board_full() or depth == max_depth:  # Stop at a certain depth
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False, max_depth)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True, max_depth)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False, max_depth=3)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def make_move(self, idx):
        if self.board[idx] == " ":
            self.board[idx] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        print("switched to player: ", self.current_player)

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.game_over = False  # Reset game over state
        print("Reset to player: ", self.current_player)


class TicTacToeUI:
    def __init__(self, root, game, home_screen):
        self.root = root
        self.game = game
        self.home_screen = home_screen
        self.buttons = []
        self.create_board()
        self.create_controls()

        root.geometry("542x557") #width x height of UI
        root.resizable(False, False)

    def update_board(self):
        print(self.game.board)
        for i, button in enumerate(self.buttons):
            button.config(text=self.game.board[i])

    def player_move(self, idx):
        mixer.init()
        sound2 = r'ButtonPlate Click (Minecraft Sound) - Sound Effect for editing.mp3'
        sound2_channel = mixer.Channel(1)  # Create a new channel for the second sound
        sound2_channel.play(mixer.Sound(sound2))
            
        if self.game.game_over:  # Check if the game is over
            return

        if self.game.make_move(idx):
            self.update_board()
            print("1")
            if self.game.check_winner(self.game.current_player):
                messagebox.showinfo("Tic-Tac-Toe", f"{self.game.current_player} wins!")
                self.game.game_over = True  # Set game as over
                self.reset_board()  # Reset the board after showing the messagebox
            elif self.game.board_full():
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.game.game_over = True  # Set game as over
                self.reset_board()  # Reset the board after showing the messagebox
            else:
                self.game.switch_player()
                print("1 33")
                if self.game.ai_enabled and self.game.current_player == "O":
                    best_move = self.game.ai_move()
                    if best_move is not None:
                        self.game.make_move(best_move)
                        self.update_board()
                        print("2")
                        if self.game.check_winner("O"):
                            messagebox.showinfo("Tic-Tac-Toe", "AI wins!")
                            self.game.game_over = True  # Set game as over
                            self.restart_game()  # Reset the board after showing the messagebox
                            return
                        elif self.game.board_full():
                            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                            self.game.game_over = True  # Set game as over
                            self.restart_game()  # Reset the board after showing the messagebox
                            return
                    self.game.switch_player()
                    print("1 34")
                    
    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text=" ", font=("Arial", 24), width=9, height=4,
                               command=lambda i=i: self.player_move(i), fg="white", bg= "silver")  
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def create_controls(self):
        mixer.init()
        sound2 = r'ButtonPlate Click (Minecraft Sound) - Sound Effect for editing.mp3'
        sound2_channel = mixer.Channel(1)  # Create a new channel for the second sound
        sound2_channel.play(mixer.Sound(sound2))

        restart_button = tk.Button(self.root, text="Restart", font=("tahoma", 16),
                                   command=self.restart_game, fg="white", bg= "gray")
        restart_button.grid(row=3, column=0, columnspan=2, sticky="ew") 

        back_button = tk.Button(self.root, text="Back to Home", font=("tahoma", 16),
                                command=self.go_back_home, fg="white", bg= "gray")
        back_button.grid(row=3, column=2, columnspan=2, sticky="ew")

    def restart_game(self):
        self.game.reset_game()
        self.update_board()
        print("3")

    def go_back_home(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.home_screen.create_home_screen()
    
    def reset_board(self):
        self.game.reset_game()
        self.update_board()
        print("4")


class OnlineUI:
    def __init__(self, root, home_screen):
        self.root = root
        self.home_screen = home_screen
        self.client = None
        self.player = None
        self.turn = False
        self.game_in_progress = True
        self.buttons = []
        self.create_ui()

        root.geometry("542x602") #width x height of UI
        root.resizable(False, False)

    def create_ui(self):
        mixer.init()
        sound2 = r'ButtonPlate Click (Minecraft Sound) - Sound Effect for editing.mp3'
        sound2_channel = mixer.Channel(1)  # Create a new channel for the second sound
        sound2_channel.play(mixer.Sound(sound2))  # Play the second sound on the new channel

        self.page1 = tk.Frame(self.root)
        self.page2 = tk.Frame(self.root)
        self.page1.pack(fill="both", expand=True)
        self.page2.pack(fill="both", expand=True)
        
        # Create UI

        connect_button = tk.Button(self.page1, text="Connect", font=("tahoma", 16), 
                                   command=self.connect_button, fg="white", bg= "gray")
        connect_button.grid(row=3, column=0, sticky="ew")

        disconnect_button = tk.Button(self.page1, text="Disconnect", font=("tahoma", 16),
                                       command=self.send_disconnect_message, fg="white", bg= "gray")
        disconnect_button.grid(row=3, column=1, sticky="ew")

        back_button = tk.Button(self.page1, text="Back to Home", font=("tahoma", 16), 
                                command=self.go_back_home, fg="white", bg= "gray")
        back_button.grid(row=3, column=2, sticky="ew")

        restart_button = tk.Button(self.page1, text="Restart", font=("tahoma", 16),
                                   command=self.restart_game, fg="white", bg= "gray")
        restart_button.grid(row=4, column=0, columnspan=3, sticky="ew")

        self.create_board()

    def restart_game(self):
            self.reset_board
            self.update_board
            print("Restarting")

    def create_board(self):
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.page1, text="", font=("Arial", 24), width=9, height=4,
                                   command=lambda i=i, j=j: self.send_coordinate(i, j), fg="white", bg= "silver") # this is what sends the corrdinates 
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def connect_button(self):
        if self.client is not None and self.client.fileno() != -1:
            print("Already connected")
            return
        
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                self.player = self.client.recv(msg_length).decode(FORMAT)
                print(f"Connected as player {self.player}")
                if self.player == 'X':
                    self.turn = True
            self.show_frame(self.page2)
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_disconnect_message(self):
        if self.client is None or self.client.fileno() == -1:
            print("No active connection to disconnect")
            return

        try:
            msg = DISCONNECT_MESSAGE
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
            self.client.close()
            self.client = None
            print("Disconnected from server")
            self.go_back_home()
        except Exception as e:
            print(f"Error during disconnection: {e}")

    def send_coordinate(self, row, col): # this sends the row and cloumn that are selected to server 
        mixer.init()
        sound2 = r'ButtonPlate Click (Minecraft Sound) - Sound Effect for editing.mp3'
        sound2_channel = mixer.Channel(1)  # Create a new channel for the second sound
        sound2_channel.play(mixer.Sound(sound2))
            
        if not self.turn or not self.game_in_progress:
            print("Not your turn or game over!")
            return
        msg = f"{self.player}:{row}:{col}"
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        self.turn = False

    def receive_messages(self):
        while True:
            try:
                msg_length = self.client.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.client.recv(msg_length).decode(FORMAT)
                    print(f"Received from server: {msg}")
                    
                    if msg.startswith("MOVE"):
                        _, p, row, col = msg.split(':')
                        self.update_board(int(row), int(col), p)
                        if p != self.player:
                            self.turn = True
                    elif msg.startswith("WINNER"):
                        _, winner = msg.split(':')
                        print(f"{winner} wins!")
                        self.game_over(f"Player {winner} wins!")
                    elif msg == "DRAW":
                        print("It's a draw!")
                        self.game_over("It's a draw!")
                    elif msg == "RESET_BOARD":
                        self.reset_board()
                    elif msg == GAME_OVER_MESSAGE:
                        print("Game over, returning to home.")
                        self.game_over("Game Over!")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state='normal')
        self.game_in_progress = True
        self.turn = (self.player == 'X')

    def game_over(self, message):
        self.game_in_progress = False
        self.display_winner_message(message)

    def display_winner_message(self, message):
        popup = tk.Toplevel()
        popup.title("Game Over")
        label = tk.Label(popup, text=message, font=("Arial", 14))
        label.pack(side="top", fill="x", pady=10)
        ok_button = tk.Button(popup, text="OK", command=lambda: (popup.destroy(), self.reset_board()))
        ok_button.pack(pady=5)

    def update_board(self, row, col, player_mark):
        self.buttons[row][col].config(text=player_mark, state='disabled')

    def show_frame(self, frame):      #this basically updates the frames 
        frame.tkraise()

    def go_back_home(self):           # to show go back to the home page ,it is bascailly done by destroying this page and then adding a new page 
        for widget in self.root.winfo_children():
            widget.destroy()
        self.home_screen.create_home_screen()
        self.show_frame(self.home_screen.page1)


class GIFLabel(tk.Label):
    def __init__(self, master, filename):
        tk.Label.__init__(self, master)
        self.filename = filename
        self.image = Image.open(filename)
        self.frames = []
        try:
            for i in range(self.image.n_frames):
                self.image.seek(i)
                frame = self.image.copy()
                photo = ImageTk.PhotoImage(frame)
                self.frames.append(photo)
        except EOFError:
            pass
        self.index = 0
        self.delay = 100 # milliseconds
        self.update()

    def update(self):
        frame = self.frames[self.index]
        self.config(image=frame)
        self.index += 1
        if self.index == len(self.frames):
            self.index = 0
        self.after(self.delay, self.update)

class HomeScreen:
    def __init__(self, root):
        
        mixer.init()
        background_music = r'C:\Users\Riz\Desktop\INF1002\PythonLOL\MyCodes\RobTop - Geometry Dash Menu Theme.mp3'
        mixer.music.load(background_music)
        mixer.music.play(-1) 

        self.root = root
        self.create_home_screen()

        root.geometry("542x602") #width x height of UI
        root.resizable(False, False)

    def create_home_screen(self):
        
        self.root.title("Tic-Tac-Toe: Select Mode")

        gif_label = GIFLabel(self.root, r"C:\Users\Riz\INF_Grp7\arcadegiflol.gif")
        gif_label.pack(fill="both", expand=True)
        gif_label.place(relx=0, rely=0, relwidth=1, relheight=1)  # Position the background label behind

        label = tk.Label(self.root, text="Tic-Tac-Toe", font=("Comic Sans MS", 40, "bold"), fg ="white", bg="#2f0064", 
                         highlightthickness=2, highlightcolor="#666")
        label.pack(pady=50)
        
        single_button = tk.Button(self.root, text="Single Player", font=("tahoma", 20, "bold"),
                                  command=self.start_single_player, fg="white", bg="#633597")
        single_button.pack(pady=10)

        multi_button = tk.Button(self.root, text="Multiplayer", font=("tahoma", 20, "bold"),
                                 command=self.start_multiplayer, fg="white", bg="#633597")
        multi_button.pack(pady=10)

        # New button for Multiplayer Online
        online_multi_button = tk.Button(self.root, text="Multiplayer Online", font=("tahoma", 20, "bold"),
                                        command=self.start_multiplayer_online, fg="white", bg="#633597")
        online_multi_button.pack(pady=10)

    def start_single_player(self):
        self.clear_screen()
        self.start_game(mode="single")

    def start_multiplayer(self):
        self.clear_screen()
        self.start_game(mode="multi")

    def start_multiplayer_online(self):
        self.clear_screen()
        OnlineUI(self.root, self)  # Create and show the OnlineUI same as ui but for online 

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self, mode):
        if mode == "single":
            game = TicTacToeGame(ai_enabled=True)
        elif mode in ["multi"]:  
            game = TicTacToeGame(ai_enabled=False)

        TicTacToeUI(self.root, game, self)


def main():
    root = Tk()
    HomeScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
