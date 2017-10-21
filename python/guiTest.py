from serial import *
from tkinter import *
from fakeSerial import *
from dividedBarGraph import *
# The start of this code came from here Evan Boldt:
# http://robotic-controls.com/learn/python-guis/tkinter-serial


serialPorts = ["/dev/ttyUSB0", "/dev/ttyUSB1","/dev/ttyUSB2", "FAKE"]
baudRate = 115200


for port in serialPorts:
    try:
        if port != "FAKE":
            ser = Serial(port , baudRate, timeout=0, writeTimeout=0) #ensure non-blocking
            print("Connecting to:", port, "... SUCCESS!")
        else:
            print("Using Fake Serial")
            ser = FakeSerial( "test.txt")            
        break
    except:
        print("Cannot connect to:", port)



DEBUG = False
BUTTON_NUM = 3
#make a TkInter Window
root = Tk()
root.wm_title("Veritas Voting")
root.attributes("-fullscreen", True)


def toggleFullscreen(event):
    root.attributes("-fullscreen", root.attributes("-fullscreen") == 0)

def toggleDebug(event):
    global DEBUG
    DEBUG = not DEBUG
    if DEBUG == True:
        log.pack()
    else:
        log.pack_forget()


root.bind("<Control-w>", lambda e: root.destroy())
root.bind("<Escape>", toggleFullscreen)
root.bind("h", toggleDebug)
canvas = Canvas(root, width=1000, height=800, bg="#F3F3F1")
canvas.pack(fill=BOTH, expand=YES)
img = PhotoImage(file='logo.png')
canvas.create_image(1000, 150, image=img)


rects = []                      # The bars in the bar graph
labels = []                     # Currently used to display votes
labelsText = ["Other", "Objective", "Subjective"] # labels for each bar graph
votes = [1 for i in range(BUTTON_NUM)]            # an array to store votes for each
canVote = [True for i in range(BUTTON_NUM)] # keeps track if slider has reset yet
offset = 200                                # offset between each of the bars
width = 50                      # of each bar
length = 450                    # max length of each bar
left = 1200                     # where to start the bars (from the left)
top =400                        # Where to start the bars

barColorNormal = "#C3384B"
barColorHighlight = "#A51C30"

for i in range(BUTTON_NUM):
    rect = canvas.create_rectangle(left, top + offset*i,
                                   left+length, top + width + offset*i, fill="#293352")
    text = canvas.create_text( left+length + width/2, top +width/2 + offset*i,
                               font=("Purisa-Bold", 35), anchor =W, fill="#1E1E1E",
                               text = "TEST OF TEXT")
    options = canvas.create_text( left + width, top +width/2 + offset*i,
                                  font=("Purisa-Bold", 35), anchor =W, fill="#1E1E1E",
                                  text = labelsText[i])
    rects.append(rect)
    labels.append(text)

# make a text box to put the serial output
log = Text ( root, width=50, height=10, takefocus=0)
log.pack()
if not DEBUG:
    log.pack_forget()


question = canvas.create_text( left/2, top +width/2 + offset, width = left, justify=CENTER,
                           font=("Purisa-Bold", 70), anchor =CENTER, fill="#1E1E1E",
                           text = "Is Morality Objective or Subjective?")


# RESULTS::
divGraph = DividedBarGraph( canvas, (200, 1000), 3)





def updateAll(string):
    minimum = left + 30
    maximum = left + length
    threshold = 20             # center point of when bar should move
    deadZone = 10               # prevent jitter (like a schmitt trigger)
    step = 20

    lst = string.split()
    if(len(lst) < BUTTON_NUM):          # stop processing if list incomplete
        return

    for i in range(len(rects)):
        x0, y0, x1, y1 = canvas.coords(rects[i])

        if int(lst[i]) > threshold + deadZone:
            newEnd = x1 + step
        elif int(lst[i]) < threshold - deadZone:
            newEnd = x1 - step
        else:
            newEnd = x1
            
        newEnd = max( min(maximum, newEnd), minimum)

        # check for votes  TODO: make more robust
        if newEnd == maximum and (canVote[i] or i == 1):
            votes[i]+=1
            canvas.itemconfig(rects[i], fill = barColorNormal)
            canVote[i] = False
        elif newEnd == minimum:
            canVote[i] = True
            canvas.itemconfig(rects[i], fill = barColorHighlight)
            
        canvas.coords(rects[i], x0,y0, newEnd, y1)
        #canvas.itemconfig(rects[i], fill = "#A51C30")
        canvas.itemconfig(labels[i], text = str(votes[i]))
    divGraph.update(votes)


        


    
#make our own buffer
#useful for parsing commands
#Serial.readline seems unreliable at times too
serBuffer = ""

def readSerial():
    global serBuffer    # get the buffer from outside of this function
    
    while True:
        c = ser.read() # attempt to read a character from Serial

        if len(c) == 0:         #was anything read?
            break
                            
        if c == b'\n':
            serBuffer += "\n" # add the newline to the buffer

            #add the line to the TOP of the log
            log.insert('0.0', serBuffer)
            #update(serBuffer)
            updateAll(serBuffer)
            serBuffer = "" # empty the buffer
        else:
            serBuffer += c.decode("utf-8")  # add to the buffer

    root.after(2, readSerial) # check serial again soon


# after initializing serial, an arduino may need a bit of time to reset
root.after(200, readSerial)

root.mainloop()
