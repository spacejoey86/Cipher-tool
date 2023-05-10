import sys
import tkinter as tk
from typing import Callable, Any

alphabet: list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
inverses: list = {1:1,3:9,5:21,7:15,9:3,11:19,15:7,17:23,19:11,21:5,23:17,25:25}
a_values: list = [1,3,5,7,9,11,15,17,19,21,23,25]


def writeTrace(variable: tk.Variable, callback: Callable[[Any, Any, Any], Any]) -> None:
    if sys.version_info[1] < 6: #tkinter trace_add replaced trace_variable in v3.6
        variable.trace_variable("w", callback)
    else:
        variable.trace_add("write", callback)

class Stage:
    name: str = "stage name" #Set the name of your stage here
    def __init__(self, frame: tk.Frame, updateFunction: Callable[[], None]) -> None: #should create all the widgets with frame as root
        self.updateFunction = updateFunction #and save updateFunction, and frame if needed (needed when adding more widgets later)
    def decode(self, text: str) -> str: #This should always return some text. If there is an invalid input, it should return the original text without changes.
        return text
    def encode(self, text: str) -> str: #by default the same as decode (for text stages)
        return self.decode(text)
    def display(self) -> None: #should grid/pack the stage's widgets
        pass
    def updateOutputWidget(self, text: str, textRef: tk.Text) -> None: #called after all the text is processed, for changing text colours etc
        pass
