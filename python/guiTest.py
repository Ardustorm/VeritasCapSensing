from serial import *
from tkinter import *
from fakeSerial import *
from barStatus import *
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



votes = [0 for i in range(BUTTON_NUM)]            # an array to store votes for each
canVote = [True for i in range(BUTTON_NUM)] # keeps track if slider has reset yet
status = [0.0 for i in range(BUTTON_NUM)] # what stage is the button in (ie starting to vote, cooling down, at max/min)

offset = 200                                # offset between each of the bars
width = 50                      # of each bar
left = 1200                     # where to start the bars (from the left)
length = 450                    # max length of each bar
top =400                        # Where to start the bars



# make a text box to put the serial output
log = Text ( root, width=50, height=10, takefocus=0)
log.pack()
if not DEBUG:
    log.pack_forget()


question = canvas.create_text( left/2, top +width/2 + offset, width = left, justify=CENTER,
                           font=("Purisa-Bold", 70), anchor =CENTER, fill="#1E1E1E",
                           text = "Is Morality Objective or Subjective?")


barStatus = BarStatus(canvas, (left,top), BUTTON_NUM)



def updateAll(string):
    minimum = left + 30
    maximum = left + length
    threshold = 20             # center point of when bar should move
    deadZone = 10               # prevent jitter (like a schmitt trigger)
    step = 20

    statStep = 0.04

    
    lst = string.split()
    if(len(lst) < BUTTON_NUM):          # stop processing if list incomplete
        return

    for i in range(BUTTON_NUM):
        if int(lst[i]) > threshold + deadZone:
            status[i] += statStep
        elif int(lst[i]) < threshold - deadZone:
            status[i] += - statStep
        status[i] = max( min(1, status[i]), 0)

        if status[i] == 1 and canVote[i]:
            votes[i]+=1
            canVote[i] = False
            # A vote was just cast
        elif status[i] == 0:
            canVote[i] = True
            # A button was just reset

    barStatus.update( votes, status, canVote)


    
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
