class __log__:
    MAX_SIZE = 1000
    DUMP_FILE = "data/log.txt"

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
            self.log.pop(0)
    
    def get(self):
        return self.log[self.cursor]
    
    def move(self, i):
        self.cursor = i

    def __len__(self):
        return len(self.log)
    
    def dump(self):
        file = open(self.DUMP_FILE, "w")
        for line in self.log:
            file.write(line + "\n")
        file.close()

LOG = __log__()