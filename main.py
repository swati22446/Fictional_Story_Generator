import tkinter as tk
from gui import StoryGeneratorGUI

def main():
    root = tk.Tk()
    app = StoryGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()