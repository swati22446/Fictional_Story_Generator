import tkinter as tk
from FictionalStory_AI.gui import StoryGeneratorGUI

def main():
    root = tk.Tk()
    app = StoryGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
