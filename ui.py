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
stage_editor.grid(row=0, column=0, rowspan=2, sticky="NESW")

stages = []
def addStage(stage):
    stages.append(stage)
    updateStagesFrame()
    stages[len(stages)-1].button.select()
    updateStageEditor()
    updateOutputText()
selected_stage = tk.IntVar()
stages_frame = tk.Frame(root)
stages_frame.grid(row=0, column=1, sticky="NS", columnspan=3)
def stageUp():
    if len(stages) > 1 and selected_stage.get() > 1:
        stages.insert(selected_stage.get()-1, stages.pop(selected_stage.get()))
        selected_stage.set(selected_stage.get()-1)
        updateStagesFrame()
        updateOutputText()
def stageDown():
    if len(stages) > 1 and selected_stage.get() < len(stages)-1 and selected_stage.get() != 0:
        stages.insert(selected_stage.get()+1, stages.pop(selected_stage.get()))
        selected_stage.set(selected_stage.get()+1)
        updateStagesFrame()
        updateOutputText()
def deleteStage():
    if len(stages) > 1 and selected_stage.get() != 0:
        stages.pop(selected_stage.get())
        selected_stage.set(selected_stage.get()-1)
        updateStagesFrame()
        updateStageEditor()
        updateOutputText()
stage_up_button = tk.Button(root, text = "↑",command=stageUp,takefocus=0)
stage_delete_button = tk.Button(root, text = "×",command=deleteStage,takefocus=0)
stage_down_button = tk.Button(root, text = "↓",command=stageDown,takefocus=0)
stage_up_button.grid(row=1, column=1, sticky="ESW")
stage_delete_button.grid(row=1,column=2, sticky="ESW")
stage_down_button.grid(row=1, column=3, sticky="ESW")

def updateStagesFrame():
    for button in stages_frame.winfo_children():
        button.destroy()
    for stage_index in range(len(stages)):
        stage = stages[stage_index]
        stage.button = tk.Radiobutton(stages_frame, text=stage.name, variable = selected_stage, value = stage_index, command=updateStageEditor,
                                      indicatoron = 0, width = 20, takefocus=0)
        stage.button.grid()
updateStagesFrame()

def updateOutputText():
    text = ""
    for stage in stages:
        text = stage.process(text)
    right_text.delete(1.0, tk.END)
    right_text.insert(tk.END,text)
right_text = tk.Text(root, takefocus=0)
right_text.grid(row=0, column=4, rowspan=2, sticky="NESW")

tk.Grid.columnconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 4, weight=1)
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.rowconfigure(root, 1, weight=1)
#tk.Grid.columnconfigure(stage_editor, 0, weight=1)
#tk.Grid.rowconfigure(stage_editor, 0, weight=1)

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
text_menu.add_command(label="Lowercase", command=lambda:addStage(Lowercase(stage_editor, updateOutputText)))
text_menu.add_command(label="Swap case", command=lambda:addStage(Swapcase(stage_editor, updateOutputText)))
text_menu.add_command(label="Strip punctuation", command=lambda:addStage(Strip(stage_editor, updateOutputText)))
text_menu.add_command(label="Remove spaces", command=lambda:addStage(RemoveSpaces(stage_editor, updateOutputText)))
text_menu.add_command(label="Reverse", command=lambda:addStage(Reverse(stage_editor, updateOutputText)))
menu.add_cascade(label="Text stage", menu=text_menu)
solve_menu = tk.Menu(menu, tearoff=0)
solve_menu.add_command(label="Caesar Shift", command=lambda:addStage(CaesarShift(stage_editor, updateOutputText)))
solve_menu.add_command(label="Substitution", command=lambda:addStage(Substitution(stage_editor, updateOutputText)))
solve_menu.add_command(label="Affine", command=lambda:addStage(Affine(stage_editor, updateOutputText)))
solve_menu.add_command(label="Viginere", command=lambda:addStage(Vigenere(stage_editor, updateOutputText)))
solve_menu.add_command(label="Transposition", command=lambda:addStage(Transposition(stage_editor, updateOutputText)))
menu.add_cascade(label="Solve stage", menu=solve_menu)
root.config(menu=menu)

addStage(Input(stage_editor, updateOutputText))
