import tkinter as tk
import constants

class Stage:
    name = "stage name"
    button = None
    update_function = None
    def __init__(self, frame, updateFunction):
        update_function = updateFunction
    def process(self, text):
        return text
    def display(self):
        pass

class Input(Stage):
    name = "Input"
    textbox = None
    def onModify(self, blah):
        try:
            self.textbox.tk.call(self.textbox._w, 'edit', 'modified', 0)
        finally:
            self.updateFunction()
    def __init__(self, frame, updateFunction):
        self.updateFunction = updateFunction
        self.textbox = tk.Text(frame)
        self.textbox.bind('<<Modified>>',self.onModify)
    def display(self):
        self.textbox.grid()
    def process(self, text):
        return self.textbox.get("1.0",tk.END)
class Output(Stage):
    name = "Output"
    def process(self, text):
        print(text)
    
class Capitalise(Stage):
    name = "Capitalise"
    def process(self, text):
        return text.upper()
class Strip(Stage):
    name = "Strip punctuation"
    def process(self, text):
        stripped = ""
        for character in text:
            if character.upper() in constants.alphabet or character == " ":
                stripped += character
        return stripped
class RemoveSpaces(Stage):
    name = "Remove Spaces"
    def process(self, text):
        removed = ""
        for character in text:
            if character != " ":
                removed += character
        return removed
class Reverse(Stage):
    name = "Reverse"
    def process(self, text):
        return text.rstrip("\n")[::-1]

class CaesarShift(Stage):
    name = "Caesar shift"
class Substitution(Stage):
    name = "Substitution"
class Affine(Stage):
    name = "Affine"
class Viginere(Stage):
    name = "Viginere"
class Transposition(Stage):
    name = "Transposition"
