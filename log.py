class __log__:
    MAX_SIZE = 1000

    def __init__(self):
        self.log = []
        self.cursor = 0

    def write(self, value):
        if self.cursor  == len(self.log):
            self.log.append(value)
        else:
            self.log.insert(self.cursor, value)
        self.cursor += 1
        if len(self.log) > self.MAX_SIZE:
            self.log.pop()
    
    def get(self):
        return self.log[self.cursor]
    
    def move(self, i):
        self.cursor = i

    def __len__(self):
        return len(self.log)
    

LOG = __log__()