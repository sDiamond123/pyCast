import pygame
import utils
import math
#from log import LOG as log

class Texture:
    PATH = "data/textures/"
    
    slices = []
    slice_count = 0

    def __init__ (self, file):
        file = self.PATH + file
        base_image = pygame.image.load(file)
        dimensions = base_image.get_size()
        self.slice_count = dimensions[0]
        self.slices = [None] * self.slice_count
        for i in range(self.slice_count):
            self.slices[i] = base_image.subsurface((i,0,1,dimensions[1]))
        #log.write ("Successfully loaded sliced texture:" + file)

    def update(self):
        # nothing to update so waste a line b/c python
        a = 1

    def get_slice (self, request):
        return self.slices[int(request * self.slice_count)]
    
class AnimatedTexture:
    PATH = "data/textures/"
    MANIFEST = "/manifest.csv"
    DATA = "/meta.csv"

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
            self.textures[i] = (Texture(directory + "/" + frame_manifest[i][0]), frame_manifest[i][1])
        #log.write("Successfully loaded animated texture: " + directory)

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

class RollingTexture:
    PATH = "data/textures/rolling/"

    base_image = None
    phase = 0
    internal_screen = None
    external_screen = None
    fov = 0
    height = 0
    width = 0
    scale = 0

    def __init__ (self, file, t_0, fov, w, h):
        file = self.PATH + file
        self.phase = t_0
        self.fov = fov
        self.external_screen = pygame.Surface((w,h))
        self.base_image = pygame.image.load(file)
        self.height = self.base_image.get_size()[1]
        self.width = self.base_image.get_size()[0]
        self.scale = self.width/(2 * math.pi)
        self.internal_screen = pygame.Surface((fov * self.scale, self.height))

    #@functools.lru_cache
    def render (self, phase):
        ang = phase - self.phase
        lower = utils.normalize_angle(ang - self.fov/2) * self.scale
        upper = utils.normalize_angle(ang + self.fov/2) * self.scale
        if (lower > upper):
            front = pygame.Rect(lower, 0, self.width - lower, self.height)
            back = pygame.Rect(0,0,upper, self.height)
            self.internal_screen.blit(self.base_image.subsurface(front), (0,0))
            self.internal_screen.blit(self.base_image.subsurface(back),(self.width - lower, 0))
        else:
            whole = pygame.Rect(lower, 0, upper - lower, self.height)
            self.internal_screen.blit(self.base_image.subsurface(whole), (0,0))
        pygame.transform.scale(self.internal_screen, self.external_screen.get_size(), self.external_screen)
        
        