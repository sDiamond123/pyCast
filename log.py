from utils import Ptr as ptr

class __log__:
    MAX_SIZE = 1000
    DUMP_FILE = "data/log.txt"

    def __init__(self):
        self.log = ptr([])
        self.cursor = 0

    def write(self, value):
        if self.cursor  == len(self.log.value):
            self.log.value.append(value)
        else:
            self.log.value.insert(self.cursor, value)
        self.cursor += 1
        if len(self.log.value) > self.MAX_SIZE:
            self.log.value.pop(0)
    
    def get(self):
        return self.log.value[self.cursor]
    
    def move(self, i):
        self.cursor = i

    def __len__(self):
        return len(self.log.value)
    
    def dump(self):
        file = open(self.DUMP_FILE, "w")
        for line in self.log.value:
            file.write(line + "\n")
        file.close()

LOG = __log__()