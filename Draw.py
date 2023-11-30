import tkinter as tk
from tkinter import messagebox

from _cffi_backend import callback


class MoveYourStepProjectApp:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback  # Callback function to handle button click
        master.title("MoveYourStepProject")

        # Define custom fonts
        self.title_font = ("Arial", 16, "bold")
        self.button_font = ("Arial", 12)

        # Create and pack the title label
        self.title_label = tk.Label(master, text="MoveYourStepProject", font=self.title_font)
        self.title_label.pack(pady=10)

        # Create buttons for each level
        for level in range(1, 5):
            button_text = f"{level}. Level {level}"
            level_button = tk.Button(master, text=button_text, command=lambda l=level: self.on_level_click(l), font=self.button_font)
            level_button.pack(pady=5)
        self.selected_level = None  # Initialize selected_level to None

    def on_level_click(self, level):
        messagebox.showinfo("Level Selected", f"You clicked on Level {level}.")
        self.selected_level = level
        self.callback(self.selected_level)

    def returnlevel(self):
        return self.selected_level

    def clear_first_screen(self):
        # Destroy all widgets in the first screen
        for widget in self.master.winfo_children():
            widget.destroy()

class SecondScreen:
    def __init__(self, master, level):
        self.master = master
        self.level = level

        # Define custom fonts
        self.title_font = ("Arial", 16, "bold")
        self.button_font = ("Arial", 12)

        # Create and pack the title label
        self.title_label = tk.Label(master, text=f"Screen for Level {level}", font=self.title_font)
        self.title_label.pack(pady=10)

        # Create buttons for the second screen
        for i in range(1, 6):
            button_text = f"{i}. Input{i}"
            input_button = tk.Button(master, text=button_text, command=lambda num=i: self.on_input_click(num), font=self.button_font)
            input_button.pack(pady=5)

    def on_input_click(self, input_num):
        messagebox.showinfo("Input Clicked", f"You clicked on Input {input_num} for Level {self.level}.")



"""
Cách để call hàm vẽ menu:
root = tk.Tk()
app = MoveYourStepProjectApp(root)
root.mainloop()

"""