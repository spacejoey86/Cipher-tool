import tkinter as tk
from tkinter import ttk
import Constants
from Constants import Stage
import math #For ceiling function (round up)

class CaesarShift(Stage):
    name = "Caesar shift"
    shift = 1
    scale = None
    down_button = None
    up_button = None
    decode_var = None
    decode = None
    encode = None
    def __init__(self, frame, updateFunction):
        self.scale = tk.Scale(frame, from_=0,to=25,orient="horizontal",length=500,command=lambda idk:updateFunction())
        self.down_button = tk.Button(frame, text = " - ",command = lambda:self.scale.set(self.scale.get()-1))
        self.up_button = tk.Button(frame, text = " + ",command = lambda:self.scale.set(self.scale.get()+1))
        self.decode_var = tk.IntVar()
        self.decode = tk.Radiobutton(frame, text="Decode", variable=self.decode_var,value=-1,command=updateFunction)
        self.encode = tk.Radiobutton(frame, text="Encode", variable=self.decode_var,value=1,command=updateFunction)
        self.decode_var.set(-1)
        self.frame = frame
    def display(self):
        self.decode.grid(row=0, column=1, sticky="EN", padx=25)
        self.encode.grid(row=0, column=2, sticky="WN", padx=25)
        self.down_button.grid(row=1, column=0, sticky="NE")
        self.scale.grid(row=1, column=1, columnspan=2, sticky="NEW")
        self.up_button.grid(row=1, column=3, sticky="NW")
        tk.Grid.rowconfigure(self.frame, 0, weight=1)
        tk.Grid.rowconfigure(self.frame, 1, weight=1)
        tk.Grid.columnconfigure(self.frame, 0, weight=1)
        tk.Grid.columnconfigure(self.frame, 1, weight=1)
        tk.Grid.columnconfigure(self.frame, 2, weight=1)
        tk.Grid.columnconfigure(self.frame, 3, weight=1)
    def process(self, text):
        shifted = ""
        for letter in text:
            if letter.upper() in constants.alphabet:
                if letter == letter.upper():
                    shifted += constants.alphabet[((constants.alphabet.index(letter)+self.decode_var.get()*self.scale.get()+1)%26)-1]
                else:
                    shifted += constants.alphabet[((constants.alphabet.index(letter.upper())+self.decode_var.get()*self.scale.get()+1)%26)-1].lower()
            else:
                shifted += letter
        return shifted
class Substitution(Stage):
    name = "Substitution"
##    substitutions = {}
##    label_one = None
##    sub_entry_one = None
##    label_two = None
##    sub_entry_two = None
##    sub_button = None
    
##    label_three = None
##    rev_entry_one = None
##    label_four = None
##    rev_entry_two = None
##    rev_button = None
    sub_display = None
    def SE1S(self, event):#Functions to select the text in the entry widgets when they are tabbed to
        self.sub_entry_one.selection_range(0, tk.END)
    def SE2S(self, event):
        self.sub_entry_two.selection_range(0, tk.END)
    def substitute(self):
        s1 = self.sub_entry_one.get()
        s2 = self.sub_entry_two.get()
        if s1 in self.substitutions.keys():
            print(s1," has already been substituted")
            self.sub_button.bell(displayof=0)
        elif s2 in self.substitutions.values():
            print(s2," has already been found")
            self.sub_button.bell(displayof=0)
        elif s1 not in constants.alphabet + [x.lower() for x in constants.alphabet]:
            print("Only substitutions in the alphabet are allowed")
            self.sub_button.bell(displayof=0)
        elif len(s1) != 1 or len(s2) != 1:
            print("They must both be a single character")
            self.sub_button.bell(displayof=0)
        elif (s1 == s1.lower() and s2 == s2.lower()) or (s1 == s1.upper() and s2 == s2.upper()):
            print("Must substitute to a different case")
            self.sub_button.bell(displayof=0)
        elif (len(self.substitutions.keys()) > 0 and list(self.substitutions.keys())[0] == list(self.substitutions.keys())[0].lower() and s1 == s1.upper()) or (len(self.substitutions.keys()) > 0 and list(self.substitutions.keys())[0] == list(self.substitutions.keys())[0].upper() and s1 == s1.lower()):
            print("Substitions must all be one case")
            self.sub_button.bell(displayof=0)
        elif s1 == s2:
            print("They can't be the same")
            self.sub_button.bell(displayof=0)
        else:
            #print("Substituting ",s1," for ",s2)
            #print("Found ",inputText.count(s1))
            self.substitutions[s1] = s2
            self.updateFunction()
        self.displaySubs()
    def displaySubs(self):
        display_text = ""
        for letter in constants.alphabet + [x.lower() for x in constants.alphabet]:
            if letter in self.substitutions.keys():
                display_text = display_text + letter + " -> " + self.substitutions[letter] + "\n"
        self.sub_display.configure(text=display_text)
        self.updateFunction()
    def unSubstitute(self):
        s1 = self.sub_entry_one.get()
        s2 = self.sub_entry_two.get()
        if s1 == "":
            self.substitutions = {key:val for key, val in self.substitutions.items() if val != s2}
        elif s2 == "":
            self.substitutions = {key:val for key, val in self.substitutions.items() if key != s1}
        else:
            self.substitutions = {key:val for key, val in self.substitutions.items() if (key != s1) or (val != s2)}
        self.displaySubs()
    def __init__(self, frame, updateFunction):
        self.substitutions = {}
        self.label_one = tk.Label(frame, text="Substitute")
        self.sub_entry_one = tk.Entry(frame, width=3)
        self.sub_entry_one.bind("<FocusIn>",self.SE1S)
        self.label_two = tk.Label(frame, text="for")
        self.sub_entry_two = tk.Entry(frame, width=3)
        self.sub_entry_two.bind("<FocusIn>",self.SE2S)
        self.sub_button = tk.Button(frame, text="Substitute",command=self.substitute)
        self.rev_button = tk.Button(frame, text="Un-substitute",command=self.unSubstitute,takefocus=0)
        self.sub_display = tk.Label(frame,text="")
        self.updateFunction = updateFunction
    def display(self):
        self.label_one.grid(row=0,column=0)
        self.sub_entry_one.grid(row=0,column=1)
        self.label_two.grid(row=0,column=2)
        self.sub_entry_two.grid(row=0,column=3)
        self.sub_button.grid(row=0,column=4, padx=10)
        self.rev_button.grid(row=1,column=4, padx=10)
        self.sub_display.grid(row=0,column=5,rowspan=3)
    def process(self, text):
        #text2 = ""
        for key, value in self.substitutions.items():
            text = text.replace(key,value)
        return text
