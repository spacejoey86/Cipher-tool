import tkinter as tk
from Stages import *

root = tk.Tk()
root.title("Cipher program")

def updateStageEditor():
    for child in stage_editor.winfo_children():
        child.grid_forget()
    stages[selected_stage.get()].display()
    root.focus_set()
stage_editor = tk.Frame(root)
stage_editor.grid(row=0, column=0)

stages = []
def addStage(stage):
    stages.append(stage)
    updateStagesFrame()
    stages[len(stages)-1].button.select()
    updateStageEditor()
    updateOutputText()
selected_stage = tk.IntVar()
stages_frame = tk.Frame(root)
stages_frame.grid(row=0, column=1, sticky="NS")
def updateStagesFrame():
    for button in stages_frame.winfo_children():
        button.destroy()
    for stage_index in range(len(stages)):
        stage = stages[stage_index]
        stage.button = tk.Radiobutton(stages_frame, text=stage.name, variable = selected_stage, value = stage_index, command=updateStageEditor,
                                      indicatoron = 0, width = 20)
        stage.button.grid()
updateStagesFrame()

def updateOutputText():
    text = ""
    for stage in stages:
        text = stage.process(text)
    right_text.delete(1.0, tk.END)
    right_text.insert(tk.END,text)
right_text = tk.Text(root)
right_text.grid(row=0, column=2)

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
text_menu.add_command(label="Capitalise", command=lambda:addStage(Capitalise(stage_editor, updateOutputText)))
text_menu.add_command(label="Strip punctuation", command=lambda:addStage(Strip(stage_editor, updateOutputText)))
text_menu.add_command(label="Remove spaces", command=lambda:addStage(RemoveSpaces(stage_editor, updateOutputText)))
text_menu.add_command(label="Reverse", command=lambda:addStage(Reverse(stage_editor, updateOutputText)))
menu.add_cascade(label="Text stage", menu=text_menu)
solve_menu = tk.Menu(menu, tearoff=0)
solve_menu.add_command(label="Caesar Shift", command=lambda:addStage(CaesarShift(stage_editor, updateOutputText)))
solve_menu.add_command(label="Substitution", command=lambda:addStage(Substitution(stage_editor, updateOutputText)))
solve_menu.add_command(label="Affine", command=lambda:addStage(Affine(stage_editor, updateOutputText)))
solve_menu.add_command(label="Viginere", command=lambda:addStage(Viginere(stage_editor, updateOutputText)))
solve_menu.add_command(label="Transposition", command=lambda:addStage(Transposition(stage_editor, updateOutputText)))
menu.add_cascade(label="Solve stage", menu=solve_menu)
root.config(menu=menu)

addStage(Input(stage_editor, updateOutputText))
