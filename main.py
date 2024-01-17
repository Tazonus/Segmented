import tkinter as tk
from tkinter import ttk
import Segmenter_file as seg

class SegmenterGUI:
    def __init__(self,):
        self.root = tk.Tk()
        self.root.title("SegmentDead")
        self.root.geometry("500x450")
        self.segmenter = seg.Segmenter()

        # Create and configure the status label
        self.status_var = tk.StringVar()
        self.status_var.set(self.segmenter.title)
        status_label = ttk.Label(self.root, textvariable=self.status_var, font=('Helvetica', 18))
        status_label.grid(row=0, column=1, columnspan=4, pady=10)

        # Create buttons for different actions
        buttons = [
            ("Split", "split"),
            ("Stop", "stop"),
            ("Reset", "reset"),
            ("Exit", "exit")
        ]

        for i, (text, action) in enumerate(buttons):
            button = ttk.Button(self.root, text=text, command=lambda a=action: self.handle_button_click(a))
            button.grid(row=i + 1, column=0, pady=5)

        # Create a Listbox for displaying split times
        self.splits_list = tk.Listbox(self.root, selectmode=tk.BROWSE, font=('Helvetica', 10), width=50, height=20)
        self.splits_list.grid(row=1, column=1, columnspan=3, padx=10, pady=10, rowspan=10)

        # Create a label to display the current time
        self.segmenter.current_time_label_var = tk.StringVar()
        current_time_label = ttk.Label(self.root, textvariable=self.segmenter.current_time_label_var, font=('Helvetica', 16))
        current_time_label.grid(row=12, column=1, columnspan=4, pady=5)

        # Create a label to display the time since the last split
        self.segmenter.split_time_label_var = tk.StringVar()
        split_time_label = ttk.Label(self.root, textvariable=self.segmenter.split_time_label_var, font=('Helvetica', 12))
        split_time_label.grid(row=13, column=1, columnspan=4, pady=5)

        # Run the main loop
        self.update_labels()
        self.root.mainloop()
    
    def handle_button_click(self, action):
        if action == "split":
            self.segmenter.split()
        elif action == "stop":
            self.segmenter.stop()
        elif action == "reset":
            self.segmenter.reset()
        elif action == "exit":
            self.root.destroy()

    def update_splits_list(self):
        self.splits_list.delete(0, tk.END)  # Usuń wszystkie elementy z Listbox

        for line in self.segmenter.curent_run_lines:
            self.splits_list.insert(tk.END, line)  # Dodaj nowe splity do Listbox

    def update_labels(self):
        current_time = self.segmenter.get_curent_time()
        split_time = self.segmenter.format_time(self.segmenter.last_segment_time)

        self.segmenter.current_time_label_var.set(f"Current Time: {current_time}")
        self.segmenter.split_time_label_var.set(f"Split Time: {split_time}")

        self.update_splits_list()  # Aktualizuj Listbox z splitami

        self.root.after(10, self.update_labels)

if __name__ == "__main__":
    app = SegmenterGUI()
    
