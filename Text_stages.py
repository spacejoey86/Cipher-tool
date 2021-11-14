import tkinter as tk
import Constants
from Constants import Stage

class Input(Stage):
    name = "Input"
    textbox = None
    frame = None
    def onModify(self, event):
        try:
            self.textbox.tk.call(self.textbox._w, 'edit', 'modified', 0)
        finally:
            self.updateFunction()
    def __init__(self, frame, updateFunction):
        self.updateFunction = updateFunction
        self.frame = frame
        self.textbox = tk.Text(frame)
        self.textbox.bind('<<Modified>>',self.onModify)
    def display(self):
        self.textbox.grid(sticky="NSEW")
        tk.Grid.rowconfigure(self.frame, 0, weight=1)
        tk.Grid.columnconfigure(self.frame, 0, weight=1)
    def decode(self, text):
        return self.textbox.get("1.0",tk.END).rstrip("\n")
class Capitalise(Stage):
    name = "Capitalise"
    def decode(self, text):
        return text.upper()
class Lowercase(Stage):
    name = "Lower Case"
    def decode(self, text):
        return text.lower()
class Swapcase(Stage):
    name= "Swap case"
    def decode(self, text):
        return text.swapcase()
class Strip(Stage):
    name = "Strip punctuation"
    def decode(self, text):
        stripped = ""
        for character in text:
            if character.upper() in Constants.alphabet or character == " ":
                stripped += character
        return stripped
class RemoveSpaces(Stage):
    name = "Remove Spaces"
    def decode(self, text):
        removed = ""
        for character in text:
            if character != " ":
                removed += character
        return removed
class Reverse(Stage):
    name = "Reverse"
    def decode(self, text):
        return text.rstrip("\n")[::-1]
