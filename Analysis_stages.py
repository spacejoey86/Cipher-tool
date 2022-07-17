import tkinter as tk
import Constants
from Constants import Stage, vowels, vowel_rarity

class Length(Stage):
    name = "Length"
    output = None
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.output = tk.Label(frame, text="")
    def display(self):
        self.output.grid(sticky="NW")
    def decode(self, text):
        self.output.configure(text="Length = " + str(len(text)))
        return text
class PlayfairDetect(Stage):
    name = "Detect Playfair"
    output = None
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.output = tk.Label(frame, text="")
    def display(self):
        self.output.grid(sticky="NW")
    def decode(self, text):
        doubles = False
        for i in range(len(text)//2):
            if text[i] == text[i+1]:
                doubles = True
                break
        if doubles:
            self.output.configure(text="Doubles found, this isn't a Playfair cipher")
        else:
            self.output.configure(text="Doubles not found, this could be a Playfair cipher")
        return text
class IoC(Stage):
    name = "Index of Coincedence"
    def __init__(self, frame, updateFunction):
        self.updateFunction = updateFunction
        self.output_label = tk.Label(frame, text="")
    def display(self):
        self.output_label.grid(sticky="NW")
    def decode(self, text):
        o = sum([f*(f-1) for f in [text.count(letter) + text.count(letter.lower()) for letter in Constants.alphabet]])
        length = sum([1 for letter in text if letter in Constants.alphabet or letter.upper() in Constants.alphabet])
        r = length * (length - 1)
        if r != 0:
            IoC = round(o / r, 5)
        else:
            IoC = "Failed: length cannot be 0 or 1"
        self.output_label.configure(text="IoC = " + str(IoC))
        return text
class VigenereKeyword(Stage):
    name = "Vigenere keyword length"
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.input_var = tk.StringVar(value="20")
        self.input = tk.Entry(frame, width=5, textvariable=self.input_var)
        Constants.writeTrace(self.input_var, lambda a, b, c, self=self : self.updateFunction())
        self.output = tk.Label(frame, text="")
    def display(self):
        self.input.grid(sticky="NW")
        self.output.grid(sticky="NW")
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
    def IC(self, text):
        length = len(text)
        frequency = {}
        a = 0.0
        for letter in Constants.alphabet:
            frequency[letter] = text.count(letter)
        for letter in Constants.alphabet:
            a += frequency[letter] * (frequency[letter] - 1)
        IC = a / (length * (length - 1))
        return round(IC, 5)
    def decode(self, text):
        if self.input.get().isnumeric():
            outputText = ""
            for currentKey in range(2, int(self.input.get()) + 1):
                tempIC = []
                for i in range(currentKey):
                    tempText = []
                    for letter in range(i, len(text), currentKey):
                        tempText.append(text[letter])
                    tempIC.append(self.IC(tempText))
                outputText += str(currentKey) + " : " + str(round(sum(tempIC) / len(tempIC), 3)) + "\n"
            self.output.configure(text=outputText)
        return text
class WordFinder(Stage):
    name = "Word Finder"
    output = None
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.input_var = tk.StringVar()
        self.input = tk.Entry(frame, width=20, textvariable=self.input_var)
        self.input.configure(font=('Courier New', 10)) #same font so it lines up with the output
        Constants.writeTrace(self.input_var, lambda a, b, c, self=self : self.updateFunction())
        self.output = tk.Label(frame, text="")
        self.output.configure(font=('Courier New', 10))
    def display(self):
        self.input.grid(sticky="NW", padx=2) #padding so it lines up with the output
        self.output.grid(sticky="NW")
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
    def changeformat(self, text): #returns an identifier representing where there are repeated letters in the string (but not what letters they are)
        nextLetter = 0
        outputText = []
        for index, letter in enumerate(text):
            if outputText == []:
                outputText.append(Constants.alphabet[nextLetter])
                nextLetter += 1
            else:
                repeated = -1
                for i, v in enumerate(range(0, index)):
                    if letter == text[i]:
                        repeated = i
                if repeated == -1:
                    outputText.append(Constants.alphabet[nextLetter])
                    nextLetter += 1
                else:
                    outputText.append(outputText[repeated])
        return outputText
    def decode(self, text):
        #self.input needs to have repeated letters, else it will match everything. add status bar message
        matches = {}
        for index, letter in enumerate(text):
            testWord = ""
            if len(text) - len(self.input.get()) >= index:
                for v in range(len(self.input.get())):
                    testWord += text[index + v]
            else:
                break
            if self.changeformat(self.input.get().lower()) == self.changeformat(testWord):
                if not testWord in matches:
                    matches[testWord] = 0
                matches[testWord] += 1
        output = ""
        for match in sorted(matches, key=matches.get, reverse=True):
            output += match + " : " + str(matches[match]) + "\n"
        if len(self.input.get()) == 0:
            output = ""
        self.output.configure(text=output)
        return text
class FrequencyAnalyse(Stage):
    name = "Frequency analysis"
    output = None
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.output = tk.Label(frame, text="")
    def display(self):
        self.output.grid(sticky="NW")
    def decode(self, text):
        frequency = {}
        for letter in set(text):
            frequency[letter] = round(text.count(letter)/len(text)*100, 2)
        output_text = ""
        for letter in sorted(frequency, key=frequency.__getitem__, reverse=True):
            output_text += letter + " = " + str(frequency[letter]) + "\n"
        self.output.configure(text=output_text)
        return text
class Doubles(Stage):
    name = "Bigram frequencies"
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.frame2 = tk.Frame(frame)
        self.frame2.rowconfigure(0, weight=1)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(1, weight=1)
        self.canvas = tk.Canvas(self.frame2)
        self.scroll = tk.Scrollbar(self.frame2, orient="vertical", command=self.canvas.yview)
        self.output = tk.Label(self.canvas, text="")
        self.output.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.output, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
    def display(self):
        self.frame2.grid(sticky="NSW")
        self.canvas.grid(sticky="NS")
        self.scroll.grid(sticky="NS", column=1, row=0)
    def decode(self, text):
        frequency = {}
        for letter in set(text[i]+text[i+1] for i in range(len(text)-1)):
            frequency[letter] = round(text.count(letter)/len(text)*100, 2)
        output_text = ""
        for letter in sorted(frequency, key=frequency.__getitem__, reverse=True):
            output_text += letter + " = " + str(frequency[letter]) + "\n"
        self.output.configure(text=output_text)
        return text
class Triples(Stage):
    name = "Trigram frequencies"
    def __init__(self, frame, updateFunction):
        self.frame = frame
        self.updateFunction = updateFunction
        self.frame2 = tk.Frame(frame)
        self.frame2.rowconfigure(0, weight=1)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(1, weight=1)
        self.canvas = tk.Canvas(self.frame2)
        self.scroll = tk.Scrollbar(self.frame2, orient="vertical", command=self.canvas.yview)
        self.output = tk.Label(self.canvas, text="")
        self.output.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.output, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
    def display(self):
        self.frame2.grid(sticky="NSW")
        self.canvas.grid(sticky="NS")
        self.scroll.grid(sticky="NS", column=1, row=0)
    def decode(self, text):
        frequency = {}
        for letter in set(text[i]+text[i+1]+text[i+2] for i in range(len(text)-2)):
            frequency[letter] = round(text.count(letter)/len(text)*100, 2)
        output_text = ""
        for letter in sorted(frequency, key=frequency.__getitem__, reverse=True):
            output_text += letter + " = " + str(frequency[letter]) + "\n"
        self.output.configure(text=output_text)
        return text
class ColumnarKeyword(Stage):
    name = "Columnar Analysis"
    def __init__(self, frame, updateFunction):
        self.variations = ["Write by rows, read by collumns", "Write by row, read by rows"]
        self.variation_selection = tk.StringVar(frame, "Write by rows, read by collumns")
        self.option_menu = tk.OptionMenu(frame, self.variation_selection, *self.variations, command=lambda args : updateFunction())
        self.updateFunction = updateFunction
        self.input_var = tk.StringVar(value="20")
        self.input = tk.Entry(frame, width=5, textvariable=self.input_var)
        self.input_var.trace_add("write", lambda a, b, c, self=self : self.updateFunction())
        self.output = tk.Label(frame, text="")
        self.frame = frame
    def display(self):
        self.option_menu.grid(sticky="NW")
        self.input.grid(column=1, row=0, sticky="NW", padx=20)
        self.output.grid(sticky="NW")
        tk.Grid.rowconfigure(self.frame, 0, weight=0)
        tk.Grid.columnconfigure(self.frame, 0, weight=0)
    def decode(self, text):
        output = ""
        if self.input_var.get().isnumeric():
            vowel_differences = {}
            for key_length in range(1, int(self.input_var.get())):
                if key_length == 0 or key_length == 1:
                    continue
                if self.variation_selection.get() == "Write by rows, read by collumns":
                    collumn_lengths = []
                    for collumn in range(key_length):
                        collumn_lengths.append(len(text) // key_length)
                        if collumn < len(text) % key_length:
                            collumn_lengths[collumn] += 1
                    row_text = ""
                    for letter in range(len(text)):
                        letter_index = 0
                        for collumn in range(letter % key_length):
                            letter_index += collumn_lengths[collumn]
                        letter_index += letter // (key_length)
                        row_text += text[letter_index]
                elif self.variation_selection.get() == "Write by row, read by rows":
                    row_text = text
                rows = []
                for letter in range(len(row_text)):
                    if letter % key_length == 0:
                        rows.append(row_text[letter])
                    else:
                        rows[-1] += row_text[letter]
                vowel_difference = 0
                for index, row in enumerate(rows):
                    vowel_count = 0
                    for letter in row:
                        if letter in vowels: vowel_count += 1
                    vowel_difference += abs(vowel_rarity - vowel_count / len(row))
                vowel_differences[key_length] = vowel_difference
            output = ""

            if vowel_differences[2] != 0:
                multi = 100 / vowel_differences[2]
            else:
                multi = 1
            for index, key in enumerate(vowel_differences):
                output += str(key) + ": " + str(round(vowel_differences[key] * multi, 2)) + "\n"
                
        self.output.configure(text=output)
        return text
    
class AffineKey(Stage):
    name = "Affine Analysis"
    
    def __init__(self, frame, updateFunction):
        self.substitutions = {}
        self.updateFunction = updateFunction
        
        self.label_one = tk.Label(frame, text="Substitute")
        self.label_two = tk.Label(frame, text="for")
        self.result = tk.Label(frame, text="")
        self.sub_entry_one = tk.Entry(frame, width=20)
        self.sub_entry_two = tk.Entry(frame, width=20)
        self.sub_entry_one.bind("<FocusIn>",lambda event:self.sub_entry_one.selection_range(0, tk.END))
        self.sub_entry_two.bind("<FocusIn>",lambda event:self.sub_entry_two.selection_range(0, tk.END))
        self.sub_button = tk.Button(frame, text="Substitute",command=self.substitute)
        self.rev_button = tk.Button(frame, text="Un-substitute",command=self.unSubstitute,takefocus=0)
        self.sub_display = tk.Label(frame,text="")
        
    def display(self):
        self.label_one.grid(row=0,column=0)
        self.label_two.grid(row=0,column=2)
        self.result.grid(row=1,column=1)
        self.sub_entry_one.grid(row=0,column=1)
        self.sub_entry_two.grid(row=0,column=3)
        self.sub_button.grid(row=0,column=4, padx=10)
        self.rev_button.grid(row=1,column=4, padx=10)
        self.sub_display.grid(row=0,column=5,rowspan=3)
        
    def decode(self, text):
        output = "α = {}, β = {}."
        a = 'unsolved'
        b = 'unsolved'

        substitutions = {} # Swaps key and value and has (at maximum) two items that when used in simultaneous equations make the coefficient of α have a multiplicitive inverse
        for x in self.substitutions:
            cur = Constants.alphabet.index(self.substitutions[x].upper())
            try:
                y = {x % 2: substitutions[x] for x in substitutions}[1 - cur % 2]
                if abs(Constants.alphabet.index(self.substitutions[x].upper()) - Constants.alphabet.index(self.substitutions[y].upper())) != 13:
                    if cur % 2 not in [x % 2 for x in substitutions]: substitutions[cur] = x
            except:
                if cur % 2 not in [x % 2 for x in substitutions]: substitutions[cur] = x

        print(substitutions)
        
        if len({x % 2 for x in substitutions}) == 2:
            e1 = [list(substitutions)[0], Constants.alphabet.index(substitutions[list(substitutions)[0]].upper())] # First equation
            e2 = [list(substitutions)[1], Constants.alphabet.index(substitutions[list(substitutions)[1]].upper())] # Second equation
            final = [(e1[0] - e2[0]) % 26, (e1[1] - e2[1]) % 26]
            
            a = str((final[1] * Constants.inverses[final[0]]) % 26)
            b = str((e1[1] - e1[0] * int(a)) % 26)
        
        self.result.configure(text=output.format(a, b))
        
        display_text = ""
        for letter in Constants.alphabet + [x.lower() for x in Constants.alphabet]:
            if letter in self.substitutions.keys():
                display_text = display_text + letter + " -> " + self.substitutions[letter] + "\n"
        self.sub_display.configure(text=display_text)
        
        return text
    
    def substitute(self):
        phrase1 = self.sub_entry_one.get()
        phrase2 = self.sub_entry_two.get()
        
        if len(phrase1) != len(phrase2):
            self.sub_button.bell(displayof=0)
        else:
            for letter_index in range(len(phrase1)):
                letter_1 = phrase1[letter_index]
                letter_2 = phrase2[letter_index]
                
                if letter_1 in self.substitutions.keys():
                    self.sub_button.bell(displayof=0)
                elif letter_1 == letter_2:
                    self.sub_button.bell(displayof=0)
                else:
                    self.substitutions[letter_1] = letter_2
                    
        self.updateFunction()
        
    def unSubstitute(self):
        phrase1 = self.sub_entry_one.get()
        phrase2 = self.sub_entry_two.get()
        
        if phrase1 == "":
            self.substitutions = {key:val for key, val in self.substitutions.items() if val not in phrase2}
        elif phrase2 == "":
            self.substitutions = {key:val for key, val in self.substitutions.items() if key not in phrase1}
        else:
            self.substitutions = {key:val for key, val in self.substitutions.items() if (key not in phrase1) or (val not in phrase2)}
            
        self.updateFunction()
