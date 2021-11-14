import tkinter as tk
from Constants import Stage

class OutputHighlight(Stage):
    name = "Highlight"
    def __init__(self, frame, updateFunction):
        self.updateFunction = updateFunction
        self.frame = frame
        self.textVar = tk.StringVar()
        self.textVar.trace_add("write", self.update)
        self.textBox = tk.Entry(frame, width=20, textvariable=self.textVar)
    def update(self, a, b, c):
        self.updateFunction()
    def updateOutputWidget(self, text, textRef):
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
class Blank(Stage):
    name = "Blank"
    def decode(self, text):
        blanked = ""
        for character in text:
            if character.upper() == character:
                blanked += " "
            else:
                blanked += character
        return blanked
