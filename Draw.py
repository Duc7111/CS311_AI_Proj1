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
        cell_size = (200 - len(floor_array) - len(floor_array[0])) / 5
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
        current_floor = agent.pos[0]
        floor_array1 = world.get_floor_array(current_floor)
        cell_size1 = (200 - len(floor_array1) - len(floor_array1[0])) / 5
        
        if self.value is None or current_floor != self.last_floor:
            floor_array = world.get_floor_array(current_floor)
            cell_size = (200 - len(floor_array) - len(floor_array[0])) / 5
            self.value = convert(floor_array)  # Update value array with new floor data
            self.last_floor = current_floor  # Record the current floor
           

        if self.value[current_agent.agents.pos[1]][current_agent.agents.pos[2]] not in check:
            self.value[current_agent.agents.pos[1]][current_agent.agents.pos[2]] += 1
        else:
            self.value[current_agent.agents.pos[1]][current_agent.agents.pos[2]] = 1
        if agent.pos[0] == current_floor:
            self.value[agent.pos[1]][agent.pos[2]] = "A1"
        board = Board(self.master, self.value, cell_size1)  # Pass self.master instead of root
        board.pack()
    def update_board_multi(self, world, agent_positions,agentKey,taskpos):
        self.clearscreen()
        print(agent_positions)
        if not agent_positions:
            return  # No positions to update
        #convert agentKey from A1 to T1, etc.
        task = agentKey.replace('A', 'T')
        # Find the first non-None floor value
        current_floor = next((floor for path in agent_positions.values() for floor, _, _ in path if floor is not None), None)
    
        if current_floor is None:
            return  # No valid positions found

        floor_array = world.get_floor_array(current_floor)
        cell_size = (200 - len(floor_array) - len(floor_array[0])) / 5

        if self.value is None or current_floor != self.last_floor:
            self.value = convert(floor_array)  # Update value array with new floor data
            self.last_floor = current_floor  # Record the current floor

        for agent_key, path in agent_positions.items():
            if path:
                floor, x, y = path[-1]  # Use the last position in the agent's path
            # Clear previous positions of the agent
                for i in range(len(self.value)):
                    for j in range(len(self.value[0])):
                        if self.value[i][j] == agent_key:
                            self.value[i][j] = 0
            # Update the current position of the agent
                if floor == current_floor:
                    self.value[x][y] = agent_key
                if taskpos[0] == current_floor:
                    self.value[taskpos[1]][taskpos[2]] = task
        board = Board(self.master, self.value, cell_size)  # Pass self.master instead of root
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
        self.original_values = {}  # Store the original values of the cells
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
            special_color_mapping[f"D{i}"] = "#EA7DFF"
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
                self.original_values[(row, col)] = cell_value

                self.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
                if cell_value not in {0, '-1'}:
                    label_x = (x1 + x2) / 2
                    label_y = (y1 + y2) / 2
                    self.create_text(label_x, label_y, text=str(cell_value), fill="black")
    def update_cell(self, row, col, value):
        # Update a specific cell with the given value
        self.board_data[row][col] = value

        # Check if the cell contains a special value
        if self.original_values.get((row, col)) not in {'T1', 'A1', 'K1', 'D1'}:
            # If not a special value, update the display with the new value
            self.create_rectangle(
                col * self.cell_size,
                row * 0.75 * self.cell_size,
                (col + 1) * self.cell_size,
                (row + 1) * 0.75 * self.cell_size,
                outline="black",
                fill=value,
            )
            if value not in {0, '-1'}:
                label_x = (col * self.cell_size + (col + 1) * self.cell_size) / 2
                label_y = (row * 0.75 * self.cell_size + (row + 1) * 0.75 * self.cell_size) / 2
                self.create_text(label_x, label_y, text=str(value), fill="black")
        else:
            # If it's a special value, restore the original display
            self.draw_board()
