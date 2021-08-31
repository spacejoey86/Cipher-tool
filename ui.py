import tkinter as tk

root = tk.Tk()
root.title("Cipher program")

menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Open")
file_menu.add_command(label="Clear")
file_menu.add_command(label="Save")
file_menu.add_command(label="Copy output")
ana_menu = tk.Menu(menu, tearoff=0)#Menu to toggle the stastical analysis shown at the bottom of display boxes
ana_menu.add_checkbutton(label="Length")
ana_menu.add_checkbutton(label="Frequency analysis")
ana_menu.add_checkbutton(label="Index of Coincidence")
ana_menu.add_checkbutton(label="Bigrams")
text_menu = tk.Menu(menu, tearoff=0)
text_menu.add_command(label="Capitalise")
text_menu.add_command(label="Remove spaces")
text_menu.add_command(label="Reverse")
solve_menu = tk.Menu(menu, tearoff=0)
solve_menu.add_command(label="Caesar Shift")
solve_menu.add_command(label="Substitution")
solve_menu.add_command(label="Affine")
solve_menu.add_command(label="Viginere")
solve_menu.add_command(label="Transposition")


menu.add_cascade(label="File", menu = file_menu)
menu.add_cascade(label="Analyse", menu=ana_menu)
menu.add_cascade(label="Text stage", menu=text_menu)
menu.add_cascade(label="Solve stage", menu=solve_menu)
root.config(menu=menu)
