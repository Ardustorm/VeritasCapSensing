from tkinter import *

class DividedBarGraph:
    #rects = []
    #numbers = []
    #labels = []
    colors = ["#293352", "purple", "green", "red", "blue", "grey", "pink"]
    colorsActive = []

    length = 1000
    width = 50
    fontSize = 35

    def __init__(self, canvas, loc, labelsText= []):
        self.canvas = canvas
        self.location = loc
        self.rects = []                      # The bars in the bar graph
        self.labels = []                     # Currently used to display votes
        self.numbers =[]
        #self.labelsText = labelsText
        self.makeBar(labelsText)

    def makeBar(self, labelsText):
        self.number = len(labelsText)

        for i in range(self.number):
            x0 = self.location[0] + i* self.length/self.number
            y0 = self.location[1]
            x1 = self.location[0]+ (i+1)*self.length/self.number
            y1 = self.location[1] + self.width

            rect = self.canvas.create_rectangle( x0, y0, x1, y1, fill=self.colors[i])
            num = self.canvas.create_text(
                x0, self.location[1],
                font=("Purisa-Bold", self.fontSize), anchor =SW, fill="#1E1E1E",
                text = labelsText[i])
            label = self.canvas.create_text(x0, self.location[1]+self.width,
                font=("Purisa-Bold", self.fontSize), anchor =NW, fill="#1E1E1E",
                text = labelsText[i])
    
            self.rects.append(rect)
            self.numbers.append(num)
            self.labels.append(label)


    def update(self, votes, status, canVote):
        total = sum(votes)

        for i in range (self.number):
            x0, y0, x1, y1 = self.canvas.coords(self.rects[i])

            newStart = sum(votes[:i])/total * self.length +self.location[0]
            newEnd =  newStart + votes[i]/total*self.length
            
            
            self.canvas.coords(self.rects[i], newStart,y0, newEnd, y1)
            self.canvas.coords(self.numbers[i], newStart, self.location[1])
            self.canvas.coords(self.labels[i], newStart, self.location[1]+self.width)
            self.canvas.itemconfig(self.numbers[i], text = str(votes[i]))        


    def changeLabels(self, labelsText):
        for i in range(self.number):
            self.canvas.delete(self.rects[i])
            self.canvas.delete(self.labels[i])
            self.canvas.delete(self.numbers[i])
        self.rects.clear()
        self.labels.clear()
        self.numbers.clear()
        
        self.makeBar(labelsText)
        pass
