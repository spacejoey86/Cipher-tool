import tkinter as tk
import Constants
from Constants import Stage, register
from typing import Callable

@register("Output")
class OutputHighlight(Stage):
    name = "Highlight"
    def __init__(self, frame: tk.Frame, updateFunction: Callable[[], None]):
        self.updateFunction = updateFunction
        self.frame = frame
        self.textVar = tk.StringVar()
        Constants.writeTrace(self.textVar, self.update)
        self.textBox = tk.Entry(frame, width=20, textvariable=self.textVar)
    def update(self, a, b, c):
        self.updateFunction()
    def updateOutputWidget(self, text: str, textRef: tk.Text):
        word = self.textVar.get()
        countVar = tk.IntVar()
        start = "1.0"
        while True:
            pos = textRef.search(word, start, stopindex="end", count=countVar)
            #print(pos)
            if pos == "" or countVar == 0: #not found
                break
            line = pos.split(".")[0]
            char = pos.split(".")[1]
            index2 = line + "." + str(int(char)+len(word))
            if start == index2: #don't get stuck in a loop
                break
            start = index2
            textRef.tag_add("highlight", pos, index2)
    def display(self):
        self.textBox.grid()

@register("Output")
class Blank(Stage):
    name = "Blank"
    def decode(self, text: str) -> str:
        blanked = ""
        for character in text:
            if character.upper() == character:
                blanked += " "
            else:
                blanked += character
        return blanked