class Affine(Stage):
    name = "Affine"
    def __init__(self, frame, updateFunction):
        self.cycleButton = tk.Button(frame, text="Cycle",command=self.cycle)
        self.aLabel = tk.Label(frame, text="0")
        self.aScale = tk.Scale(frame,from_=1,to=12,orient="horizontal",length=300,command=self.update,showvalue=False)
        self.bLabel = tk.Label(frame, text="1")
        self.bScale = tk.Scale(frame,from_=0,to=25,orient="horizontal",length=300,command=self.update,showvalue=False)
        self.decode_var = tk.IntVar()
        self.decode = tk.Radiobutton(frame, text="Decode", variable=self.decode_var,value=1,command=updateFunction)
        self.encode = tk.Radiobutton(frame, text="Encode", variable=self.decode_var,value=0,command=updateFunction)
        self.decode_var.set(1)
        self.updateFunction = updateFunction
        self.update("blah")
    def display(self):
        self.decode.grid()
        self.encode.grid()
        self.cycleButton.grid()
        self.aLabel.grid()
        self.aScale.grid()
        self.bLabel.grid()
        self.bScale.grid()
    def cycle(self):
        if self.aScale.get() == 12:
            self.aScale.set(1)
            if self.bScale.get() == 25:
                self.bScale.set(0)
            else:
                self.bScale.set(self.bScale.get()+1)
        else:
            self.aScale.set(self.aScale.get()+1)
    def update(self, args):
        self.a = constants.a_values[self.aScale.get()-1]
        self.aLabel.config(text=self.a)
        self.ia = constants.inverses[self.a]
        self.b = self.bScale.get()
        self.bLabel.config(text=self.b)
        self.updateFunction()
        #print("a=",a)
        #print("ia=",ia)
        #print("b=",b)
    def process(self, text):
        inputText = text
        if self.decode_var.get():
            for letter in constants.alphabet:
                lNum = constants.alphabet.index(letter)
                rNum = constants.alphabet[((self.ia*(lNum-self.b))%26)].lower()
                inputText = inputText.replace(letter,rNum)
        else:
            for letter in constants.alphabet:
                lNum = constants.alphabet.index(letter)
                rNum = constants.alphabet[((self.a*lNum+self.b)%26)].upper()
                inputText = inputText.replace(letter.lower(),rNum)
        return inputText
