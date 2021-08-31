import tkinter as tk
from Stages import *

root = tk.Tk()
root.title("Cipher program")

menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Open")
file_menu.add_command(label="Clear")
file_menu.add_command(label="Save")
file_menu.add_command(label="Copy output")
menu.add_cascade(label="File", menu = file_menu)
ana_menu = tk.Menu(menu, tearoff=0)#Menu to toggle the stastical analysis shown at the bottom of display boxes
ana_menu.add_checkbutton(label="Length")
ana_menu.add_checkbutton(label="Frequency analysis")
ana_menu.add_checkbutton(label="Index of Coincidence")
ana_menu.add_checkbutton(label="Bigrams")
menu.add_cascade(label="Analyse", menu=ana_menu)
text_menu = tk.Menu(menu, tearoff=0)
text_menu.add_command(label="Capitalise")
text_menu.add_command(label="Remove spaces")
text_menu.add_command(label="Reverse")
menu.add_cascade(label="Text stage", menu=text_menu)
solve_menu = tk.Menu(menu, tearoff=0)
solve_menu.add_command(label="Caesar Shift")
solve_menu.add_command(label="Substitution")
solve_menu.add_command(label="Affine")
solve_menu.add_command(label="Viginere")
solve_menu.add_command(label="Transposition")
menu.add_cascade(label="Solve stage", menu=solve_menu)
root.config(menu=menu)

stage_editor = tk.Frame(root)
stage_editor.grid(row=0, column=0)

#stages list
def updateStagesFrame():
    for stage in stages:
        print(stage.name)
        stage.button = tk.Radiobutton(stages_frame, text=stage.name, indicatoron = 0, width = 20, padx = 20).pack()

stages = [Input()]
stages_frame = tk.Frame(root)
updateStagesFrame()
stages_frame.grid(row=0, column=1)



right_text = tk.Text(root)
right_text.grid(row=0, column=1)
