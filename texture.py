import pygame
import utils

class Texture:
    PATH = "data\\textures\\"
    slices = []
    slice_count = 0

    def __init__ (self, file):
        file = self.PATH + file
        base_image = pygame.image.load(file)
        dimensions = base_image.size
        self.slice_count = dimensions[0]
        self.slices = [None] * self.slice_count
        for i in range(self.slice_count):
            slice = pygame.Surface((1, dimensions[1]))
            slice.unlock()
            for j in range (dimensions[1]):
                slice.set_at((0, j), base_image.get_at((i, j)))
            slice.lock()
            self.slices[i] = slice
            #self.slices[i] = base_image
        print ("Successfully loaded sliced texture:" + file)

    def update(self):
        # nothing to update so waste a line b/c python
        a = 1

    def get_slice (self, request):
        return self.slices[int(request * self.slice_count)]
    
class AnimatedTexture:
    PATH = "data\\textures\\"
    MANIFEST = "\manifest.csv"
    DATA = "\meta.csv"

    current = 0
    clock = 0
    prev_time = 0
    runtime = 0
    frames = 0
    textures = []

    def __init__ (self, directory):
        self.clock = 0 
        self.current = 0
        self.prev_time = pygame.time.get_ticks()
        file = self.PATH + directory
        data = utils.csv_load(file+self.DATA, 1, 2)
        self.runtime = data[1][0]
        self.frames = data[0][0]
        self.textures = [None] * self.frames
        frame_manifest = utils.csv_load(file + self.MANIFEST, 2, self.frames)
        for i in range (self.frames):
            self.textures[i] = (Texture(directory + "\\" + frame_manifest[i][0]), frame_manifest[i][1])
        print("Successfully loaded animated texture: " + directory)

    # loop through frames
    def update(self):
        time = pygame.time.get_ticks() # get time since epoch
        self.clock += time - self.prev_time # set clock to number of milliseconds since last check
        self.prev_time = time
        if self.clock > self.textures[self.current][1]:
            self.clock = 0
            self.current += 1
            if self.current >= self.frames:
                self.current = 0
    
    def get_slice(self, request):
        self.update()
        return self.textures[self.current][0].get_slice(request)
