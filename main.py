from tkinter import Tk
from home_screen import HomeScreen

def main():
    root = Tk()
    root.resizable(True, True)  # Make the window resizeable
    HomeScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
