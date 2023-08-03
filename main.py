import pygame
from Level1 import Level1
from dataclasses import dataclass
from GameObject import MovingObject


@dataclass
class StartVars:
    X, Y = 1280, 720
    fps = 60
    clock = pygame.time.Clock()


# Init all Modules

pygame.init()

# Window init
window = pygame.display.set_mode((StartVars.X, StartVars.Y))
glorious_leader = pygame.image.load("zie_zie_ping_公鸡.jpg").convert()
pygame.display.set_icon(glorious_leader)
pygame.display.set_caption("这 事物")

update_lvl_id = pygame.USEREVENT + 2
update_half_lvl_event = pygame.event.Event(update_lvl_id, subtype=0.5)
update_lvl_event = pygame.event.Event(update_lvl_id, subtype=1)
pygame.time.set_timer(update_half_lvl_event, millis=8100, loops=1)

# Game loop
curr_lvl = 0.5


def level_loader():
    global curr_lvl
    if curr_lvl == 0.5:
        Level1.lvl1_pregame(window)
    elif curr_lvl == 1:
        Level1.lvl1_start(window)


level_loader()

while True:
    window.fill((0, 0, 0))  # Replace with background game object
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == update_lvl_id:
            curr_lvl += event.subtype
            level_loader()

        if curr_lvl == 0.5:
            pass
        elif curr_lvl == 1:
            Level1.lvl1_event_loop(event)

    if curr_lvl == 0.5:
        Level1.pregame_loop(window)
    elif curr_lvl == 1:
        Level1.loop(window)

    pygame.display.flip()
    StartVars.clock.tick(StartVars.fps)
