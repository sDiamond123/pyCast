import pygame
import world


if __name__ == "__main__":
    # pygame setup
    pygame.init()

    # read in config file and set w/h
    config = open("data\config\config.txt", "r")
    config.readline()
    name = config.readline().strip()
    pygame.display.set_caption(name)
    config.readline()
    fullscreen = "true" == (config.readline().strip().lower())
    config.readline()
    w = int(config.readline())
    config.readline()
    h = int(config.readline())
    config.readline()
    fps = int(config.readline())
    config.readline()
    i_w = int(config.readline())
    config.readline()
    i_h = int(config.readline())
    config.close()

    #print out config to terminal
    print ("Started: "+name+"\nWindow: " + str(w) + " by " + str(h) +"\nFullscreen: "+str(fullscreen)+
           "\nInternal Resolution: "+str(i_w)+" by "+ str(i_h)+"\nTargeting " + str(fps) +" FPS")

    # finish pygame init
    if not fullscreen:
        screen = pygame.display.set_mode((w, h))
    else:
        screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    running = True
    dt = 0

    manager = world.World(screen,w,h,i_w, i_h, "default.csv")
    print("Game Start!")
    # main loop
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # run a frame of the game
        keys = pygame.key.get_pressed()
        if running:
            running = manager.update(keys)
            manager.render()

        # push frame to screen
        pygame.display.flip()

        # limits FPS
        dt = clock.tick(fps) / 1000
    print("Exited: " + name)
    pygame.quit()