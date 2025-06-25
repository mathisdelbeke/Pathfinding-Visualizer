#!/usr/bin/env python3

import algos
from enum import Enum
import time
import tkinter as tk

class AppState(Enum):                                                                                   
    SEL_START_POS = 0
    SEL_STOP_POS = 1
    SEL_OBSTACLES_POS = 2

class ObstacleType(Enum):
    WALL = 0
    WATER = 1

class PathfinderVisualizer:
    GRID_SIZE = 30                                                                                      # For drawing the 2 dim grid (e.g. 30 x 30)
    start_pos_color = "red"
    stop_pos_color = "red"
    reset_button_color = "red"
    start_algos_button_color = "blue"
    wall_color = "grey"
    water_color = "blue"
    discovered_color = "orange"
    path_color = "green"

    def __init__(self):
        self.current_state = AppState.SEL_START_POS                                                     # For deciding which buttons are enabled
        self.current_obstacle_type = ObstacleType.WALL
        self.grid = self.get_new_grid()                                                                 # 2 dim grid for saving which block is free/obstacle
        self.start_pos = ()
        self.stop_pos = ()
        self.app_root = tk.Tk()
        self.reset_button = None
        self.start_buttons = []
        self.water_button = None
        self.wall_button = None
        self.field_buttons = [[None for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]     # 2 dim grid with buttons, corresponding with previous grid
        self.algo_stats_text = None
        self.default_button_bg = ""                                                                     # To Save color of a default tkinter button
        self.init_app()

    def on_close_app(self):                                                                             # Destroys application (with window) cleanly 
        self.app_root.destroy()

    def on_reset_button_click(self):
        self.reset_app()

    def on_start_button_click(self, selected_algo):
        self.disable_all_buttons()                                                                      # Prevent user input during animations
        algo_results = None
        if (selected_algo == "BFS"):
            algo_results = algos.bfs(self.grid, self.start_pos, self.stop_pos)

        elif(selected_algo == "Dijkstra"):
            algo_results = algos.dijkstra(self.grid, self.start_pos, self.stop_pos)

        elif(selected_algo == "A*"):
            algo_results = algos.a_star(self.grid, self.start_pos, self.stop_pos)
            
        if (algo_results != None):                                                                      # If path is found
            self.show_algo_stats(algo_results)
            self.animate_discovered_in_order(algo_results.discovered_in_order)
            self.animate_path(algo_results.path)
            self.reset_button.config(state="normal")
        else: 
            self.reset_app()

    def on_select_obstacle_click(self, obstacle_type):
        self.current_obstacle_type = obstacle_type
        if (self.current_obstacle_type == ObstacleType.WALL):
            self.water_button.config(state="normal")
            self.wall_button.config(state="disabled")
        elif (self.current_obstacle_type == ObstacleType.WATER):
            self.wall_button.config(state="normal")
            self.water_button.config(state="disabled")

    def on_field_button_click(self, row, column):
        if (self.current_state == AppState.SEL_START_POS):                                              # Selecting start position
            self.field_buttons[row][column].config(state="disabled", bg=self.start_pos_color)
            self.start_pos = (row, column)
            self.current_state = AppState.SEL_STOP_POS

        elif (self.current_state == AppState.SEL_STOP_POS):                                             # Selecting stop position
            self.field_buttons[row][column].config(state="disabled", bg=self.stop_pos_color)
            self.enable_start_buttons()                                                                 # Algo may be started now
            self.stop_pos = (row, column)
            self.current_state = AppState.SEL_OBSTACLES_POS

        elif (self.current_state == AppState.SEL_OBSTACLES_POS):                                        # Selecting blocks as obstacles
            if (self.current_obstacle_type == ObstacleType.WALL):
                self.field_buttons[row][column].config(state="disabled", bg=self.wall_color) 
                self.grid[row][column] = 1                                                              # Save obstacle in grid
            elif(self.current_obstacle_type == ObstacleType.WATER):
                self.field_buttons[row][column].config(state="disabled", bg=self.water_color)
                self.grid[row][column] = 1

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
        self.reset_button = tk.Button(top_frame, text="Reset", command=self.on_reset_button_click, fg=self.reset_button_color, bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat")
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.start_buttons.append(tk.Button(top_frame, text="Start BFS", command=lambda: self.on_start_button_click("BFS"), fg=self.start_algos_button_color, bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat", state="disabled"))
        self.start_buttons[0].pack(side=tk.LEFT, padx=10, pady=5)
        self.start_buttons.append(tk.Button(top_frame, text="Start Dij", command=lambda: self.on_start_button_click("Dijkstra"), fg=self.start_algos_button_color, bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat", state="disabled"))
        self.start_buttons[1].pack(side=tk.LEFT, padx=10, pady=5)
        self.start_buttons.append(tk.Button(top_frame, text="Start A*", command=lambda: self.on_start_button_click("A*"), fg=self.start_algos_button_color, bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat", state="disabled"))
        self.start_buttons[2].pack(side=tk.LEFT, padx=10, pady=5)

        # Wrapper frame to center content frame
        center_wrapper = tk.Frame(self.app_root)
        center_wrapper.pack(expand=True, fill=tk.BOTH)

        # Content frame with the field button grid and algo stats text
        content_frame = tk.Frame(center_wrapper)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Buttons to select which obstacle to place
        self.wall_button = tk.Button(content_frame, text="Walls", command=lambda: self.on_select_obstacle_click(ObstacleType.WALL), fg="black", bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat", state="disabled")
        self.wall_button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.water_button = tk.Button(content_frame, text="Water", command=lambda: self.on_select_obstacle_click(ObstacleType.WATER), fg=self.water_color, bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat", state="normal")
        self.water_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Make a text block that will hold algo stats
        self.algo_stats_text = tk.Text(content_frame, height=5, width=40)
        self.algo_stats_text.insert("1.0", "Algo stats: ")
        self.algo_stats_text.config(state="disabled")
        self.algo_stats_text.pack(side=tk.RIGHT, padx=10)
        
        # Frame for the field button grid (left side)
        button_grid_frame = tk.Frame(content_frame)
        button_grid_frame.pack(side=tk.LEFT)

        # Make field of buttons with callback
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                button = tk.Button(button_grid_frame, width=1, height=1, bg=self.default_button_bg, command=lambda row=i, column=j: self.on_field_button_click(row, column))
                self.field_buttons[i][j] = button
                button.grid(row=i, column=j)
        
        # Show app
        self.app_root.mainloop()

    def reset_app(self):
        self.current_state = AppState.SEL_START_POS
        self.current_obstacle_type = ObstacleType.WALL
        self.wall_button.config(state="disabled")
        self.water_button.config(state="normal")
        self.grid = self.get_new_grid()
        self.start_pos = ()
        self.stop_pos = ()
        self.reset_button.config(state="normal")
        self.disable_start_buttons()
        self.algo_stats_text.config(state="normal") 
        self.algo_stats_text.delete("2.0", tk.END)                                                      # Leaves first line intact
        self.algo_stats_text.config(state="disabled")
        for i in range(len(self.field_buttons)):
            for j in range(len(self.field_buttons[i])):
                self.field_buttons[i][j].config(state="normal", bg=self.default_button_bg)

    def disable_all_buttons(self):           
        self.reset_button.config(state="disabled")                                                                                        
        self.disable_start_buttons()
        for i in range(len(self.field_buttons)):                                                        
            for j in range(len(self.field_buttons[i])):
                self.field_buttons[i][j].config(state="disabled")

    def enable_start_buttons(self):
        for button in self.start_buttons:
            button.config(state="normal")

    def disable_start_buttons(self):
        for button in self.start_buttons:
            button.config(state="disable")

    def animate_discovered_in_order(self, discovered_in_order):
        for visit in discovered_in_order:
            self.field_buttons[visit[0]][visit[1]].config(bg=self.discovered_color)
            self.app_root.update()                                                                  # Keeps UI changing when using timer.sleep
            time.sleep(0.01)

    def animate_path(self, path):
        for step in path:                                                             
            self.field_buttons[step[0]][step[1]].config(bg=self.path_color)   
            self.app_root.update()                                                                  # Keeps UI changing when using timer.sleep
            time.sleep(0.1)
    
    def show_algo_stats(self, algo_results):
        self.algo_stats_text.config(state="normal")
        self.algo_stats_text.insert("end", f"\n\n\t{len(algo_results.path)} steps")               
        self.algo_stats_text.insert("end", f"\n\t{len(algo_results.discovered_in_order)} discovered")
        self.algo_stats_text.config(state="disabled")

    def get_new_grid(self):
        return [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]


if __name__ == "__main__":
    pfv = PathfinderVisualizer()