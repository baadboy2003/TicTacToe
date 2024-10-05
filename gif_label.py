import tkinter as tk
from PIL import Image, ImageTk

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
        frame = self.frames[self.index]
        self.config(image=frame)
        self.index += 1
        if self.index == len(self.frames):
            self.index = 0
        self.after(self.delay, self.update)
