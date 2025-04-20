import map
import math
import texture
import pygame
import utils
from log import LOG as log

class Camera:
    # camera constants
    CAST_OFFSET = 0.00001
    MARGIN_OF_ERROR = 0.0001
    MAX_CELL_TRAVERSE = 20
    NO_CELL_H = 50
    BRIGHTNESS_MODIFIER = 1.2
    __CORRECTION_FACTOR = math.pi * 1/4 

    # camera world
    position_vector = None
    map = None
    skybox = None
    # camera variables
    fov = 0
    raycount = 0
    draw_dist = 0
    delta_ang =0
    z_buffer = []
    # internal surface to draw to
    int_w = 0
    int_h = 0
    midpoint = 0
    internal_surface = None
    # external surface to scale/return
    ext_w = 0
    ext_h = 0
    external_surface = None
    x_ray = False

    def __init__(self, map, camera_man, w, h, ray_count, fov, draw_dist, sprites, ignore_bounds = False):
        # set up location
        self.position_vector = camera_man
        self.map = map
        # set up camera variables
        self.fov = fov
        self.half_fov = fov/2
        self.raycount = ray_count
        self.draw_dist = draw_dist
        self.delta_ang = fov/ray_count
        self.int_w = ray_count
        self.int_h = h
        self.midpoint = self.int_h/2
        self.max_sprite_w = self.int_w << 3
        self.max_sprite_h = self.int_h << 3
        self.internal_surface = pygame.Surface((self.int_w, self.int_h))
        self.ext_w = w
        self.ext_h = h
        self.external_surface = pygame.Surface((self.ext_w, self.ext_h))
        self.z_buffer = [0] * self.raycount
        self.objects = sprites
        self.object_w_factor = (math.pi/(self.fov * 4))
        self.ignore_bounds = ignore_bounds
        if self.map.has_skybox:
            sky = self.map.get_skybox()
            self.skybox = texture.RollingTexture(sky[0],sky[1],self.fov, self.int_w, self.int_h/2)
        # print statement
        log.write("Set up camera at ("+str(camera_man.x)+","+str(camera_man.y)
              +") with a " + str(math.degrees(self.fov)) + 
              " degree FOV and casting " + str(self.raycount) +" rays out to " 
              + str(self.draw_dist) +" cells")

    def render(self):
        pygame.draw.rect(self.internal_surface, (35,35,35), (0,self.midpoint-self.NO_CELL_H, self.int_w, 2 * self.NO_CELL_H))
        # render skybox (if applicable)
        if self.map.has_skybox:
            self.skybox.render(self.position_vector.ang)
            self.internal_surface.blit(self.skybox.external_screen)
        # render walls/floor/ceiling
        ang = self.position_vector.ang - self.half_fov
        for i in range(self.raycount):
            ang %= 2 * math.pi
            if ang < 0:
                ang += 2 * math.pi
            self.__cast__(ang, i)
            ang += self.delta_ang
        # render sprites
        self.__render_objects__()
        # scale picture for output
        pygame.transform.scale(self.internal_surface, (self.ext_w,self.ext_h), self.external_surface)
        

    def __distance__ (self,x, y, x1, y1):
        return math.dist((x,y), (x1,y1))

    #@functools.cache
    def __apply_brightness__ (self, dist, color):
        scale = self.BRIGHTNESS_MODIFIER * (1 - dist/self.draw_dist)
        return (utils.clamp_multiplication(color[0], scale, 255, 0), 
                utils.clamp_multiplication(color[1], scale, 255, 0), 
                utils.clamp_multiplication(color[2], scale, 255, 0))

    #@functools.cache
    def __cast__ (self, ang, ray_offset):
        ang_check = ang%(math.pi/2) > self.MARGIN_OF_ERROR
        if (ang_check):
            ang += self.MARGIN_OF_ERROR
        offset = -1
        x0 = self.position_vector.x
        y0 = self.position_vector.y
        x = x0
        y = y0
        dy = abs(math.tan(ang))
        if dy == 0:
            dy = self.MARGIN_OF_ERROR
        dx = 1/dy
        d2x = self.CAST_OFFSET * math.cos(ang)
        d2y = self.CAST_OFFSET * math.sin(ang)
        x_increase = 1
        y_increase = 1
        if ang > math.pi:
           y_increase = -1
        if ang > math.pi/2 and ang < math.pi * 3/2:
            x_increase = -1
        distance = self.__distance__(x,y,x0,y0)
        draw_height = 0
        step = self.MAX_CELL_TRAVERSE # number of cells before we just quit
        # for tiling floor/ceiling:
        prev_y_up = self.int_h
        prev_y_down = self.midpoint
        prev_color_down = -1
        prev_color_up = self.map.get_floor_text(x,y)
        if self.map.has_ceil:
            prev_color_down = self.map.get_ceil_text(x,y)
        correction = math.cos(self.__CORRECTION_FACTOR * (0.5 - ray_offset/self.raycount))
        # enter cast
        #print("\n\nstart:")
        while distance <= self.draw_dist and step > 0:
            step -= 1
            if self.map.is_valid(x,y):
                if distance != 0:
                    # draw ceil/map
                    delta_h = self.midpoint + draw_height
                    pygame.draw.line(self.internal_surface, self.__apply_brightness__(distance, prev_color_up), 
                                     (ray_offset, prev_y_up + self.position_vector.z), 
                                     (ray_offset, delta_h + self.position_vector.z))
                    prev_y_up = delta_h
                    if (self.map.has_ceil and prev_color_down != self.map.TRANS):
                        delta_h = self.midpoint - draw_height
                        pygame.draw.line(self.internal_surface, self.__apply_brightness__(distance, prev_color_down) , 
                                         (ray_offset, prev_y_down + self.position_vector.z), 
                                         (ray_offset, delta_h + self.position_vector.z))
                        prev_y_down = delta_h
                if not self.map.is_empty(x,y):
                    # hit wall, set up parameters to draw wall
                    offset_x = abs(x - int(x))
                    if offset_x > 0.5:
                        offset_x = 1 - offset_x
                    offset_y = abs(y - int(y))
                    if offset_y > 0.5:
                        offset_y = 1 - offset_y
                    offset = abs(y - int (y))
                    if offset_y < offset_x:
                        offset = abs(x - int (x))
                    break
                prev_color_up = self.map.get_floor_text(x,y)
                if self.map.has_ceil:
                    prev_color_down = self.map.get_ceil_text(x,y)
            else:
                self.z_buffer[ray_offset] = -1
                return
            # move on to next grid cell
                
            x_n = 1 + math.floor(x) - x
            if x_increase < 0:
                x_n = x -  math.floor(x)
            proj_y = y + dy * x_n * y_increase
            x =  math.floor(x)
            if (x_increase > 0):
                x += 1
            if proj_y <  math.floor(y) + 1 and proj_y >  math.floor(y):
                y = proj_y
            else:
                y =  math.floor(y)
                if (y_increase > 0):
                    y += 1
                x -= abs(y-proj_y) * dx * x_increase
            #print(x,y)
            x += d2x
            y += d2y
            #print(x,y)
            distance = self.__distance__(x,y,x0,y0) * correction
            draw_height = self.int_h/(2 * distance)
            if draw_height > self.midpoint:
                draw_height = self.midpoint
                
            
        # out of cast
        if offset != -1:
            # we hit a wall
            self.z_buffer[ray_offset] = distance
            height = self.map.get_height(x,y)
            scale = height * 2 - 1
            top = (ray_offset, self.midpoint - scale * draw_height + self.position_vector.z)
            self.internal_surface.blit(pygame.transform.scale(self.map.get_text(x,y,offset), (1,2 * draw_height * height)),top)
        else:
            self.z_buffer[ray_offset] = -1
    
    def __check_sprite_visiblity__ (self, min, max):        
        return not ((min < 0 and max < 0) or (min > self.int_w and max > self.int_w))

    def __render_objects__(self):
        x0 = self.position_vector.x
        y0 = self.position_vector.y
        cam_min = self.position_vector.ang - self.fov/2
        draw_me = []
        # find all sprits in fov and add them to a queue to draw
        for sprite in self.objects:
            x = sprite.x()
            y = sprite.y()
            #make sure sprite is within draw distance
            distance_to_sprite = self.__distance__(x0,y0,x,y)
            if (distance_to_sprite <= self.MARGIN_OF_ERROR):
                distance_to_sprite = self.MARGIN_OF_ERROR
            if distance_to_sprite < self.draw_dist:
                w = int(self.int_w * (sprite.w/distance_to_sprite)* self.object_w_factor)  # not sure why I have to divide by 2 here, but I do
                h = int(self.int_h * (sprite.h/distance_to_sprite))
                if (w > self.max_sprite_w):
                    w = self.max_sprite_w
                if (h > self.max_sprite_h):
                    h = self.max_sprite_h
                raw_ang= utils.get_angle(x0,y0,x,y)
                ang_to_sprite = (raw_ang - cam_min) % (2 * math.pi)
                ang_to_sprite/=self.delta_ang 
                sprite_min = int(ang_to_sprite - w/2)
                sprite_max = int(ang_to_sprite + w/2)
                # make sure at least some of the sprite is visible to the camera
                if (self.__check_sprite_visiblity__(sprite_min,sprite_max)):
                    # we can see this sprite so add to queue
                    draw_me.append((distance_to_sprite, sprite, raw_ang,sprite_min,sprite_max, w, h))
        # sort so drawing queue is in descending order (no longer a queue I suppose)
        # draws sprites in order via painters algo.
        draw_me.sort(key = lambda obj : obj[0], reverse = True)
        # draw elements in queue
        for tup in draw_me:
            # pull out sprite from queue
            # not the most elegant solution, but whatever
            distance_to_sprite = tup[0]
            sprite = tup[1]
            w = tup [5]
            h = tup [6]
            delta = 0
            start = tup[3]
            floor = self.int_h * (0.5 -sprite.z())/distance_to_sprite
            if (start < 0):
                start =0
                delta = abs(tup[3])
            end = tup[4]
            if (end > self.int_w):
                end = self.int_w
            # find all slices of a sprite we can see
            to_draw = []
            in_drawing = False
            frame = [0,0,0]
            for i in range (start, end):
                z = self.z_buffer[i]
                if z == -1 or z > distance_to_sprite or self.x_ray:
                    if not in_drawing:
                        in_drawing = True
                        frame[0] = delta
                        frame[2] = i
                elif in_drawing:
                    in_drawing = False
                    frame[1] = delta
                    to_draw.append(frame)
                delta += 1
            if in_drawing:
                frame[1] = delta
                to_draw.append(frame)
            # draw the slices if we have any
            if (len(to_draw) > 0):
                top = self.int_h/2 + floor - h + self.position_vector.z
                image = sprite.get_sprite(w,h,tup[2])
                for frame in to_draw:
                    slice_w = frame[1] - frame[0] 
                    if (slice_w > w):
                        slice_w = w
                    slice = image.subsurface((frame[0], 0, slice_w, h))
                    self.internal_surface.blit(slice, (frame[2], top))