import time
import re
from World import World
from Draw import MoveYourStepProjectApp, SecondScreen, AlgorithmScreen, Board, convert
import tkinter as tk
from tkinter import messagebox
from Algo import bfs, UCS, Astar,decisionSearch
import sys
import pygetwindow as gw
import pyautogui
from Level4 import Level4
def visualize_heatmap(world, move, score,cell_size):
    app.clearscreen()

    for floor_index in range(len(world.floors)):
        current_floor_data = world.get_floor_array(floor_index)

        # Create a separate value array for each floor
        value = convert(current_floor_data)

        for index, item in enumerate(reversed(move)):
            is_last_item = index == 0

            # Check if the item is on the current floor
            if item.agents.pos[0] == floor_index:
                if is_last_item:
                    value[item.agents.pos[1]][item.agents.pos[2]] = 'A1'
                else:
                    if re.match(r'(D\d+|A\d+|K\d+|T\d+)', str(value[item.agents.pos[1]][item.agents.pos[2]])):
                        value[item.agents.pos[1]][item.agents.pos[2]] = 1
                    else:
                        value[item.agents.pos[1]][item.agents.pos[2]] = int(value[item.agents.pos[1]][item.agents.pos[2]]) + 1

        # Create a board for each floor
        board = Board(app.master, value, cell_size)
        board.pack()

    # Display the score label for the overall score
    score_label = tk.Label(app.master, text=f"Overall Score: {score}", font=("Arial", 12))
    score_label.pack(pady=10)


def capture_window(window_title):
    # Get the specified window by its title
    window = gw.getWindowsWithTitle(window_title)

    if not window:
        print(f"Window with title '{window_title}' not found.")
        return

    # Get the bounding box of the window
    window_rect = window[0]._rect

    # Capture the content of the specified window
    screenshot = pyautogui.screenshot(region=(window_rect.left, window_rect.top, window_rect.width, window_rect.height))

    # Save the screenshot to a file
    screenshot.save("window_screenshot.png")

    print(f"Screenshot of '{window_title}' captured and saved.")

if __name__ == "__main__":

    def handle_level_selection(selected_level):
        print(f"Selected Level in main function: {selected_level}")
        app.clearscreen()
        second_screen = SecondScreen(root, selected_level, handle_algorithm_selection)

    def handle_algorithm_selection(level, input_file):
        app.clearscreen()
        if level == 1:
            algorithm_screen = AlgorithmScreen(root, level, input_file, handle_algorithm_click)
        else:
            handle_algorithm_click(level, input_file, None)

    def handle_algorithm_selection(level, input_file, algorithm=None):
        app.clearscreen()
        if level == 1:
            algorithm_screen = AlgorithmScreen(root, level, input_file, handle_algorithm_click)
        else:
            handle_algorithm_click(level, input_file, None)
        # Create and display the algorithm selection screen
    def handle_algorithm_click(level, input_file, algorithm):
        print(f"Selected Level in main function: {level}")
        print(f"Selected Input in main function: {input_file}")
        print(f"Selected Algorithm in main function: {algorithm}")
        app.clearscreen()
        inp = "input"+str(input_file)+"_level"+str(level)+".txt"
        world = World(inp)
        move = []
        score = 100
        cell_size=20
        if level == 1:
            algorithm_screen = AlgorithmScreen(root, level, input_file, handle_algorithm_click)
            if algorithm == "BFS":
                final, steps = bfs(world)
            elif algorithm == "UCS":
                final, steps = UCS(world)
            else:
                final, steps = Astar(world)
            if final is not None:
                for pos in steps:
                    algorithm_screen.update_board(world, pos)
                    app.master.update()  # Force an update of the GUI
                    app.master.after(80)
            while final is not None:
                move.append(final.agents.pos)
                final = final.parent
                score -= 1
            floor_index_to_access = 0  # Replace this with the desired floor index
            floor_array = world.get_floor_array(floor_index_to_access)
            value = convert(floor_array)
            cell_size = (200 - len(floor_array) - len(floor_array[0])) / 5
            for index, item in enumerate(reversed(move)):
                is_last_item = index == 0
                if is_last_item:
                    value[item[1]][item[2]] = 'A1'
                else:
                    if re.match(r'(D\d+|A\d+|K\d+|T\d+)', str(value[item[1]][item[2]])):
                        pass
                    else:
                        value[item[1]][item[2]] = int(value[item[1]][item[2]]) + 1
            app.clearscreen()
            board = Board(root, value, cell_size)
            board.pack()
            score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 12))
            score_label.pack(pady=10)
        elif level == 2 or level == 3:
            algorithm_screen = AlgorithmScreen(root, level, input_file, handle_algorithm_click)
            final = decisionSearch(world)
            floor_index_to_access = 0  # Replace this with the desired floor index
            floor_array = world.get_floor_array(floor_index_to_access)
            value = convert(floor_array)
            agent = world.agents["A1"]
            value[agent.pos[1]][agent.pos[2]]="A1"
            app.clearscreen()
            board = Board(root, value, cell_size)
            board.pack()
            path = []
            if final is not None:
                while final is not None:
                    path.append(final)
                    final = final.parent
                    score -= 1
                for current_node in reversed(path):
                    algorithm_screen.update_board_advance(world, current_node)
                    app.master.update()  # Force an update of the GUI
                    app.master.after(250)
                visualize_heatmap(world, path,score,cell_size)
            else: 
                app.Message("No solution")
        elif level == 4:
            algorithm_screen = AlgorithmScreen(root, level, input_file, handle_algorithm_click)
            level4 = Level4(world)
            app.clearscreen()
            floor_index_to_access = 0  # Replace this with the desired floor index
            floor_array = world.get_floor_array(floor_index_to_access)
            value = convert(floor_array)
            app.clearscreen()
            board = Board(root, value, cell_size)
            board.pack()
            paths = {}
            for agentKey, path in level4.agents.items():
                paths[agentKey] = [path[0][0]]
            while True:
                result = level4.move()
                # record path
                for agentKey, path in level4.agents.items():
                    if path[0] is not None:
                        val = path[0][path[1] - 1]
                        paths[agentKey].append(val)
                        algorithm_screen.update_board_multi(world, val, agentKey)
                        app.master.update()  # Force an update of the GUI
                        app.master.after(200)
                        print(agentKey, val)
                if result == -1:
                    print('A1 has reached task')
                    break
                elif result == -2:
                    print('No possible move')
                    break

        capture_window("MoveYourStepProject")


    root = tk.Tk()
    app = MoveYourStepProjectApp(root, handle_level_selection)
    root.mainloop()

