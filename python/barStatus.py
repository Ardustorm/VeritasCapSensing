from tkinter import *

class BarStatus:



    offset = 60                                # offset between each of the bars
    width = 40                      # of each bar
    length = 1920 - 300                    # max length of each bar
    rectFill = ["#B71212", "#07106D", "#F26D00", "#0C4F06"]
    #rectFill = ["#293352", "purple", "green", "red", "blue", "grey", "pink"]
    rectFillAlt = rectFill #["#293352", "purple", "green", "red", "blue", "grey", "pink"]
    
    def __init__(self, canvas, loc, labelsText=[]):
        self.rects = []                      # The bars in the bar graph
        self.labels = []                     # Currently used to display votes
        self.options = []
        self.prefixes = []
        self.numOn = False
        self.canvas = canvas
        self.location = loc

        self.makeBars(labelsText)

    # This was part of the init but I moved to seperate function to be able to change them
    def makeBars(self, labelsText):
        self.number = len(labelsText)
        
        for i in range(self.number):
            rect = self.canvas.create_rectangle(
                self.location[0], self.location[1] + self.offset*i,
                self.location[0]+self.length, self.location[1] + self.width + self.offset*i,
                fill=self.rectFill[i])
            if self.numOn:
                text = self.canvas.create_text(
                    self.location[0]+self.length + self.width/2, self.location[1] +self.width/2 + self.offset*i,
                    font=("Purisa-Bold", 35), anchor =W, fill="#1E1E1E")
            option = self.canvas.create_text(
                self.location[0] + self.width, self.location[1] +self.width/2 + self.offset*i,
                font=("Purisa-Bold", 35), anchor =W, fill="#1E1E1E",
                text = labelsText[i])
            prefix = self.canvas.create_text(
                self.location[0] - self.width, self.location[1] +self.width/2 + self.offset*i,
                font=("Purisa-Bold", 35), anchor =W, fill="#1E1E1E",
                text = chr(ord("A") +i))
            
            self.rects.append(rect)
            if self.numOn:
                self.labels.append(text)
            self.options.append(option)
            self.prefixes.append(prefix)


    def update(self, votes, status, canVote):
        step = 20
        maximum = self.length
        minimum = 30

        for i in range(self.number):
            x0, y0, x1, y1 = self.canvas.coords(self.rects[i])
            self.canvas.coords(
                self.rects[i], x0,y0,
                self.location[0] + max( min(maximum, status[i] * maximum), minimum), y1)
            if self.numOn:
                self.canvas.itemconfig(self.labels[i], text = str(votes[i]))

            if canVote[i]:
                self.canvas.itemconfig(self.rects[i], fill=self.rectFill[i])
            else:
                self.canvas.itemconfig(self.rects[i], fill=self.rectFillAlt[i])


    def changeLabels(self, labelsText):
        for i in range(self.number):
            self.canvas.delete(self.rects[i])
            if self.numOn:
                self.canvas.delete(self.labels[i])
            self.canvas.delete(self.options[i])
            self.canvas.delete(self.prefixes[i])
        self.rects.clear()
        if self.numOn:
            self.labels.clear()
        self.options.clear()
        self.prefixes.clear()
            
        self.makeBars(labelsText)
