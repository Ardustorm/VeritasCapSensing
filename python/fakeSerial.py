

class FakeSerial:

    def __init__(self, filename):
        self.filename = open(filename, 'r')
        self.delay = 0

    def read(self):
        self.delay += 1
        if (self.delay % 5 != 0):
            return bytes(self.filename.read(1), "utf-8")
        else:
            return bytes("", "utf-8")
        
