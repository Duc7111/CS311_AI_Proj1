import tkinter as tk
from tkinter import messagebox

from _cffi_backend import callback

def convert(board):
    converted_board = [[0 if cell == '0' else cell for cell in row] for row in board]
    return converted_board

class AlgorithmScreen:
    def __init__(self, master, level, input_file, callback):
        self.master = master
        self.level = level
        self.input_file = input_file
        self.callback = callback  # Callback function to handle algorithm selection
        # Define custom fonts
        self.title_font = ("Arial", 16, "bold")
        self.button_font = ("Arial", 12)

        # Create and pack the title label
        self.title_label = tk.Label(master, text=f"Algorithm Selection for Level {level} - Input {input_file}",
                                    font=self.title_font)
        self.title_label.pack(pady=10)

        # Create buttons for algorithm selection
        algorithms = ["BFS", "UCS", "A*"]
        for algorithm in algorithms:
            algorithm_button = tk.Button(master, text=algorithm, command=lambda alg=algorithm: self.on_algorithm_click(alg),
                                         font=self.button_font)
            algorithm_button.pack(pady=5)

    def on_algorithm_click(self, algorithm):
        messagebox.showinfo("Algorithm Selected", f"You selected {algorithm} for Level {self.level} - Input {self.input_file}.")
        self.callback(self.level, self.input_file, algorithm)

    def update_board(self, world, current_pos):
        self.clearscreen()
        floor_index_to_access = 0
        floor_array = world.get_floor_array(floor_index_to_access)
        value = convert(floor_array)
        cell_size = (200 - len(floor_array) - len(floor_array[0])) / 6
        if value[current_pos[1]][current_pos[2]] != 'T1':
            value[current_pos[1]][current_pos[2]] += 2
        board = Board(self.master, value, cell_size)  # Pass self.master instead of root
        board.pack()
    def clearscreen(self):
        # Destroy all widgets in the first screen
        for widget in self.master.winfo_children():
            widget.destroy()
class SecondScreen:
    def __init__(self, master, level, callback):
        self.master = master
        self.level = level
        self.callback = callback  # Callback function to handle button click
        self.input = None
        # Define custom fonts
        self.title_font = ("Arial", 16, "bold")
        self.button_font = ("Arial", 12)

        # Create and pack the title label
        self.title_label = tk.Label(master, text=f"Screen for Level {level}", font=self.title_font)
        self.title_label.pack(pady=10)

        # Create buttons for the second screen
        for i in range(1, 6):
            button_text = f"{i}. Input{i}"
            input_button = tk.Button(master, text=button_text, command=lambda num=i: self.on_input_click(num),
                                     font=self.button_font)
            input_button.pack(pady=5)

    def on_input_click(self, input_num):
        messagebox.showinfo("Input Clicked", f"You clicked on Input {input_num} for Level {self.level}.")
        self.input = input_num
        self.callback(self.level, self.input)
    def clearscreen(self):
        # Destroy all widgets in the first screen
        for widget in self.master.winfo_children():
            widget.destroy()


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
            level_button = tk.Button(master, text=button_text, command=lambda l=level: self.on_level_click(l),
                                     font=self.button_font)
            level_button.pack(pady=5)
        self.selected_level = None  # Initialize selected_level to None

    def on_level_click(self, level):
        messagebox.showinfo("Level Selected", f"You clicked on Level {level}.")
        self.selected_level = level
        self.callback(self.selected_level)

    def clearscreen(self):
        # Destroy all widgets in the first screen
        for widget in self.master.winfo_children():
            widget.destroy()


class Board(tk.Canvas):
    def __init__(self, master, board_data, cell_size):
        rows = len(board_data)
        cols = len(board_data[0])
        super().__init__(master, width=cols * cell_size, height=rows * cell_size)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.board_data = board_data
        self.draw_board()

    def draw_board(self):
        # Color mapping for specific values
        special_color_mapping = {0: "white", '-1': "gray", "T1": "yellow"}

        # Define a range of red tones for positive values
        min_value = 1  # Minimum positive value
        max_value = 10  # Maximum positive value
        red_tones = ['#ff9999', '#ff8888', '#ff7777', '#ff6666', '#ff5555', '#ff4444', '#ff3333', '#ff2222', '#ff1111']

        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = self.board_data[row][col]
                value_text = str(cell_value)

                # Check for special values
                if cell_value in special_color_mapping:
                    color = special_color_mapping[cell_value]
                elif cell_value > 0:
                    # Map positive values to red tones
                    index = min(cell_value - min_value, len(red_tones) - 1)
                    color = red_tones[index]
                else:
                    # Default to white if not in mapping
                    color = "white"

                x1 = col * self.cell_size
                y1 = row * 0.75 * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + 0.75 * self.cell_size

                self.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
