import map
import math
import texture
import pygame

class Camera:
    # camera constants
    CAST_OFFSET = 0.00001
    MARGIN_OF_ERROR = 0.0001
    MAX_CELL_TRAVERSE = 20

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

    def __init__(self, map, camera_man, w, h, ray_count, fov, draw_dist):
        # set up location
        self.position_vector = camera_man
        self.map = map
        # set up camera variables
        self.fov = fov
        self.raycount = ray_count
        self.draw_dist = draw_dist
        self.delta_ang = fov/ray_count
        self.int_w = ray_count
        self.int_h = h
        self.midpoint = self.int_h/2
        self.internal_surface = pygame.Surface((self.int_w, self.int_h))
        self.ext_w = w
        self.ext_h = h
        self.external_surface = pygame.Surface((self.ext_w, self.ext_h))
        self.z_buffer = [0] * self.raycount
        if not self.map.has_ceil:
            sky = self.map.get_skybox()
            self.skybox = texture.RollingTexture(sky[0],sky[1],self.fov, self.int_w, self.int_h/2)
        # print statement
        print("Set up camera at ("+str(camera_man.x)+","+str(camera_man.y)
              +") with a " + str(math.degrees(self.fov)) + 
              " degree FOV and casting " + str(self.raycount) +" rays out to " 
              + str(self.draw_dist) +" cells")

    def render(self):
        self.internal_surface.fill((35,35,35))
        if not self.map.has_ceil:
            self.skybox.render(self.position_vector.ang)
            self.internal_surface.blit(self.skybox.external_screen)
        ang = self.position_vector.ang - self.fov/2
        for i in range(self.raycount):
            ang %= 2 * math.pi
            if ang < 0:
                ang += 2 * math.pi
            self.__cast__(ang, i)
            ang += self.delta_ang
        # scale picture for output
        pygame.transform.smoothscale(self.internal_surface, (self.ext_w,self.ext_h), self.external_surface)
        

    def __distance__ (self,x, y, x1, y1):
        return math.dist((x,y), (x1,y1))

    def __cast__ (self, ang, ray_offset):
        ang_check = ang%(math.pi/2) > self.MARGIN_OF_ERROR
        if (ang_check):
            ang += self.delta_ang
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
        # enter cast
        while distance <= self.draw_dist and step > 0:
            step -= 1
            if self.map.is_valid(x,y):
                if distance != 0:
                    # draw ceil/map
                    delta_h = self.midpoint + draw_height
                    pygame.draw.line(self.internal_surface, prev_color_up, 
                                     (ray_offset, prev_y_up + self.position_vector.z), 
                                     (ray_offset, delta_h + self.position_vector.z))
                    prev_y_up = delta_h
                    if (self.map.has_ceil):
                        delta_h = self.midpoint - draw_height
                        pygame.draw.line(self.internal_surface, prev_color_down , 
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
            # move on to next grid cell
            x_n = 1 + int(x) - x
            if x_increase < 0:
                 x_n = x - int(x)
            proj_y = y + dy * x_n * y_increase
            if (ang_check):
                x = int(x)
                if (x_increase > 0):
                    x += 1
            if proj_y < int(y) + 1 and proj_y > int(y):
                y = proj_y
            else:
                y = int(y)
                if (y_increase > 0):
                    y += 1
                if ang_check:
                    x -= abs(y-proj_y) * dx * x_increase
            x += d2x
            y += d2y
            distance = self.__distance__(x,y,x0,y0)
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
            #pygame.draw.line(self.internal_surface,(255 * offset, 0, 255), (ray_offset, self.midpoint + draw_height), top)
            self.internal_surface.blit(pygame.transform.scale(self.map.get_text(x,y,offset), (1,2 * draw_height * height)),top)
        else:
            self.z_buffer[ray_offset] = -1