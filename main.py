import tkinter as tk
from tkinter import filedialog
from Solve_stages import *
from Text_stages import *
from Analysis_stages import *
from Output import *

root = tk.Tk()
root.title("Cipher program")
root.geometry("1500x500")
root.state("zoomed") #apparently windows only

def getOutputText():
    text = ""
    for stage in stages:
        if stage.check_var.get():
            if decode_var.get() == 1: #encode is selected
                text = stage.encode(text)
            else: #decode is selected
                text = stage.decode(text)
    return text
def updateOutputText():
    text = getOutputText()
    right_text.delete(1.0, tk.END)
    right_text.insert(tk.END,text)
    for stage in stages:
        if stage.check_var.get():
            stage.updateOutputWidget(text, right_text)

def updateStageEditor():
    for child in stage_editor.winfo_children():
        child.grid_forget()
    stages[selected_stage.get()].display()
    root.focus_set()
stage_editor = tk.Frame(root, width=10, height=10)#Size is the same as right_text, they will expand equally to fill the space
stage_editor.grid(row=0, column=0, rowspan=4, sticky="NESW")
stage_editor.grid_propagate(0) #stops the contents of the window affecting the size

stages = []
def addStage(stage):
    stages.append(stage)
    updateStagesFrame()
    stages[len(stages)-1].button.select() #select the newly added stage
    updateStageEditor()
    updateOutputText()
selected_stage = tk.IntVar()
stages_frame = tk.Frame(root)
stages_frame.grid(row=0, column=1, sticky="NS", columnspan=3)

#Radiobuttons to select between encode and decode
decode_var = tk.IntVar()
decodeBox = tk.Radiobutton(root, text="Decode", variable=decode_var,value=-1,command=updateOutputText)
encodeBox = tk.Radiobutton(root, text="Encode", variable=decode_var,value=1,command=updateOutputText)
decode_var.set(-1) #set to decode as default
decodeBox.grid(row=1,column=1,columnspan=3)
encodeBox.grid(row=2,column=1,columnspan=3)

#Up, Delete, and Down buttons
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
stage_up_button.grid(row=3, column=1, sticky="ESW")
stage_delete_button.grid(row=3,column=2, sticky="ESW")
stage_down_button.grid(row=3, column=3, sticky="ESW")

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


right_text = tk.Text(root, takefocus=0, width=10, height=10, font=("Courier", 10))
right_text.grid(row=0, column=4, rowspan=4, sticky="NESW")
right_text.grid_propagate(0)

tk.Grid.columnconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 1, weight=0)
tk.Grid.columnconfigure(root, 2, weight=0)
tk.Grid.columnconfigure(root, 3, weight=0)
tk.Grid.columnconfigure(root, 4, weight=1)
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.rowconfigure(root, 1, weight=0)
tk.Grid.columnconfigure(stage_editor, 0, weight=1)
tk.Grid.rowconfigure(stage_editor, 0, weight=1)

#==========
def add(menu, StageClass): #Helper function to make adding stages neater
    menu.add_command(label= StageClass.name,#Takes the name from the class
                     command=lambda:addStage(StageClass(stage_editor, #passes the stage editor frame to draw to
                                                        updateOutputText))) #and a callback for when things change and the output text needs updating
#Functions for file menu operations:
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

ana_menu = tk.Menu(menu, tearoff=0)
add(ana_menu, Length)
add(ana_menu, PlayfairDetect)
add(ana_menu, FrequencyAnalyse)
add(ana_menu, Doubles)
add(ana_menu, Triples)
add(ana_menu, IoC)
add(ana_menu, WordFinder)
add(ana_menu, VigenereKeyword)
menu.add_cascade(label="Analyse", menu=ana_menu)

text_menu = tk.Menu(menu, tearoff=0)
add(text_menu, Capitalise)
add(text_menu, Lowercase)
add(text_menu, Swapcase)
add(text_menu, Strip)
add(text_menu, RemoveSpaces)
add(text_menu, Reverse)
add(text_menu, Block)
menu.add_cascade(label="Text stage", menu=text_menu)

solve_menu = tk.Menu(menu, tearoff=0)
add(solve_menu, CaesarShift)
add(solve_menu, Substitution)
add(solve_menu, Affine)
add(solve_menu, Vigenere)
#add(solve_menu, Transposition) #this one doesn't work
add(solve_menu, Morse)
menu.add_cascade(label="Solve stage", menu=solve_menu)

#Functions for the output menu operations
def changeFontSize(change):
    currentSize = int(right_text.cget("font").split(" ")[1])
    right_text.config(font=("Courier", currentSize + change))
    stages[0].textbox.config(font=("Courier", currentSize + change))
output_menu = tk.Menu(menu, tearoff=0)
add(output_menu, OutputHighlight)
add(output_menu, Blank)
output_menu.add_command(label="Increase font size", command=lambda:changeFontSize(1))
output_menu.add_command(label="Decrease font size", command=lambda:changeFontSize(-1))

right_text.tag_configure("highlight", foreground = "red")
menu.add_cascade(label="Output", menu=output_menu)

root.config(menu=menu)

addStage(Input(stage_editor, updateOutputText))

root.mainloop()
