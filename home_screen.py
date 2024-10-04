import tkinter as tk
from game import TicTacToeGame
from ui import TicTacToeUI
from online_ui import OnlineUI
from PIL import Image, ImageTk
from pygame import mixer


class GIFLabel(tk.Label):
    def __init__(self, master, filename):
        # Initialize the parent Label class
        tk.Label.__init__(self, master)
        
        # Store the filename for future reference
        self.filename = filename
        
        # Open the GIF file using PIL
        self.image = Image.open(filename)
        
        # Initialize an empty list to store the frames
        self.frames = []
        
        try:
            # Extract each frame from the GIF file
            for i in range(self.image.n_frames):
                # Seek to the current frame
                self.image.seek(i)
                
                # Copy the current frame
                frame = self.image.copy()
                
                # Convert the frame to a PhotoImage object
                photo = ImageTk.PhotoImage(frame)
                
                # Append the PhotoImage object to the frames list
                self.frames.append(photo)
        except EOFError:
            # Ignore any EOF errors that occur during frame extraction
            pass
        
        # Initialize the index to the first frame
        self.index = 0
        
        # Set the delay between frames in milliseconds
        self.delay = 100
        
        # Start the animation by calling the update method
        self.update()

    def update(self):
        # Retrieve the current frame from the frames list
        frame = self.frames[self.index]
        
        # Configure the label with the current frame
        self.config(image=frame)
        
        # Increment the index to point to the next frame
        self.index += 1
        
        # If the index reaches the end of the frames list, reset to 0
        if self.index == len(self.frames):
            self.index = 0
        
        # Schedule the next call to update after the specified delay
        self.after(self.delay, self.update)

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
        background_music = r'RobTop - Geometry Dash Menu Theme.mp3'
        mixer.music.load(background_music)
        mixer.music.play(-1) 

        self.root = root
        self.create_home_screen()

        root.geometry("542x602") #width x height of UI
        root.resizable(False, False)

    def create_home_screen(self):
        
        self.root.title("Tic-Tac-Toe: Select Mode")

        gif_label = GIFLabel(self.root, r"arcadegiflol.gif")
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