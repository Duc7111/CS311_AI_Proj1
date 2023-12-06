import time

from World import World
from Draw import MoveYourStepProjectApp, SecondScreen, AlgorithmScreen, Board, convert
import tkinter as tk
from tkinter import messagebox
from Algo import bfs, UCS, Astar
import pygame
import sys

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
        floor_index_to_access = 0  # Replace this with the desired floor index
        floor_array = world.get_floor_array(floor_index_to_access)
        value = convert(floor_array)
        print(value)
        cell_size = (200-len(floor_array)-len(floor_array[0]))/6
        board = Board(root, value, cell_size)
        value_test=convert(floor_array)
        move = []
        board.pack()
        if algorithm == "BFS":
            algorithm_screen = AlgorithmScreen(root, level, input_file, handle_algorithm_click)
            final, steps = bfs(world, update_screen_callback=algorithm_screen.update_board)
            if final is not None:
                for pos in steps:
                    algorithm_screen.update_board(world, pos)
                    app.master.update()  # Force an update of the GUI
                    app.master.after(100)
        elif algorithm == "UCS":
            final = UCS(world)
        else:
            final = Astar(world)
        while final is not None:
            move.append(final.agents.pos)
            final = final.parent
        for item in reversed(move):
            if value[item[1]][item[2]] != 'T1':
                value[item[1]][item[2]] = int(value[item[1]][item[2]]) + 1
            print(item)
        app.clearscreen()
        board = Board(root, value, cell_size)
        board.pack()

    root = tk.Tk()
    app = MoveYourStepProjectApp(root, handle_level_selection)
    root.mainloop()

