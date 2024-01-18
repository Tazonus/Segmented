import tkinter as tk
from tkinter import ttk
import Segmenter_file as seg
from pynput import keyboard



class SegmenterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.segmenter = seg.Segmenter()
        listener = keyboard.Listener(on_press=self.keyPressed,on_release=self.keyReleased)
        listener.start()

        self.keyShortcuts = [("'s'","segment")]
        self.shortcutBuffor = ""

        self.setup()
        #Main loop:
        self.update_labels()
        self.root.mainloop()
        

### INPUT HANDLING ###
    def keyReleased(self,key):
        character = str(key)
        self.shortcutBuffor = self.shortcutBuffor.replace(character, '')
        
    def keyPressed(self,key):
        self.shortcutBuffor += str(key)

        if 'Key.ctrl' in self.shortcutBuffor and 'Key.alt' in self.shortcutBuffor:
            for x in self.keyShortcuts:
                if self.shortcutBuffor.find(x[0]) > 0:
                    self.handle_button_click(x[1])

#Handles button click
    def handle_button_click(self, action):
        if action == "segment":
            self.segmenter.segment()
        elif action == "stop":
            self.segmenter.stop()
        elif action == "reset":
            self.segmenter.reset()
        elif action == "exit":
            self.root.destroy()  

### GRAPHICAL INTERFACE ###
    def setup(self):
        self.root.title("SegmentDead")
        self.root.geometry("500x450")

        #Label displaying title
        self.title_var = tk.StringVar()
        self.title_var.set(self.segmenter.title)
        title_label = ttk.Label(self.root, textvariable=self.title_var, font=('Helvetica', 18))
        title_label.grid(row=0, column=1, columnspan=1000, pady= [8,0])

        #Label displaying category
        self.category_var = tk.StringVar()
        self.category_var.set(self.segmenter.category)
        category_label = ttk.Label(self.root, textvariable=self.category_var, font=('Helvetica', 12))
        category_label.grid(row=1, column=1, columnspan=1000)

        #Buttons for different actions
        buttons = [
            ("Segment", "segment"),
            ("Stop", "stop"),
            ("Reset", "reset"),
            ("Exit", "exit")
        ]
        for i, (text, action) in enumerate(buttons):
            button = ttk.Button(self.root, text=text, command=lambda a=action: self.handle_button_click(a))
            button.grid(row=i + 2, column=0, pady=5)

        #List displaying split times
        self.segment_list = tk.Listbox(self.root, selectmode=tk.BROWSE, font=('Helvetica', 10), width=50, height=20)
        self.segment_list.grid(row=2, column=3, columnspan=1, padx=3, pady=10, rowspan=10)
        
        #Label displaying current time
        self.segmenter.current_time_label_var = tk.StringVar()
        current_time_label = ttk.Label(self.root, textvariable=self.segmenter.current_time_label_var, font=('Helvetica', 16))
        current_time_label.grid(row=13, column=1, columnspan=4, pady=5)

        #Label displaying time since the last segment(not split)
        self.segmenter.segment_time_label_var = tk.StringVar()
        segment_time_label = ttk.Label(self.root, textvariable=self.segmenter.segment_time_label_var, font=('Helvetica', 12))
        segment_time_label.grid(row=14, column=1, columnspan=4, pady=5)

#Updates list of segmments
#by clearing whole list and filling it again
    def update_segment_list(self):
        self.segment_list.delete(0, tk.END) 
        i = 0
        for line in self.segmenter.curent_run_lines:
            time_stamp = self.segmenter.make_line(line, i)
            self.segment_list.insert(tk.END, time_stamp)
            i += 1

#Updates labels
#loops via self-invocation, loop end when root.destroy() is invoked
    def update_labels(self):
        current_time = self.segmenter.get_curent_time()
        segment_time = self.segmenter.get_segment_time()

        self.segmenter.current_time_label_var.set(f"Current Time: {current_time}")
        self.segmenter.segment_time_label_var.set(f"Segment Time: {segment_time}")
        self.update_segment_list()
        
        self.root.after(10, self.update_labels) #updates every 10 miliseconds

if __name__ == "__main__":
    app = SegmenterGUI()
    
