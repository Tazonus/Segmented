import tkinter as tk
import customtkinter as ctk
import Segmenter as seg
from pynput import keyboard
from tkinter import ttk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()        
        self.segmenter = seg.Segmenter()
        listener = keyboard.Listener(on_press=self.keyPressed,on_release=self.keyReleased)
        self.keyShortcuts = [("'s'","segment")]
        self.shortcutBuffor = ""

        self.setup()
        listener.start()

        self.update_segment_list()
        self.update_labels()
        self.mainloop()

### INPUT HANDLING
    def keyReleased(self,key):
        '''Handles Releasing a key, used with shortcuts'''
        character = str(key)
        self.shortcutBuffor = self.shortcutBuffor.replace(character, '')
    def keyPressed(self,key):
        '''Handles Pressing a key, used with shortcuts'''
        self.shortcutBuffor += str(key)
        if 'Key.ctrl' in self.shortcutBuffor and 'Key.alt' in self.shortcutBuffor:
            for x in self.keyShortcuts:
                if self.shortcutBuffor.find(x[0]) > 0:
                    self.handle_button_click(x[1])
    def handle_button_click(self, action):
        '''Handles button click'''
        if action == "segment":
            self.segmenter.segment()
        elif action == "stop":
            self.segmenter.stop()
        elif action == "reset":
            self.segmenter.reset()
        elif action == "exit":
            self.destroy()  

### Setup
    def setup(self):
        '''Setups Graphical user interface'''
        self.title("SegmentDead")
        self.geometry("500x520")
        self.setup_title(self.segmenter.title)
        self.setup_category(self.segmenter.category)
        self.setup_buttons()
        self.setup_curentTime()
        self.setup_list()
        
    def setup_title(self, title):
        '''Setups label displaying title'''
        self.title_var = tk.StringVar()
        self.title_var.set(title)
        title_label = ttk.Label(self, textvariable=self.title_var, font=('Helvetica', 18))
        title_label.grid(row=0, column=1, columnspan=1000, pady= [8,0])   
    def setup_category(self, category):
        '''Setups label displaying category'''
        self.category_var = tk.StringVar()
        self.category_var.set(category)
        category_label = ttk.Label(self, textvariable=self.category_var, font=('Helvetica', 12))
        category_label.grid(row=1, column=1, columnspan=1000)
    def setup_buttons(self):
        '''Setups button to segment, stop, reset and exit program'''        
        buttons = [
            ("Segment", "segment"),
            ("Stop", "stop"),
            ("Reset", "reset"),
            ("Exit", "exit")
        ]
        for i, (text, action) in enumerate(buttons):
            button = ttk.Button(self, text=text, command=lambda a=action: self.handle_button_click(a))
            button.grid(row=i + 2, column=0, pady=5)
    def setup_curentTime(self):
        '''Setups display for curent time, and curent segment time'''
                #Label displaying current time
        self.segmenter.current_time_label_var = tk.StringVar()
        current_time_label = ttk.Label(self, textvariable=self.segmenter.current_time_label_var, font=('Helvetica', 16))
        current_time_label.grid(row=13, column=1, columnspan=4, pady=5)

        #Label displaying time since the last segment(not split)
        self.segmenter.segment_time_label_var = tk.StringVar()
        segment_time_label = ttk.Label(self, textvariable=self.segmenter.segment_time_label_var, font=('Helvetica', 12))
        segment_time_label.grid(row=14, column=1, columnspan=4, pady=5)
    def setup_list(self):
        '''Setups list for displaying segments time'''
        self.segment_list = tk.Listbox(self, selectmode=tk.BROWSE, font=('Helvetica', 10), width=50, height=20)
        self.segment_list.grid(row=2, column=1, columnspan=1, padx=3, pady=10, rowspan=10)

### Update
    def update_segment_list(self):
        '''Updates list of segments by clearin whole list and filling it again'''
        self.segment_list.delete(0, tk.END) 
        i = 0
        for line in self.segmenter.curent_run_lines:
            time_stamp = self.segmenter.make_line(line, i)
            self.segment_list.insert(tk.END, time_stamp)
            i += 1
    def update_labels(self):
        '''Updates labels'''
        current_time = self.segmenter.get_curent_time()
        segment_time = self.segmenter.get_segment_time()

        self.segmenter.current_time_label_var.set(f"Current Time: {current_time}")
        self.segmenter.segment_time_label_var.set(f"Segment Time: {segment_time}")
        self.update_segment_list()
        
        self.after(10, self.update_labels) #updates every 10 miliseconds

if __name__ == "__main__":
    app = GUI()
    