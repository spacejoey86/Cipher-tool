import tkinter as tk
import constants
from Stages import Stage

class Length(Stage):
    name = "Length"
    output = None
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.output = tk.Label(frame, text="")
    def display(self):
        self.output.grid()
    def process(self, text):
        self.output.configure(text="Length = " + str(len(text)))
        return text
