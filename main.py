from tkinter import Tk
from ui_home import HomeScreen

def main():
    root = Tk()
    root.resizable(True, True)  # Make the window resizeable
    HomeScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
