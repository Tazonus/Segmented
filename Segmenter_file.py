import tkinter as tk
from tkinter import ttk
import time

class Segmenter:
    def __init__(self):
        self.title = "Starcraft 2 - Wings of Liberty"
        self.category = "Any% Normal"
        
        #those will go to vector:
        #self.current_time_label_var = None
        #self.split_time_label_var = None

        #and these will go to tuple:
        self.segments_time = []
        self.segment_names = [
            "Liberation Day", "The Outlaws", "Zero Hour", "Smash and Grab",
            "The Devil's Playground", "Welcome to the Jungle", "The Great Train Robbery",
            "Cutthroat", "Ghost of a Chance", "The Dig", "Whispers of Doom",
            "A Sinister Turn", "Echoes of the Future", "The Moebius Factor",
            "Supernova", "Maw of the Void", "The Gates of Hell", "Shatter the Sky", "All In"
        ]

        #temp:
        self.is_running = False
        self.start_time = 0
        self.last_segment_time = 0
        self.current_segment = 0
        self.curent_run_lines = []

    def get_curent_time(self):
        if self.is_running:
            curent_time = time.time() - self.start_time
            return self.format_time(curent_time)
        else:
            return self.last_segment_time

    def get_segment_time(self):
        if self.is_running:
            segment_time = self.get_curent_time() - self.last_segment_time_time()
            return segment_time

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours <= 0:
            if minutes <= 0:
                return f"{seconds:.2f}"
            else:
                return f"{int(minutes):02}:{seconds:.2f}"
        else:
            return f"{int(hours):02}:{int(minutes):02}:{seconds:.2f}"
        
    def make_line(self, current_time):
        return (f"Split {self.segment_names[self.current_segment]}: {self.format_time(current_time)}")
        #in progress
        
    def start(self):
        if not self.is_running:
            self.reset()
            self.start_time = time.time()
            self.is_running = True
            while len(self.curent_run_lines) < len(self.segment_names):
                self.curent_run_lines.append("")
        print("Start time.")

    def stop(self):
        if self.is_running:
            elapsed_time = time.time() - self.start_time
            self.is_running = False
            print(f"Stopped. Total time: {self.format_time(elapsed_time)}")

    def reset(self):
        self.is_running = False
        self.start_time = 0
        self.last_segment_time = 0
        self.current_segment = 0
        self.curent_run_lines = []
        print("Reset time.")

    def split(self):
        if self.is_running:
            print(f"Split {self.current_segment+1}.")

            current_time = time.time() - self.start_time
            split_time = current_time - self.last_segment_time

            self.last_segment_time = current_time
            if self.current_segment < len(self.segment_names) - 1:
                segment_name = self.segment_names[self.current_segment]

                self.curent_run_lines[self.current_segment] = self.make_line(current_time)
            else:
                if self.current_segment == len(self.segment_names) - 1:
                    segment_name = self.segment_names[self.current_segment]
                    self.curent_run_lines[self.current_segment] = self.make_line(current_time)
                self.stop()
            self.current_segment += 1
        else:
            self.start()
