import tkinter as tk
import Constants
from Constants import Stage, register
from typing import Callable


@register("Text stage")
class Capitalise(Stage):
    name = "Capitalise"
    def __init__(self, frame, updateFunction):
        super().__init__(frame, updateFunction)
    def decode(self, text: str) -> str:
        return text.upper()

@register("Text stage")
class Lowercase(Stage):
    name = "Lower Case"
    def decode(self, text: str) -> str:
        return text.lower()

@register("Text stage")
class Swapcase(Stage):
    name = "Swap case"
    def decode(self, text: str) -> str:
        return text.swapcase()

@register("Text stage")
class Block(Stage):
    name = "Block text"
    def __init__(self, frame, updateFunction):
        self.updateFunction = updateFunction
        self.input_var = tk.IntVar(value=5)
        self.n_input = tk.Entry(frame, width=5, textvariable = self.input_var)
        Constants.writeTrace(self.input_var, lambda a, b, c, self=self : self.updateFunction())
    def decode(self, text: str) -> str:
        n = self.input_var.get()
        #if n.isnumeric():
        return " ".join([text[i:i+n] for i in range(0, len(text), n)])
        #else: #add status bar message here
        #    return text

@register("Text stage")
class Strip(Stage):
    name = "Strip punctuation"
    def decode(self, text: str) -> str:
        stripped: str = ""
        for character in text:
            if character.upper() in Constants.alphabet or character == " ":
                stripped += character
        return stripped

@register("Text stage")
class RemoveSpaces(Stage):
    name = "Remove Spaces"
    def decode(self, text: str) -> str:
        removed: str = ""
        for character in text:
            if character != " ":
                removed += character
        return removed

@register("Text stage")
class Reverse(Stage):
    name = "Reverse"
    def decode(self, text: str) -> str:
        return text.rstrip("\n")[::-1]
