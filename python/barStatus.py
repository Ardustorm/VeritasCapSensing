from tkinter import *

class BarStatus:

    rects = []                      # The bars in the bar graph
    labels = []                     # Currently used to display votes
    options = []


    offset = 200                                # offset between each of the bars
    width = 50                      # of each bar
    length = 450                    # max length of each bar
    left = 1200                     # where to start the bars (from the left)
    top =400                        # Where to start the bars

    rectFill = "#A51C30"
    rectFillAlt = "#C3384B"

    def __init__(self, canvas, loc, num, labelsText=[]):
        self.labelsText = labelsText
        self.number = num
        self.canvas = canvas
        self.location = loc
        for i in range(self.number):
            rect = canvas.create_rectangle(
                self.location[0], self.location[1] + self.offset*i,
                self.location[0]+self.length, self.location[1] + self.width + self.offset*i,
                fill=self.rectFill)
            
            text = canvas.create_text(
                self.location[0]+self.length + self.width/2, self.location[1] +self.width/2 + self.offset*i,
                font=("Purisa-Bold", 35), anchor =W, fill="#1E1E1E")
            option = canvas.create_text(
                self.location[0] + self.width, self.location[1] +self.width/2 + self.offset*i,
                font=("Purisa-Bold", 35), anchor =W, fill="#1E1E1E",
                text = self.labelsText[i])
            
            self.rects.append(rect)
            self.labels.append(text)
            self.options.append(option)



    def update(self, votes, status, canVote):
        step = 20
        maximum = self.length
        minimum = 30

        for i in range(self.number):
            x0, y0, x1, y1 = self.canvas.coords(self.rects[i])
            self.canvas.coords(
                self.rects[i], x0,y0,
                self.location[0] + max( min(maximum, status[i] * maximum), minimum), y1)
            self.canvas.itemconfig(self.labels[i], text = str(votes[i]))

            if canVote[i]:
                self.canvas.itemconfig(self.rects[i], fill=self.rectFill)
            else:
                self.canvas.itemconfig(self.rects[i], fill=self.rectFillAlt)
