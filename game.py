import pygame, sys, math, time, random, traceback
from baseobjects import *
from units import *

# Display surface
DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# List of other objects
GAME_OBJECTS = []

# Represents position of mouse (updated in mouseMotion)
MOUSE = [0,0]

# Interval between draw/update cycles
fpsClock = pygame.time.Clock()

# Main menu screen (for settings, saveloading)
def main_menu():
    show = True
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tanks!')
    
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                show = False

        DISPLAY_SURF.fill(WHITE)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        smallText = pygame.font.Font('freesansbold.ttf',30)
        textSurf, textRect = text_objects("Tanks!", largeText)
        smallTextSurf, smallTextRect = text_objects("Click to start",smallText)
        textRect.center = ((WINDOW_WIDTH/2),(WINDOW_HEIGHT/2))
        smallTextRect.center = ((WINDOW_WIDTH/2),(WINDOW_HEIGHT/2)+70)
        DISPLAY_SURF.blit(textSurf, textRect)
        DISPLAY_SURF.blit(smallTextSurf, smallTextRect)
        pygame.display.update()

        fpsClock.tick(round(1000/FPS))

    return game_loop

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

# Menu screen between missions
# Represents a single playthrough
def game_menu():
    pass

# Map class to handle all ingame objects
class Map():
    def __init__(self,bounds,player):
        self.game_objects = []
        self.bounds = bounds
        self.player_tank = player
        self.game_objects.append(player)

    def spawns(self,objs):
        self.game_objects.extend(objs)

    def clear_dead(self):
        self.game_objects = list(filter(lambda x: not x.is_dead, self.game_objects))

# Game loop
def game_loop():
    global PLAYER_TANK, GAME_OBJECTS
    PLAYER_TANK = PlayerTank((960,540))

    enemy = DummyTank((600,300))
    GAME_OBJECTS.append(Crate((700,500)))
    GAME_OBJECTS.append(Crate((800,400)))
    GAME_OBJECTS.append(enemy)

    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tanks!')
    draw()
    while True:
        # Handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouseMotion(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseButton(event)
        keyPress()
        update()
        draw()
        fpsClock.tick(round(1000/FPS))

        if PLAYER_TANK.is_dead is True:
            # Eventually remove these global variables entirely
            GAME_OBJECTS = []
            return end_mission(win=False)
        if enemy.is_dead:
            GAME_OBJECTS = []
            return end_mission(win=True)

def end_mission(win):
    show = True
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tanks!')

    display_str = "How the fuck did you just die? You know what, just click and start again. Try not to be stupid this time!"
    if win:
        display_str = "VICTORY"
    
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                show = False
                if win:
                    return None

        DISPLAY_SURF.fill(WHITE)
        smallText = pygame.font.Font('freesansbold.ttf',30)
        smallTextSurf, smallTextRect = text_objects(display_str,smallText)
        smallTextRect.center = ((WINDOW_WIDTH/2),(WINDOW_HEIGHT/2))
        DISPLAY_SURF.blit(smallTextSurf, smallTextRect)
        pygame.display.update()

        fpsClock.tick(round(1000/FPS))

    return game_loop

# Handle user input
def keyPress():
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_d]):
        PLAYER_TANK.moveX(5)
    elif(keys[pygame.K_a]):
        PLAYER_TANK.moveX(-5)
    elif(keys[pygame.K_w]):
        PLAYER_TANK.moveY(-5)
    elif(keys[pygame.K_s]):
        PLAYER_TANK.moveY(5)

# Update position of mouse
def mouseMotion(event):
    mouse_pos = pygame.mouse.get_pos()
    MOUSE[0] = mouse_pos[0]
    MOUSE[1] = mouse_pos[1]

def mouseButton(event):
    # Left mouse button
    if event.button == 1:
        PLAYER_TANK.shoot()

# Main method that updates the state of all objects
def update():
    global GAME_OBJECTS
    
    # Update all objects
    if not PLAYER_TANK.is_dead:
        PLAYER_TANK.update()
    for obj in GAME_OBJECTS:
        obj.update()

    if PLAYER_TANK.is_dead:
        all_objects = GAME_OBJECTS
    else:
        all_objects = GAME_OBJECTS + [PLAYER_TANK]
    # Deal with collisions
    for obj1 in all_objects:
        for obj2 in all_objects:
            if obj1 != obj2 and colliding(obj1,obj2):
                obj1.on_collide(obj2)
    
    # Clean up dead objects and add new objects
    GAME_OBJECTS = list(filter(lambda x: not x.is_dead, GAME_OBJECTS))
    GAME_OBJECTS.extend(get_spawn_objects())
    SPAWN_GAME_OBJECTS.clear()

# Main method that draws all objects
def draw():
    DISPLAY_SURF.fill(WHITE)
    
    for obj in GAME_OBJECTS:
        obj.draw(DISPLAY_SURF)
    if not PLAYER_TANK.is_dead:
        PLAYER_TANK.draw(DISPLAY_SURF)
    pygame.display.update()

def main():
    pygame.init()
    try:
        # Mode represents the next function to run: each mode returns the next one to run
        mode = main_menu
        while mode:
            mode = mode()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    main()
