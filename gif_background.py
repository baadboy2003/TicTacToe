import tkinter as tk
from PIL import Image, ImageTk

class GIFLabel(tk.Label):
    """
    A custom Tkinter Label widget for displaying and animating GIF images.

    Attributes:
    -----------
    master : tk.Tk or tk.Frame
        The parent widget where the GIFLabel is placed.
    filename : str
        The file path of the GIF to be displayed.
    image : PIL.Image.Image
        The main image object opened from the GIF file.
    frames : list
        A list that holds individual frames of the GIF as PhotoImage objects.
    index : int
        The current frame index in the GIF animation.
    delay : int
        The time delay between frames, in milliseconds.
    """

    def __init__(self, master, filename):
        """
        Initializes the GIFLabel widget, extracts frames from the GIF, and starts the animation.

        Parameters:
        -----------
        master : tk.Tk or tk.Frame
            The parent widget that will contain the GIFLabel.
        filename : str
            The file path of the GIF to be loaded and displayed.
        """
        # Initialize the parent tk.Label class
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
                # Seek to the current frame in the GIF
                self.image.seek(i)
                
                # Copy the current frame to avoid referencing issues
                frame = self.image.copy()
                
                # Convert the frame to a PhotoImage object that Tkinter can handle
                photo = ImageTk.PhotoImage(frame)
                
                # Append the PhotoImage object (frame) to the frames list
                self.frames.append(photo)
        except EOFError:
            # If an EOFError occurs, it means no more frames are available, so ignore it
            pass
        
        # Set the current frame index to the first frame
        self.index = 0
        
        # Set the delay between frames (in milliseconds)
        self.delay = 100
        
        # Start the animation loop by calling the update method
        self.update()

    def update(self):
        """
        Updates the displayed image to the next frame in the animation, looping back to the start
        after the last frame. This method is called recursively with a delay.
        """
        # Get the current frame using the frame index
        frame = self.frames[self.index]
        
        # Update the label's image to the current frame
        self.config(image=frame)
        
        # Move to the next frame
        self.index += 1
        
        # If the index exceeds the number of frames, reset to the first frame
        if self.index == len(self.frames):
            self.index = 0
        
        # Schedule the next frame update after the specified delay (in milliseconds)
        self.after(self.delay, self.update)
