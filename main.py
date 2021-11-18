import tkinter as tk
from tkinter import filedialog
from Solve_stages import *
from Text_stages import *
from Analysis_stages import *

root = tk.Tk()
root.title("Cipher program")
root.geometry("1500x500")
root.state("zoomed") #apparently windows only

def updateStageEditor():
    for child in stage_editor.winfo_children():
        child.grid_forget()
    stages[selected_stage.get()].display()
    root.focus_set()
stage_editor = tk.Frame(root, width=10, height=10)#Size is the same as right_text, they will expand equally to fill the space
stage_editor.grid(row=0, column=0, rowspan=2, sticky="NESW")
stage_editor.grid_propagate(0) #stops the contents of the window affecting the size

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

#Shortcuts for selecting the next and previous stage
def stageSelectUp(event):
    if selected_stage.get() > 0:
        selected_stage.set(selected_stage.get()-1)
    updateStagesFrame()
    updateStageEditor()
def stageSelectDown(event):
    if selected_stage.get() < len(stages) - 1:
        selected_stage.set(selected_stage.get()+1)
    updateStagesFrame()
    updateStageEditor()
root.bind("<Control-Tab>", stageSelectUp)
root.bind("<Control-Shift-Tab>", stageSelectDown)
root.bind("<Control-Prior>", stageSelectUp)     #Control + page up
root.bind("<Control-Next>", stageSelectDown)    #Control + page down


def updateStagesFrame():
    for button in stages_frame.winfo_children():
        button.destroy()
    for stage_index in range(len(stages)):
        stage = stages[stage_index]
        stage.button = tk.Radiobutton(stages_frame, text=stage.name, variable = selected_stage, value = stage_index, command=updateStageEditor,
                                      indicatoron = 0, width = 20, takefocus=0)
        stage.check_var = tk.BooleanVar()
        stage.check_var.set(True)
        stage.checkbox = tk.Checkbutton(stages_frame, variable = stage.check_var, command=updateOutputText, takefocus=0)
        
        if stage_index == 0: #Input cannot be disabled, so don't show the checkbox
            stage.checkbox.config(state="disabled")
        stage.button.grid(column=1, row=stage_index)
        stage.checkbox.grid(column=0, row=stage_index)
updateStagesFrame()

def getOutputText():
    text = ""
    for stage in stages:
        if stage.check_var.get():
            text = stage.process(text)
    return text
def updateOutputText():
    text = getOutputText()
    right_text.delete(1.0, tk.END)
    right_text.insert(tk.END,text)
right_text = tk.Text(root, takefocus=0, width=10, height=10)
right_text.grid(row=0, column=4, rowspan=2, sticky="NESW")

tk.Grid.columnconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 1, weight=0)
tk.Grid.columnconfigure(root, 2, weight=0)
tk.Grid.columnconfigure(root, 3, weight=0)
tk.Grid.columnconfigure(root, 4, weight=1)
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.rowconfigure(root, 1, weight=0)
tk.Grid.columnconfigure(stage_editor, 0, weight=1)
tk.Grid.rowconfigure(stage_editor, 0, weight=1)

def openCom():
    text = ""
    try:
        with filedialog.askopenfile() as file:
            for line in file:
                text += line
        stages[0].textbox.delete(1.0, tk.END)
        stages[0].textbox.insert(tk.END,text)
    except AttributeError:#Catch error if the user cancels the dialog
        pass
def clearCom():
    global stages
    stages[0].textbox.delete(1.0, tk.END)
    stages = [stages[0]]
    selected_stage.set(0)
    updateStageEditor()
    updateStagesFrame()
    #updateOutputText()
def saveCom():
    text = getOutputText()
    try:
        with filedialog.asksaveasfile() as file:
            file.write(text)
    except AttributeError:
        pass
def copyCom():
    text = ""
    for stage in stages:
        text = stage.process(text)
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Open", command=openCom)
file_menu.add_command(label="Clear", command = clearCom)
file_menu.add_command(label="Save", command=saveCom)
file_menu.add_command(label="Copy output", command=copyCom)
menu.add_cascade(label="File", menu = file_menu)
ana_menu = tk.Menu(menu, tearoff=0)#Menu to toggle the stastical analysis shown at the bottom of display boxes
ana_menu.add_command(label="Length", command=lambda:addStage(Length(stage_editor, updateOutputText)))
ana_menu.add_command(label="Playfair", command=lambda:addStage(PlayfairDetect(stage_editor, updateOutputText)))
ana_menu.add_command(label="Frequency analysis", command=lambda:addStage(FrequencyAnalyse(stage_editor, updateOutputText)))
#ana_menu.add_checkbutton(label="Index of Coincidence")
ana_menu.add_command(label="Bigram frequencies", command=lambda:addStage(Doubles(stage_editor, updateOutputText)))
ana_menu.add_command(label="Word finder", command=lambda:addStage(WordFinder(stage_editor, updateOutputText)))
ana_menu.add_command(label="Vigenere keyword length", command=lambda:addStage(VigenereKeyword(stage_editor, updateOutputText)))
menu.add_cascade(label="Analyse", menu=ana_menu)
text_menu = tk.Menu(menu, tearoff=0)
text_menu.add_command(label="Capitalise", command=lambda:addStage(Capitalise(stage_editor, updateOutputText)))
text_menu.add_command(label="Lowercase", command=lambda:addStage(Lowercase(stage_editor, updateOutputText)))
text_menu.add_command(label="Swap case", command=lambda:addStage(Swapcase(stage_editor, updateOutputText)))
text_menu.add_command(label="Strip punctuation", command=lambda:addStage(Strip(stage_editor, updateOutputText)))
text_menu.add_command(label="Remove spaces", command=lambda:addStage(RemoveSpaces(stage_editor, updateOutputText)))
text_menu.add_command(label="Reverse", command=lambda:addStage(Reverse(stage_editor, updateOutputText)))
text_menu.add_command(label="Blank", command=lambda:addStage(Blank(stage_editor, updateOutputText)))
menu.add_cascade(label="Text stage", menu=text_menu)
solve_menu = tk.Menu(menu, tearoff=0)
solve_menu.add_command(label="Caesar Shift", command=lambda:addStage(CaesarShift(stage_editor, updateOutputText)))
solve_menu.add_command(label="Substitution", command=lambda:addStage(Substitution(stage_editor, updateOutputText)))
solve_menu.add_command(label="Affine", command=lambda:addStage(Affine(stage_editor, updateOutputText)))
solve_menu.add_command(label="Viginere", command=lambda:addStage(Vigenere(stage_editor, updateOutputText)))
solve_menu.add_command(label="Partial Viginere", command=lambda:addStage(VigenerePartial(stage_editor, updateOutputText)))
solve_menu.add_command(label="Transposition", command=lambda:addStage(Transposition(stage_editor, updateOutputText)))
menu.add_cascade(label="Solve stage", menu=solve_menu)
root.config(menu=menu)

addStage(Input(stage_editor, updateOutputText))

root.mainloop()
