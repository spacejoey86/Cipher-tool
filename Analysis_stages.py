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
class PlayfairDetect(Stage):
    name = "Detect Playfair"
    output = None
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.output = tk.Label(frame, text="")
    def display(self):
        self.output.grid()
    def process(self, text):
        doubles = False
        for i in range(len(text)//2):
            if text[i] == text[i+1]:
                doubles = True
                break
        if doubles:
            self.output.configure(text="Doubles found, this isn't a Playfair cipher")
        else:
            self.output.configure(text="Doubles not found, this could be a Playfair cipher")
        return text
class FrequencyAnalyse(Stage):
    name = "Frequency analysis"
    output = None
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.output = tk.Label(frame, text="")
    def display(self):
        self.output.grid()
    def process(self, text):
        frequency = {}
        for letter in set(text):
            frequency[letter] = round(text.count(letter)/len(text)*100, 2)
        output_text = ""
        for letter in sorted(frequency, key=frequency.__getitem__, reverse=True):
            output_text += letter + " = " + str(frequency[letter]) + "\n"
        self.output.configure(text=output_text)
        return text
class Doubles(Stage):
    name = "Bigram frequencies"
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.frame2 = tk.Frame(frame)
        self.canvas = tk.Canvas(self.frame2)
        self.scroll = tk.Scrollbar(self.frame2, orient="vertical", command=self.canvas.yview)
        self.output = tk.Label(self.canvas, text="")
        self.output.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.output, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
    def display(self):
        self.frame2.grid()
        self.canvas.grid()
        self.scroll.grid()
    def process(self, text):
        frequency = {}
        for letter in set(text[i]+text[i+1] for i in range(len(text)-1)):
            frequency[letter] = round(text.count(letter)/len(text)*100, 2)
        output_text = ""
        for letter in sorted(frequency, key=frequency.__getitem__, reverse=True):
            output_text += letter + " = " + str(frequency[letter]) + "\n"
        self.output.configure(text=output_text)
        return text
