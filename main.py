from World import World
from Draw import MoveYourStepProjectApp, SecondScreen
import tkinter as tk
from tkinter import messagebox

if __name__ == "__main__":
    def handle_level_selection(selected_level):
        if selected_level == 1:
            app.clear_first_screen()
            second_screen = SecondScreen(root, selected_level)

    root = tk.Tk()
    app = MoveYourStepProjectApp(root, handle_level_selection)
    root.mainloop()