class Vigenere(Stage):
    name = "Vigenere"
    def __init__(self, frame, updateFunction):
        self.keyVar = tk.StringVar()
        self.keyVar.trace_add("write", self.update)
        self.keyEntry = tk.Entry(frame,width=15, textvariable=self.keyVar)
        self.decode_var = tk.IntVar()
        self.decode = tk.Radiobutton(frame, text="Decode", variable=self.decode_var,value=1,command=updateFunction)
        self.encode = tk.Radiobutton(frame, text="Encode", variable=self.decode_var,value=-1,command=updateFunction)
        self.decode_var.set(1)
        self.updateFunction = updateFunction
        #self.update("blah")
    def display(self):
        self.keyEntry.grid()
        self.decode.grid()
        self.encode.grid()
    def update(self, arg1, arg2, arg3):
        self.updateFunction()
    def process(self, text):
        outputText = ""
        i = 0
        #print(self.keyVar.get())
        if len(self.keyVar.get()) == 0:
            return text
        for letter in text:
            if letter.upper() in constants.alphabet:
                if self.keyVar.get()[i%len(self.keyVar.get())].upper() in constants.alphabet:
                    knum = constants.alphabet.index(self.keyVar.get()[i % len(self.keyVar.get())].upper())
                    lnum = constants.alphabet.index(letter.upper())
                    newLetter = constants.alphabet[((lnum - (knum*self.decode_var.get())))%26]
                    if letter.upper() == letter:
                        outputText += newLetter.lower()
                    else:
                        outputText += newLetter
                else:
                    #outputText += "?"
                    outputText += letter
                i += 1
            else:
                outputText += letter
        return outputText
class Transposition(Stage):
    name = "Transposition"
    def __init__(self, frame, updateFunction):
        self.updateFunction = updateFunction
        self.col_from = 0
        self.tree = ttk.Treeview(frame, show='headings',selectmode="none", displaycolumns="#all",height=16)
        self.visual_drag = ttk.Treeview(frame, show='headings',selectmode="none", displaycolumns="#all")
        self.scroll = tk.Scrollbar(frame,orient="vertical",command=self.tree.yview)
        self.keyLabel = tk.Label(frame,text="Key length:")
        self.keyVar = tk.StringVar()
        self.keyVar.trace_add("write", self.update)
        self.keyEntry = tk.Entry(frame,width=5, textvariable=self.keyVar)
        self.keyEntry.insert(0,"5")
        self.tree.configure(yscrollcommand = self.scroll.set)
        
        self.inputVar = tk.IntVar()
        self.inLabel = tk.Label(frame, text="In:")
        self.inCol = tk.Radiobutton(frame, text="Columns", variable=self.inputVar,value=1,command=updateFunction)
        self.inRow = tk.Radiobutton(frame, text="Rows", variable=self.inputVar,value=-1,command=updateFunction)
        self.inputVar.set(1)
        
        self.outputVar = tk.IntVar()
        self.outLabel = tk.Label(frame, text="Out:")
        self.outCol = tk.Radiobutton(frame, text="Columns", variable=self.outputVar,value=1,command=updateFunction)
        self.outRow = tk.Radiobutton(frame, text="Rows", variable=self.outputVar,value=-1,command=updateFunction)
        self.outputVar.set(1)
        self.prevtext = ""
        self.prevInput = 1
        self.prevOutput = 1
        
    def display(self):
        self.keyLabel.grid(row=0,column=0)
        self.keyEntry.grid(row=0,column=1)
        self.inLabel.grid(row=1,column=0)
        self.inCol.grid(row=1,column=1)
        self.inRow.grid(row=1,column=2)
        self.outLabel.grid(row=2,column=0)
        self.outCol.grid(row=2,column=1)
        self.outRow.grid(row=2, column=2)
        self.scroll.grid(row=3,column=0,sticky=tk.N+tk.S+tk.E)
        self.tree.grid(row=3,column=1,columnspan=2,sticky=tk.W)
        self.tree.bind("<ButtonPress-1>", self.bDown)
        self.tree.bind("<ButtonRelease-1>",self.bUp)
        self.tree.bind("<Motion>",self.bMotion)
        #self.reload("Hello")
        self.updateFunction()
    def update(self, arg1, arg2, arg3):#Used by the entry widget to update when the number of columns changes
        self.prevtext = ""#Make sure it actually updates
        self.updateFunction()
    def swap(self, tv, col1, col2):  #Swaps col1 and col2 in tv (a treeview widget)
        dcols = list(tv["displaycolumns"])
        if dcols[0] == "#all":
            dcols = list(tv["columns"])
        id1 = self.tree.column(col1, 'id')
        id2 = self.tree.column(col2, 'id')
        i1 = dcols.index(id1)
        i2 = dcols.index(id2)
        dcols[i1] = id2
        dcols[i2] = id1
        tv["displaycolumns"] = dcols
        #loadOutput()
        self.updateFunction()
    def bDown(self, event):
        global dx, col_from_id
        tv = event.widget
        if tv.identify_region(event.x, event.y) != 'separator':
            col = tv.identify_column(event.x)
            self.col_from_id = tv.column(col, 'id')
            # get column x coordinate and width
            bbox = tv.bbox(tv.get_children("")[int(tv.yview()[0]*len(tv.get_children("")))], self.col_from_id)
            #print(bbox)
            self.dx = bbox[0] - event.x  # distance between cursor and column left border
            self.visual_drag.configure(displaycolumns=[self.col_from_id])
            self.visual_drag.yview_moveto(self.tree.yview()[0])
            self.visual_drag.place(in_=tv, x=bbox[0], y=0, anchor='nw', width=bbox[2], relheight=1)
        else:
            col_from_id = None
    def bUp(self, event):
        self.visual_drag.place_forget()
    def bMotion(self, event):
        tv = event.widget
        # drag around label if visible
        if self.visual_drag.winfo_ismapped():
            x = self.dx + event.x
            # middle of the dragged column
            xm = int(x + self.visual_drag.column('#1', 'width')/2)
            self.visual_drag.place_configure(x=x)
            col = tv.identify_column(xm)
            # if the middle of the dragged column is in another column, swap them
            if col == "":
                pass
            elif tv.column(col, 'id') != self.col_from_id:
                self.swap(tv, self.col_from_id, col)

    def process(self, text):
        got = self.keyVar.get()
        if got == "":
            got = "1"
        self.cols = int(got)
        if self.prevtext != text or self.inputVar.get() != self.prevInput or self.outputVar.get() != self.prevOutput:#If it redraws the table all the time you can't swap the columns because they reset
            self.reload(text)
            self.prevtext = text
            self.prevOutput = self.outputVar.get()
            self.prevInput = self.inputVar.get()
            
        dcols = list(self.tree["displaycolumns"])
        if dcols[0] == "#all":
            dcols = list(self.tree["columns"])
        #print(dcols)
        self.outputText = ""
    
        if self.ouputVar.get() == 1 and self.inputVar.get() == 1:#col to col
            smallColLen = math.floor(len(text)/self.cols)#length of the smaller columns
            bigCols = len(text) - 1 - (smallColLen*self.cols)#number of columns which are bigger
            for col in dcols:
                for row in range(math.ceil(len(text)/self.cols)):
                    self.outputText += text[col*smallColLen+row]
            
        if self.outputVar.get() == 1:
            #col to col:
            smallColLen = math.floor(len(text)/self.cols)#length of the smaller columns
            bigCols = len(text) - 1 - (smallColLen*self.cols)#number of columns which are bigger
            print(smallColLen, ",", bigCols, len(text)-1)
            for col in dcols:
                col=int(col)
                self.outputText += text[(smallColLen+1)*min(col-1,0) - min(0,col - bigCols - 1):(smallColLen+1)*(col+1)- min(0,col - bigCols + 1)]
                #self.outputText += text[smallColLen*min(col-1,0) - min(0,col -(self.cols-smallCols)):(smallColLen+1)*(col+1)- min(0,col -(self.cols-smallCols)+1)]
