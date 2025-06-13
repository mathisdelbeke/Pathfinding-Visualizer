#!/usr/bin/env python3

import algos
from enum import Enum
import time
import tkinter as tk

class AppState(Enum):                                                                                   
    SEL_START_POS = 0
    SEL_STOP_POS = 1
    SEL_OBSTACLES_POS = 2

class PathfinderVisualizer:
    GRID_SIZE = 30                                                                                      # For drawing the 2 dim grid (e.g. 30 x 30)

    def __init__(self):
        self.current_state = AppState.SEL_START_POS                                                     # For deciding which buttons are enabled
        self.grid = self.get_new_grid()                                                                 # 2 dim grid for saving which block is free/obstacle
        self.start_pos = ()
        self.stop_pos = ()
        self.app_root = tk.Tk()
        self.reset_button = None
        self.start_button = None
        self.field_buttons = [[None for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]     # 2 dim grid with buttons, corresponding with previous grid
        self.algo_stats_text = None
        self.default_button_bg = ""                                                                     # To Save color of a default tkinter button
        self.init_app()

    def on_close_app(self):                                                                             # Destroys application (with window) cleanly 
        self.app_root.destroy()

    def on_reset_button_click(self):
        self.reset_app()

    def on_start_button_click(self):
        self.disable_all_buttons()                                                                      # Prevent user input during path animation
        path = algos.bfs(self.grid, self.start_pos, self.stop_pos)                                      
        if (path != None):                                                                              # If path is found                                                                              
            self.show_algo_stats(path)
            for steps in path:                                                                          # Animate steps of the path
                self.field_buttons[steps[0]][steps[1]].config(bg="green")   
                self.app_root.update()                                                                  # Keeps UI changing when using timer.sleep
                time.sleep(0.1)
            self.reset_button.config(state="normal")
        else: 
            self.reset_app()

    def on_field_button_click(self, row, column):
        if (self.current_state == AppState.SEL_START_POS):                                              # Selecting start position
            self.field_buttons[row][column].config(state="disabled", bg="blue")
            self.start_pos = (row, column)
            self.current_state = AppState.SEL_STOP_POS

        elif (self.current_state == AppState.SEL_STOP_POS):                                             # Selecting stop position
            self.field_buttons[row][column].config(state="disabled", bg="red")
            self.start_button.config(state="normal")                                                    # Algo may be started now
            self.stop_pos = (row, column)
            self.current_state = AppState.SEL_OBSTACLES_POS

        elif (self.current_state == AppState.SEL_OBSTACLES_POS):                                        # Selecting blocks as obstacles
            self.field_buttons[row][column].config(state="disabled", bg="grey") 
            self.grid[row][column] = 1                                                                  # Save obstacle in grid

    def init_app(self):
        self.app_root.title("Pathfinder Visualizer")
        self.app_root.attributes("-fullscreen", True)
        
        temp_button = tk.Button()                                                                       # Temp button to copy its default color
        self.default_button_bg = temp_button.cget("background")

        # Top frame with close, reset and start button
        top_frame = tk.Frame(self.app_root)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        close_button = tk.Button(top_frame, text="✕", command=self.on_close_app, fg="red", bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat")
        close_button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.reset_button = tk.Button(top_frame, text="Reset", command=self.on_reset_button_click, fg="red", bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat")
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.start_button = tk.Button(top_frame, text="Start BFS", command=self.on_start_button_click, fg="blue", bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat", state="disabled")
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Wrapper frame to center content frame
        center_wrapper = tk.Frame(self.app_root)
        center_wrapper.pack(expand=True, fill=tk.BOTH)

        # Content frame with the field button grid and algo stats text
        content_frame = tk.Frame(center_wrapper)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Frame for the field button grid (left side)
        button_grid_frame = tk.Frame(content_frame)
        button_grid_frame.pack(side=tk.LEFT)

        # Make field of buttons with callback
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                button = tk.Button(button_grid_frame, width=1, height=1, bg=self.default_button_bg, command=lambda row=i, column=j: self.on_field_button_click(row, column))
                self.field_buttons[i][j] = button
                button.grid(row=i, column=j)
        
        # Make a text block that will hold algo stats
        self.algo_stats_text = tk.Text(content_frame, height=5, width=40)
        self.algo_stats_text.insert("1.0", "Algo stats: ")
        self.algo_stats_text.config(state="disabled")
        self.algo_stats_text.pack(side=tk.RIGHT, padx=10)

        # Show app
        self.app_root.mainloop()
    
    def disable_all_buttons(self):           
        self.reset_button.config(state="disabled")                                                                                        
        self.start_button.config(state="disabled")
        for i in range(len(self.field_buttons)):                                                        
            for j in range(len(self.field_buttons[i])):
                self.field_buttons[i][j].config(state="disabled")

    def reset_app(self):
        self.current_state = AppState.SEL_START_POS
        self.grid = self.get_new_grid()
        self.start_pos = ()
        self.stop_pos = ()
        self.reset_button.config(state="normal")
        self.start_button.config(state="disabled")
        self.algo_stats_text.config(state="normal") 
        self.algo_stats_text.delete("2.0", tk.END)                                                      # Leaves first line intact
        self.algo_stats_text.config(state="disabled")
        for i in range(len(self.field_buttons)):
            for j in range(len(self.field_buttons[i])):
                self.field_buttons[i][j].config(state="normal", bg=self.default_button_bg)

    def show_algo_stats(self, path):
        self.algo_stats_text.config(state="normal")
        self.algo_stats_text.insert("end", f"\n\n\t{len(path)} steps needed")                           # Leaves first line intact
        self.algo_stats_text.config(state="disabled")

    def get_new_grid(self):
        return [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]


if __name__ == "__main__":
    pfv = PathfinderVisualizer()