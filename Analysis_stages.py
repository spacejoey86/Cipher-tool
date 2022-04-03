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
            for index, key in enumerate(vowel_differences):
                output += str(key) + ": " + str(round(vowel_differences[key], 2)) + "\n"
        self.output.configure(text=output)
        return text
