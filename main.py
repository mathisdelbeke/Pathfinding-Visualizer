#!/usr/bin/env python3

import algos
from enum import Enum
import tkinter as tk

class AppState(Enum):
    SEL_START_POS = 0
    SEL_STOP_POS = 1
    SEL_OBSTACLES_POS = 2

class PathfinderVisualizer:
    GRID_SIZE = 30

    def __init__(self):
        self.current_state = AppState.SEL_START_POS
        self.grid = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.start_pos = ()
        self.stop_pos = ()
        self.app_root = tk.Tk()
        self.start_button = None
        self.field_buttons = [[None for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.init_app()

    def on_close_app(self):
        self.app_root.destroy()

    def on_start_button_click(self):
        path = algos.bfs(self.grid, self.start_pos, self.stop_pos)

        print(path)

    def on_field_button_click(self, row, column):
        if (self.current_state == AppState.SEL_START_POS):
            self.field_buttons[row][column].config(state="disabled", bg="blue")
            self.start_pos = (row, column)
            self.current_state = AppState.SEL_STOP_POS

        elif (self.current_state == AppState.SEL_STOP_POS):
            self.field_buttons[row][column].config(state="disabled", bg="red")
            self.stop_pos = (row, column)
            self.start_button.config(state="normal")
            self.current_state = AppState.SEL_OBSTACLES_POS
        
    def init_app(self):
        self.app_root.title("Pathfinder Visualizer")
        self.app_root.attributes("-fullscreen", True)

        # Top frame with close and start button
        top_frame = tk.Frame(self.app_root)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        close_button = tk.Button(top_frame, text="✕", command=self.on_close_app, fg="red", bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat")
        close_button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.start_button = tk.Button(top_frame, text="Start BFS", command=self.on_start_button_click, fg="blue", bg="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat", state="disabled")
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Wrapper frame to center content frame
        center_wrapper = tk.Frame(self.app_root)
        center_wrapper.pack(expand=True, fill=tk.BOTH)

        # Content frame with the field
        content_frame = tk.Frame(center_wrapper)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                button = tk.Button(content_frame, width=1, height=1, command=lambda row=i, column=j: self.on_field_button_click(row, column))
                self.field_buttons[i][j] = button
                button.grid(row=i, column=j)

        # Show app
        self.app_root.mainloop()

main = PathfinderVisualizer()