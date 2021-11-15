alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
inverses = {1:1,3:9,5:21,7:15,9:3,11:19,15:7,17:23,19:11,21:5,23:17,25:25}
a_values = [1,3,5,7,9,11,15,17,19,21,23,25]

class Stage:
    name = "stage name"
    def __init__(self, frame, updateFunction): #should create all the widgets with frame as root
        update_function = updateFunction #and save updateFunction, and frame if needed (needed when adding more widgets later)
    def decode(self, text):
        return text
    def encode(self, text): #by default the same as decode (for text stages)
        return self.decode(text)
    def display(self): #should grid/pack the stage's widgets
        pass
    def updateOutputWidget(self, text, textRef): #called after all the text is processed, for changing text colours etc
        pass
