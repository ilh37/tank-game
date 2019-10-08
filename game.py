import pygame, sys, math, time, random
from baseobjects import *
from units import *

# Global constants

# Represents position of mouse (updated in mouseMotion)
MOUSE = [0,0]

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

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

# Menu screen between missions
# Represents a single playthrough
def game_menu():
    pass

# Game loop
def game_loop():
    global PLAYER_TANK
    PLAYER_TANK = PlayerTank((960,540))

    GAME_OBJECTS.append(Crate((700,500)))
    GAME_OBJECTS.append(Crate((800,400)))
    GAME_OBJECTS.append(DummyTank((600,300)))

    fpsClock = pygame.time.Clock()

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
    GAME_OBJECTS.extend(SPAWN_GAME_OBJECTS)
    SPAWN_GAME_OBJECTS.clear()

# Main method that draws all objects
def draw():
    DISPLAY_SURF.fill(WHITE)
    if not PLAYER_TANK.is_dead:
        PLAYER_TANK.draw(DISPLAY_SURF)
    
    for obj in GAME_OBJECTS:
        obj.draw(DISPLAY_SURF)
    pygame.display.update()

# Checks if two GameObjects collide
def colliding(obj1,obj2):
    # Quickly remove obvious cases: if bounding rects don't collide
    if not obj1.rect.colliderect(obj2.rect):
        return False
    # Then compare bitmasks
    mask1 = pygame.mask.from_surface(obj1.image,0)
    mask2 = pygame.mask.from_surface(obj2.image,0)
    
    dx = obj2.rect.topleft[0] - obj1.rect.topleft[0]
    dy = obj2.rect.topleft[1] - obj1.rect.topleft[1]
    return mask1.overlap_area(mask2,(dx,dy)) > 0

def main():
    pygame.init()
    main_menu()
    game_loop()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
