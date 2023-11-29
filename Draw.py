import tkinter as tk
from tkinter import messagebox

class MoveYourStepProjectApp:
    def __init__(self, master):
        self.master = master
        master.title("MoveYourStepProject")

        # Define custom fonts
        self.title_font = ("Arial", 16, "bold")
        self.button_font = ("Arial", 12)

        # Create and pack the title label
        self.title_label = tk.Label(master, text="MoveYourStepProject", font=self.title_font)
        self.title_label.pack(pady=10)

        # Create buttons for each level
        for level in range(1, 4):
            button_text = f"{level}. Level {level}"
            level_button = tk.Button(master, text=button_text, command=lambda l=level: self.on_level_click(l), font=self.button_font)
            level_button.pack(pady=5)

    def on_level_click(self, level):
        messagebox.showinfo("Level Selected", f"You clicked on Level {level}.")
        return level
    
"""
Cách để call hàm vẽ menu:
root = tk.Tk()
app = MoveYourStepProjectApp(root)
root.mainloop()

"""