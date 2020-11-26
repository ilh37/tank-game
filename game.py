import pygame, sys, math, time, random, traceback
from baseobjects import *
from units import *
from maps import *

# List of other objects
GAME_OBJECTS = []

DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Represents position of mouse (updated in mouseMotion)
MOUSE = [0,0]

# Interval between draw/update cycles
fpsClock = pygame.time.Clock()

MISSIONS = [Map1] * 100

def draw_button(display_surf,text,rect,color=GREEN,mouseover_color=LIGHT_GREEN, fontsize=30):
    if on_button(rect):
        pygame.draw.rect(display_surf,mouseover_color,rect)
    else:
        pygame.draw.rect(display_surf,color,rect)

    font = pygame.font.Font('freesansbold.ttf',fontsize)
    textSurf, textRect = text_objects(text,font)
    textRect.center = rect.center
    display_surf.blit(textSurf,textRect)
    

def on_button(rect):
    return rect.collidepoint(pygame.mouse.get_pos())

# Main menu screen (for settings, saveloading)
def main_menu():
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Tanks!')

    startgame_rect = pygame.Rect(0,0,300,50)
    startgame_rect.center = (800,500)
    quit_rect = pygame.Rect(0,0,300,50)
    quit_rect.center = (800,575)

    largeText = pygame.font.Font('freesansbold.ttf',80)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEMOTION:
                pass
                #mouseMotion(event,None)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if on_button(startgame_rect):
                    return game_menu()
                if on_button(quit_rect):
                    return None

        DISPLAY_SURF.fill(WHITE)
        textSurf, textRect = text_objects("Tanks!", largeText)
        textRect.center = (800,400)
        DISPLAY_SURF.blit(textSurf, textRect)

        draw_button(DISPLAY_SURF,"Start Game",startgame_rect)
        draw_button(DISPLAY_SURF,"Quit",quit_rect,color=RED,mouseover_color=LIGHT_RED)
        
        pygame.display.update()

        fpsClock.tick(round(1000/FPS))

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

# Menu screen between missions
# Represents a single playthrough
LEVEL_TL = (500,200)
LEVEL_SIZE = 60
LEVEL_ROW_NUMS = 10

def game_menu():
    mission_buttons = [None] * len(MISSIONS)
    mediumFont = pygame.font.Font('freesansbold.ttf', 50)
    largeFont = pygame.font.Font('freesansbold.ttf',80)
    for i in range(len(mission_buttons)):
        r = pygame.Rect(LEVEL_TL[0] + LEVEL_SIZE * (i % LEVEL_ROW_NUMS),
                                         LEVEL_TL[1] + LEVEL_SIZE * (i // LEVEL_ROW_NUMS),
                                         LEVEL_SIZE, LEVEL_SIZE)
        mission_buttons[i] = (r,i+1)
    
    while True:
        DISPLAY_SURF.fill(WHITE)
        
        textSurf, textRect = text_objects("Levels", largeFont)
        textRect.center = (800,100)
        DISPLAY_SURF.blit(textSurf, textRect)
        
        for r,i in mission_buttons:
            draw_button(DISPLAY_SURF, str(i), r, color=GRAY, mouseover_color=LIGHT_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for r,i in mission_buttons:
                    if on_button(r):
                        return game_loop(MISSIONS[i-1])
        
        pygame.display.update()
        fpsClock.tick(round(1000/FPS))
        
        

# Game loop
def game_loop(map_class):
    if map_class is None:
        return main_menu
    game = map_class(bounds=(WINDOW_WIDTH,WINDOW_HEIGHT),player=PlayerTank(location=(960,540)))
    game.load_data()
    
    #DISPLAY_SURF = pygame.display.set_mode(game.bounds)
    draw(game)
    while True:
        # Handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            #elif event.type == pygame.MOUSEMOTION:
                #mouseMotion(event,game)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseButton(event,game)
        keyPress(game)
        update(game)
        draw(game)
        fpsClock.tick(round(1000/FPS))

        if game.is_lost():
            return end_mission(win=False)
        if game.is_won():
            return end_mission(win=True)

# Screen displayed at the end of a game
def end_mission(win):
    show = True
    #DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    #pygame.display.set_caption('Tanks!')

    display_str = "DEFEAT"
    if win:
        display_str = "VICTORY"
    
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                show = False

        DISPLAY_SURF.fill(WHITE)
        smallText = pygame.font.Font('freesansbold.ttf',80)
        smallTextSurf, smallTextRect = text_objects(display_str,smallText)
        smallTextRect.center = ((WINDOW_WIDTH/2),(WINDOW_HEIGHT/2))
        DISPLAY_SURF.blit(smallTextSurf, smallTextRect)
        pygame.display.update()

        fpsClock.tick(round(1000/FPS))

    return main_menu

# Handle user input
def keyPress(game):
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_d]):
        game.player_tank.moveX(5)
    elif(keys[pygame.K_a]):
        game.player_tank.moveX(-5)
    elif(keys[pygame.K_w]):
        game.player_tank.moveY(-5)
    elif(keys[pygame.K_s]):
        game.player_tank.moveY(5)


def mouseButton(event,game):
    # Left mouse button
    if event.button == 1:
        game.player_tank.shoot()
    # Right mouse button (test forcefield)
    #if event.button == 3:
        #game.spawn(ForceField((MOUSE[0],MOUSE[1]),2000))
    

# Main method that updates the state of all objects
def update(game):
    # Update all objects
    game.update()
    
    # Clean up dead objects and add new objects
    game.clear_dead()
    game.spawns(get_spawn_objects())

# Main method that draws all objects
def draw(game):
    game.draw(DISPLAY_SURF)

def main():
    pygame.init()
    try:
        # Mode represents the next function to run: each mode returns the next one to run
        mode = main_menu
        while mode:
            mode = mode()
    except:
        # Absolute last resort
        print(traceback.format_exc())
    finally:
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    main()
