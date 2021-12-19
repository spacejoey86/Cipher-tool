import tkinter as tk
from tkinter import ttk
import Constants
from Constants import Stage
import math #For ceiling function (round up)

class RailFence(Stage):
    name = "Rail fence"
    def __init__(self, frame, updateFunction):
        self.variations = ["Write vertically, read horizontally", "Write horizontally, read vertically"]
        self.variation_selection = tk.StringVar(frame, "Write vertically, read horizontally")
        self.option_menu = tk.OptionMenu(frame, self.variation_selection, *self.variations, command=lambda args : updateFunction())
        self.key_length_string = tk.StringVar(value="2")
        self.key_length_input = tk.Entry(frame, width=5, textvariable=self.key_length_string)
        self.key_length_string.trace_add("write", lambda a, b, c : updateFunction())
        self.frame = frame
    def display(self):
        self.option_menu.grid(sticky="NW")
        self.key_length_input.grid(column=1, row=0, sticky="NW", padx=20)
        tk.Grid.rowconfigure(self.frame, 0, weight=0)
        tk.Grid.columnconfigure(self.frame, 0, weight=0)
    def looping_counter(self, maximum): # A generator so the rails can be looped through in the right order
        counter = [0, 0]
        while True:
            yield counter[1]
            counter[0] = (counter[0] + 1) % (maximum * 2 - 2)
            counter[1] = counter[0] - 2 * (counter[0] // maximum) * (counter[0] % maximum + 1)
    def update_variables(self, text):
        if self.key_length_string.get().isnumeric():
            self.rail_lengths = {}
            self.key_length = int(self.key_length_string.get())
            
            # The text is a number of complete cycles, plus an extra length
            self.cycle_length = self.key_length * 2 - 2
            self.extra_length = len(text) % self.cycle_length
            
            # Work out the length of the rails
            for rail_index in range(self.key_length): # This ignores the extra length
                self.rail_lengths[rail_index] = (len(text) - self.extra_length) // (self.key_length - 1)
                if rail_index == 0 or rail_index == self.key_length - 1:
                    self.rail_lengths[rail_index] = self.rail_lengths[rail_index] // 2

            counter = self.looping_counter(self.key_length)
            for i in range(self.extra_length): # This adds the extra length
                self.rail_lengths[next(counter)] += 1
    def write_horizontal(self, text):
        if self.key_length_string.get().isnumeric():
            output = ""
            
            # Find the index of each letter in the ciphertext then add it to output
            for rail in range(self.key_length):
                for index in range(self.rail_lengths[rail]):
                    letter_index = 0
                    letter_index += rail
                    if rail == 0 or rail == self.key_length - 1:
                        letter_index += index * self.cycle_length
                    else:
                        letter_index += index * (self.key_length - 1)
                        if index % 2 == 1:
                            letter_index += ((self.key_length - 1) / 2 - rail) * 2
                    output += text[int(letter_index)]
            return output
    def write_vertical(self, text):
        if self.key_length_string.get().isnumeric():
            output = ""
            
            # Find the index of each letter in the ciphertext then add it to output
            counter = self.looping_counter(self.key_length)
            for i in range(len(text)):
                current_count = next(counter)
                letter_index = 0
                for rail in range(current_count):
                    letter_index += self.rail_lengths[rail]
                if current_count == 0 or current_count == self.key_length - 1:
                    letter_index += i // self.cycle_length
                else:
                    letter_index += i // (self.key_length - 1)
                output += text[letter_index]
            text = output
        return text
    def decode(self, text):
        self.update_variables(text)
        if self.variation_selection.get() == "Write horizontally, read vertically":
            return self.write_horizontal(text)
        elif self.variation_selection.get() == "Write vertically, read horizontally":
            return self.write_vertical(text)
    def encode(self, text):
        self.update_variables(text)
        if self.variation_selection.get() == "Write horizontally, read vertically":
            return self.write_vertical(text)
        elif self.variation_selection.get() == "Write vertically, read horizontally":
            return self.write_horizontal(text)
class Scytale(Stage):
    name = "Scytale"
    def __init__(self, frame, updateFunction):
        self.variations = ["Write vertically, read horizontally", "Write horizontally, read vertically"]
        self.variation_selection = tk.StringVar(frame, "Write vertically, read horizontally")
        self.option_menu = tk.OptionMenu(frame, self.variation_selection, *self.variations, command=lambda args, self=self : updateFunction())
        self.key_length = tk.StringVar(value="2")
        self.key_length_input = tk.Entry(frame, width=5, textvariable=self.key_length)
        self.key_length.trace_add("write", lambda a, b, c, self=self : updateFunction())
        self.frame = frame
    def display(self):
        tk.Grid.rowconfigure(self.frame, 0, weight=0)
        tk.Grid.columnconfigure(self.frame, 0, weight=0)
        self.option_menu.grid(column=0, sticky="NW")
        self.key_length_input.grid(column=1, row=0, sticky="NW", padx=20)
    def decode(self, text):
        if self.key_length.get().isnumeric():
            # A generator so the lines can be looped through in the right order
            def looping_counter(maximum):
                counter = 0
                while True:
                    yield counter % maximum
                    counter += 1

            output = ""
            line_lengths = {}
            key_length = int(self.key_length.get())
            
            # The text is a number of complete cycles, plus an extra length
            cycle_length = key_length
            extra_length = len(text) % cycle_length
            
            # Work out the length of the lines
            for line_index in range(key_length): # This ignores the extra length
                line_lengths[line_index] = (len(text) - extra_length) // (key_length)

            counter = looping_counter(key_length)
            for i in range(extra_length): # This adds the extra length
                line_lengths[next(counter)] += 1

            # Find the index of each letter in the ciphertext then add it to output
            if self.variation_selection.get() == "Write horizontally, read vertically":
                counter = looping_counter(key_length)
                for line in range(key_length):
                    for index in range(line_lengths[line]):
                        letter_index = index * key_length + line
                        output += text[letter_index]
            elif self.variation_selection.get() == "Write vertically, read horizontally":
                counter = looping_counter(key_length)
                for i in range(len(text)):
                    current_count = next(counter)
                    letter_index = 0
                    for line in range(current_count):
                        letter_index += line_lengths[line]
                    letter_index += i // (key_length)
                    output += text[letter_index]
            text = output
        return text
class CaesarShift(Stage):
    name = "Caesar shift"
    def __init__(self, frame, updateFunction):
        self.scale = tk.Scale(frame, from_=0,to=25,orient="horizontal",length=500,command=lambda idk:updateFunction())
        self.down_button = tk.Button(frame, text = " - ",command = lambda:self.scale.set(self.scale.get()-1))
        self.up_button = tk.Button(frame, text = " + ",command = lambda:self.scale.set(self.scale.get()+1))
        self.frame = frame
    def display(self):
        self.down_button.grid(row=1, column=0, sticky="NW")
        self.scale.grid(row=1, column=1, columnspan=2, sticky="NEW")
        self.up_button.grid(row=1, column=3, sticky="NW")
        tk.Grid.rowconfigure(self.frame, 0, weight=0)
        tk.Grid.columnconfigure(self.frame, 0, weight=0)
    def encode(self, text):
        shifted = ""
        for letter in text:
            if letter.upper() in Constants.alphabet: #lowercase to UPPERCASE
                shifted += Constants.alphabet[((Constants.alphabet.index(letter.upper())+self.scale.get()+1)%26)-1]
            else:
                shifted += letter
        return shifted
    def decode(self, text):
        shifted = ""
        for letter in text:
            if letter in Constants.alphabet: #UPPER to lower
                shifted += Constants.alphabet[((Constants.alphabet.index(letter)-self.scale.get()+1)%26)-1].lower()
            else:
                shifted += letter
        return shifted
class Morse(Stage):
    name = "Morse code"
    dot = "."
    dash = "-"
    seperator = " "
    morse_encode = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----'}
    morse_decode = {" ": "", "":""}
    for key, value in morse_encode.items():
        morse_decode[value] = key
    def decode(self, text):
        output_text = ""
        for phrase in text.split(self.seperator):
            if phrase in self.morse_decode.keys():
                output_text += self.morse_decode[phrase].lower()
            elif phrase in [""," "]:
                pass
            elif phrase == "/":
                output_text += " "
            else:
                output_text += phrase
        return output_text
        #return "".join([self.morse_decode[letter] for letter in text.split(self.seperator)]).lower()
    def encode(self, text):
        return " ".join([self.morse_encode[letter.upper()] if letter != letter.upper and letter.upper() in Constants.alphabet else letter for letter in text])
class Substitution(Stage):
    name = "Substitution"
    arrow = " -> "
    def __init__(self, frame, updateFunction):
        self.substitutions = {}
        self.label_one = tk.Label(frame, text="Substitute")
        self.sub_entry_one = tk.Entry(frame, width=20)
        self.sub_entry_one.bind("<FocusIn>",self.SE1S)
        self.label_two = tk.Label(frame, text="for")
        self.sub_entry_two = tk.Entry(frame, width=20)
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
    def decode(self, text):
        self.arrow = " -> "
        self.displaySubs()
        for key, value in self.substitutions.items():
            text = text.replace(key,value)
        return text
    def encode(self, text):
        self.arrow = " <- "
        self.displaySubs()
        for key, value in self.substitutions.items():
            text = text.replace(value,key)
        return text
    def SE1S(self, event):#Functions to select the text in the entry widgets when they are tabbed to
        self.sub_entry_one.selection_range(0, tk.END)
    def SE2S(self, event):
        self.sub_entry_two.selection_range(0, tk.END)
    def substitute(self):
        phrase1 = self.sub_entry_one.get()
        phrase2 = self.sub_entry_two.get()
        if len(phrase1) != len(phrase2):
            self.sub_button.bell(displayof=0)
        else:
            for letter_index in range(len(phrase1)):
                letter_1 = phrase1[letter_index]
                letter_2 = phrase2[letter_index]
                if letter_1 in self.substitutions.keys(): #letter_1 has already been substituted
                    self.sub_button.bell(displayof=0)
                elif letter_1 == letter_2: #They can't be the same
                    self.sub_button.bell(displayof=0)
                else:
                    self.substitutions[letter_1] = letter_2
                    self.updateFunction()
        self.displaySubs()
        self.updateFunction()
    def displaySubs(self):
        display_text = ""
        for letter in Constants.alphabet + [x.lower() for x in Constants.alphabet]:
            if letter in self.substitutions.keys():
                display_text = display_text + letter + self.arrow + self.substitutions[letter] + "\n"
        self.sub_display.configure(text=display_text)
    def unSubstitute(self):
        s1 = self.sub_entry_one.get()
        s2 = self.sub_entry_two.get()
        if s1 == "":
            self.substitutions = {key:val for key, val in self.substitutions.items() if val not in s2}
        elif s2 == "":
            self.substitutions = {key:val for key, val in self.substitutions.items() if key not in s1}
        else:
            self.substitutions = {key:val for key, val in self.substitutions.items() if (key not in s1) or (val not in s2)}
        self.displaySubs()
        self.updateFunction()
class Affine(Stage):
    name = "Affine"
    def __init__(self, frame, updateFunction):
        self.cycleButton = tk.Button(frame, text="Cycle",command=self.cycle)
        self.aLabel = tk.Label(frame, text="0")
        self.aScale = tk.Scale(frame,from_=1,to=12,orient="horizontal",length=300,command=self.update,showvalue=False)
        self.bLabel = tk.Label(frame, text="1")
        self.bScale = tk.Scale(frame,from_=0,to=25,orient="horizontal",length=300,command=self.update,showvalue=False)
        self.updateFunction = updateFunction
        self.update("blah")
    def display(self):
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
        self.a = Constants.a_values[self.aScale.get()-1]
        self.aLabel.config(text=self.a)
        self.ia = Constants.inverses[self.a]
        self.b = self.bScale.get()
        self.bLabel.config(text=self.b)
        self.updateFunction()
    def encode(self, text):
        for letter in Constants.alphabet:
            lNum = Constants.alphabet.index(letter)
            rNum = Constants.alphabet[((self.a*lNum+self.b)%26)].upper()
            text = text.replace(letter.lower(),rNum)
        return text
    def decode(self, text):
        for letter in Constants.alphabet:
            lNum = Constants.alphabet.index(letter)
            rNum = Constants.alphabet[((self.ia*(lNum-self.b))%26)].lower()
            text = text.replace(letter,rNum)
        return text
class Vigenere(Stage):
    name = "Vigenere"
    def __init__(self, frame, updateFunction):
        self.keyVar = tk.StringVar()
        self.keyVar.trace_add("write", self.update)
        self.keyEntry = tk.Entry(frame,width=15, textvariable=self.keyVar)
        self.updateFunction = updateFunction
    def display(self):
        self.keyEntry.grid()
    def update(self, arg1, arg2, arg3):
        self.updateFunction()
    def encode(self, text):
        output_text = ""
        key_index = 0
        key = self.keyVar.get()
        if len(self.keyVar.get()) == 0: #Ignore if the key box is empty
            return text
        for letter in text:
            if letter.upper() in Constants.alphabet and letter != letter.upper(): #lowercase letters in the alphabet only
                key_letter = key[key_index % len(key)].upper()
                if key_letter in Constants.alphabet:
                    knum = Constants.alphabet.index(key_letter)
                    lnum = Constants.alphabet.index(letter.upper())
                    newLetter = Constants.alphabet[(lnum + knum)%26]
                    output_text += newLetter
                else:
                    output_text += "?" #integrate with blanking somehow
                key_index += 1
            else:
                output_text += letter
        return output_text
    def decode(self, text):
        output_text = ""
        key_index = 0
        key = self.keyVar.get()
        if len(self.keyVar.get()) == 0: #Ignore if the key box is empty
            return text
        for letter in text:
            if letter in Constants.alphabet: #UPPERCASE letters in the alphabet only
                key_letter = key[key_index % len(key)].upper()
                if key_letter in Constants.alphabet:
                    knum = Constants.alphabet.index(key_letter)
                    lnum = Constants.alphabet.index(letter)
                    newLetter = Constants.alphabet[(lnum - knum)%26]
                    output_text += newLetter.lower()
                else:
                    output_text += "?"
                key_index += 1
            else:
                output_text += letter
        return output_text
class Transposition(Stage): #this one is broken
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
        self.scroll.grid(row=3,column=0,sticky="NSE")
        self.tree.grid(row=3,column=1,columnspan=2,sticky="ESW")
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

    def process(self, text): #swap for encode and decode
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