##                if col <= self.cols-smallCols:#If this is a longer column
##                    self.outputText += text[(smallColLen+1)*min(col-1,0):(smallColLen+1)*(col+1)]
##                    self.outputText += text[(smallColLen+1)*min(col-1,0) - min(0,col -(self.cols-smallCols):(smallColLen+1)*(col+1)- min(0,col -(self.cols-smallCols)+1)]
##                elif col == self.cols - smallCols + 1:
##                    self.outputText += text[(smallColLen+1)*(self.cols-smallCols):(smallColLen+1)*(self.cols-smallCols+1)-1]
##                else:#shorter column
##                    self.outputText += text[(smallColLen+1)*(self.cols-smallCols)+smallColLen*(col-1):]
        else:
            for row in range(math.ceil(len(text)/self.cols)):
                for col in dcols:
                    if row*self.cols+int(col) < len(text):
                        self.outputText += text[row*self.cols+int(col)]
        return self.outputText
        
    def reload(self, text):#Puts the text in the tree, and the drag tree. This resets the column order too
        self.tree["displaycolumns"] = "#all"
        self.visual_drag["displaycolumns"] = "#all"
        self.tree.delete(*self.tree.get_children())
        self.visual_drag.delete(*self.visual_drag.get_children())
        columns = []
        for cnum in range(0,self.cols):
            columns.append(str(cnum))
        self.tree.configure(columns=columns)
        self.visual_drag.configure(columns=columns)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=25,stretch=False)
            self.visual_drag.heading(col, text=col)
            self.visual_drag.column(col, width=25)
        for row in range(math.ceil(len(text)/self.cols)):
            vals = []
            for v in text[row*self.cols:(row+1)*self.cols]:
                vals.append(v)
            self.tree.insert('', 'end',values=vals)
            self.visual_drag.insert('', 'end',values=vals)
