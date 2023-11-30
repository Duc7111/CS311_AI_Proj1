from World import World
from Draw import MoveYourStepProjectApp, SecondScreen, AlgorithmScreen
import tkinter as tk
from tkinter import messagebox
from Algo import bfs, UCS, Astar


if __name__ == "__main__":

    def handle_level_selection(selected_level):
        print(f"Selected Level in main function: {selected_level}")

        app.clearscreen()

        # Create and display the second screen
        second_screen = SecondScreen(root, selected_level, handle_input_selection)
    def handle_input_selection(selected_level, selected_input):
        app.clearscreen()

        # Create and display the second screen
        algorithm_screen = AlgorithmScreen(root, selected_level, selected_input, handle_algorithm_click)

    def handle_algorithm_selection(level, input_file):
        print(f"Selected Level in main function: {level}")
        print(f"Selected Input in main function: {input_file}")

        app.clearscreen()

        # Create and display the algorithm selection screen
    def handle_algorithm_click(level, input_file, algorithm):
        print(f"Selected Level in main function: {level}")
        print(f"Selected Input in main function: {input_file}")
        print(f"Selected Algorithm in main function: {algorithm}")
        inp = "input"+str(input_file)+"_level"+str(level)+".txt"
        world = World(inp)
        if algorithm == "BFS":
            final = bfs(world)
        elif algorithm == "UCS":
            final = UCS(world)
        else:
            final = Astar(world)
        while final is not None:
            print(final.agents.pos)
            final = final.parent

    root = tk.Tk()
    app = MoveYourStepProjectApp(root, handle_level_selection)
    root.mainloop()


