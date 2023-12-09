import tkinter as tk
from tkinter import messagebox

from _cffi_backend import callback


def convert(board):
    converted_board = [[0 if cell == '0' else cell for cell in row] for row in board]
    return converted_board


def special_val():
    arr = []
    for i in range(0, 10):
        arr.append(f"A{i}")
        arr.append(f"T{i}")
        arr.append(f"K{i}")
        arr.append(f"D{i}")
    arr.append("UP")
    arr.append("DO")
    return arr


check = special_val()


class AlgorithmScreen:
    def __init__(self, master, level, input_file, callback):
        self.master = master
        self.level = level
        self.input_file = input_file
        self.value = None
        self.callback = callback  # Callback function to handle algorithm selection
        # Define custom fonts
        self.title_font = ("Arial", 16, "bold")
        self.button_font = ("Arial", 12)
        self.score = 100  # Add a score attribute

        # Create a label to display the score
        self.score_label = tk.Label(master, text=f"Score: {self.score}", font=("Arial", 12))

        # Create and pack the title label
        self.title_label = tk.Label(master, text=f"Algorithm Selection for Level {level} - Input {input_file}",
                                    font=self.title_font)
        self.title_label.pack(pady=10)

        # Create buttons for algorithm selection
        algorithms = ["BFS", "UCS", "A*"]
        for algorithm in algorithms:
            algorithm_button = tk.Button(master, text=algorithm,
                                         command=lambda alg=algorithm: self.on_algorithm_click(alg),
                                         font=self.button_font)
            algorithm_button.pack(pady=5)

    def on_algorithm_click(self, algorithm):
        self.callback(self.level, self.input_file, algorithm)

    def update_board(self, world, current_pos):
        self.clearscreen()
        agent = world.agents["A1"]
        floor_index_to_access = current_pos[0]
        floor_array = world.get_floor_array(floor_index_to_access)
        cell_size = (200 - len(floor_array) - len(floor_array[0])) / 6
        if self.value is None:
            self.value = convert(floor_array)  # Initialize value array if not set

        if self.value[current_pos[1]][current_pos[2]] not in check:
            self.value[current_pos[1]][current_pos[2]] += 1

        self.value[agent.pos[1]][agent.pos[2]] = "A1"

        board = Board(self.master, self.value, cell_size)  # Pass self.master instead of root
        board.pack()

    def update_board_advance(self, world, current_agent):
        self.clearscreen()
        agent = world.agents["A1"]
        current_floor = current_agent.agents.pos[0]
        floor_array1 = world.get_floor_array(current_floor)
        cell_size1 = (200 - len(floor_array1) - len(floor_array1[0])) / 6

        if self.value is None or current_floor != self.last_floor:
            floor_array = world.get_floor_array(current_floor)
            cell_size = (200 - len(floor_array) - len(floor_array[0])) / 6
            self.value = convert(floor_array)  # Update value array with new floor data
            self.last_floor = current_floor  # Record the current floor

        if self.value[current_agent.agents.pos[1]][current_agent.agents.pos[2]] not in check:
            self.value[current_agent.agents.pos[1]][current_agent.agents.pos[2]] += 1
        else:
            self.value[current_agent.agents.pos[1]][current_agent.agents.pos[2]] = 1
        self.value[agent.pos[1]][agent.pos[2]] = "A1"
        board = Board(self.master, self.value, cell_size1)  # Pass self.master instead of root
        board.pack()
    def update_board_multi(self, world, current_agent,agentkey):
        self.clearscreen()
        agent = world.agents[agentkey]
        current_floor = current_agent[0]
        floor_array1 = world.get_floor_array(current_floor)
        cell_size1 = (200 - len(floor_array1) - len(floor_array1[0])) / 6

        if self.value is None or current_floor != self.last_floor:
            floor_array = world.get_floor_array(current_floor)
            cell_size = (200 - len(floor_array) - len(floor_array[0])) / 6
            self.value = convert(floor_array)  # Update value array with new floor data
            self.last_floor = current_floor  # Record the current floor

        if self.value[current_agent[1]][current_agent[2]] not in check:
            self.value[current_agent[1]][current_agent[2]] += 1
        else:
            self.value[current_agent[1]][current_agent[2]] = 1
        #self.value[agent[1]][agent[2]] = agentkey
        board = Board(self.master, self.value, cell_size1)  # Pass self.master instead of root
        board.pack()


    def clearscreen(self):
        # Destroy all widgets in the first screen
        for widget in self.master.winfo_children():
            widget.destroy()

    def updatescore(self, score):
        self.score = score
        self.score_label.config(text=f"Score: {self.score}")
        self.score_label.pack(pady=10)


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
        special_color_mapping = {0: "white", '-1': "gray", 'UP': "brown", 'DO': "brown"}
        for i in range(0, 10):
            special_color_mapping[f"A{i}"] = "green"
        for i in range(0, 10):
            special_color_mapping[f"T{i}"] = "yellow"
        for i in range(0, 10):
            special_color_mapping[f"K{i}"] = "#8dbfff"
        for i in range(0, 10):
            special_color_mapping[f"D{i}"] = "#5e0511"
        # Define a range of red tones for positive values
        min_value = 1  # Minimum positive value
        max_value = 20  # Maximum positive value
        red_tones = ['#ff9999', '#ff8888', '#ff7777', '#ff6666', '#ff5555', '#ff4444', '#ff3333', '#ff2222', '#ff1111',
                     '#ff0000', '#fd0000', '#fb0000', '#f90000', '#f70000', '#f50000', '#f30000', '#f10000', '#ef0000']

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
                if cell_value not in {0, '-1'}:
                    label_x = (x1 + x2) / 2
                    label_y = (y1 + y2) / 2
                    self.create_text(label_x, label_y, text=str(cell_value), fill="black")

