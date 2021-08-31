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
text_menu.add_command(label="Capitalise", command=lambda:[stages.append(Capitalise()),updateStagesFrame()])
text_menu.add_command(label="Remove spaces", command=lambda:[stages.append(RemoveSpaces()),updateStagesFrame()])
text_menu.add_command(label="Reverse", command=lambda:[stages.append(Reverse()),updateStagesFrame()])
menu.add_cascade(label="Text stage", menu=text_menu)
solve_menu = tk.Menu(menu, tearoff=0)
solve_menu.add_command(label="Caesar Shift", command=lambda:[stages.append(CaesarShift()),updateStagesFrame()])
solve_menu.add_command(label="Substitution", command=lambda:[stages.append(Substitution()),updateStagesFrame()])
solve_menu.add_command(label="Affine", command=lambda:[stages.append(Affine()),updateStagesFrame()])
solve_menu.add_command(label="Viginere", command=lambda:[stages.append(Viginere()),updateStagesFrame()])
solve_menu.add_command(label="Transposition", command=lambda:[stages.append(Transposition()),updateStagesFrame()])
menu.add_cascade(label="Solve stage", menu=solve_menu)
root.config(menu=menu)

stage_editor = tk.Frame(root)
stage_editor.grid(row=0, column=0)

#stages list
stages = [Input()]
selected_stage = tk.IntVar()
stages_frame = tk.Frame(root)
stages_frame.grid(row=0, column=1, sticky="NS")
def updateStagesFrame():
    for button in stages_frame.winfo_children():
      button.destroy()
    for stage_index in range(len(stages)):
        stage = stages[stage_index]
        stage.button = tk.Radiobutton(stages_frame, text=stage.name, variable = selected_stage, value = stage_index,
                                      indicatoron = 0, width = 20)
        stage.button.grid()
updateStagesFrame()


right_text = tk.Text(root)
right_text.grid(row=0, column=2)
