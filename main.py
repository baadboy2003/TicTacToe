from tkinter import Tk
from ui_home import HomeScreen

def main():
    """
    The main entry point of the application.

    This function initializes the Tkinter root window, sets its properties, 
    and loads the home screen UI. The root window's main event loop is started, 
    which listens for user interactions and updates the UI accordingly.
    """
    # Create the root Tkinter window (main application window)
    root = Tk()
    
    # Make the window resizable both horizontally and vertically
    root.resizable(True, True)
    
    # Initialize the HomeScreen UI and pass the root window as its parent
    HomeScreen(root)
    
    # Start the Tkinter main event loop (keeps the application running)
    root.mainloop()

# If this script is executed directly, call the main function to start the program
if __name__ == "__main__":
    main()
