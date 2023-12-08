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
        cell_size=40
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
            cell_size = (200 - len(floor_array) - len(floor_array[0])) / 6
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
            value[0][3] = "A1"
            app.clearscreen()
            board = Board(root, value, cell_size)
            board.pack()

            while final is not None:
                algorithm_screen.update_board_advance(world, final)
                app.master.update()  # Force an update of the GUI
                app.master.after(200)
                final = final.parent

        capture_window("MoveYourStepProject")


    root = tk.Tk()
    app = MoveYourStepProjectApp(root, handle_level_selection)
    root.mainloop()

