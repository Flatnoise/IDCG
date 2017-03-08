import os
import json
import argparse
import idcg_common
import pygame
from pygame.locals import *
import time
from os import path

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)


class StarSprite(pygame.sprite.Sprite):
    """
    Picture of star
    Derives from pygame's sprite class
    """
    def __init__(self, sid, image):
        # Call the parent class (Sprite) constructor
        # pygame.sprite.RenderClear.__init__(self)
        super().__init__()

        self.image = pygame.image.load(image)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        # Adding ID. ID for sprite has the same number as ID of star system
        self.id = sid

class StarTextSprite(pygame.sprite.Sprite):
    """
    Star name, written below star's sprite
    Derives from pygame's sprite class
    """
    def __init__(self, sid, text, size, textcolor, backcolor):
        # Call the parent class (Sprite) constructor
        # pygame.sprite.RenderClear.__init__(self)
        super().__init__()

        self.font = pygame.font.SysFont("Arial", size)
        self.image = self.font.render(text, True, textcolor, backcolor)
        self.rect = self.image.get_rect()

        # Adding ID. ID for sprite has the same number as ID of star system
        self.id = sid

#Parsing command-line parameters
# USAGE: simple_viewer.py -i <SAVEFILE> [optional parameters]
#
#
#
#
parser = argparse.ArgumentParser(description="Simple Galaxy Viewer for IDCG",
                                 usage='simple_viewer.py -i SAVEFILE [options]')
parser.add_argument('-x', help="Screen width, default 1024", type=int, default=1024)
parser.add_argument('-y', help="Screen height, default 768", type=int, default=870)
parser.add_argument('-i', help="Input file", default='new_galaxy.json')
args = parser.parse_args()

# Determining directories
dir_main = path.dirname(os.path.realpath(__file__))
dir_resources = path.join(dir_main, 'resources')
dir_images = path.join(dir_resources, 'images')
json_input_filename = path.join(dir_main, args.i)


# Creating list of star systems and load JSON with data
stars = []
with open(args.i,'r') as json_input:
    json_data = json.load(json_input)
    json_input.close()

# Importing stars data from input savefile to list of stars
for item in json_data:
    stars.append(idcg_common.import_star(item))





# Initialize Pygame
pygame.init()

# Scaling variables
grid_x = 120
grid_y = 120
shift_x = -30
shift_y = -30
fl_quit = False
scroll_speed = 15
is_scrolled = False     # flag. True if scrolling key was pressed

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Screen initialisation
screen = pygame.display.set_mode([args.x, args.y])

# Creating sprite group
stars_sprites_list = pygame.sprite.Group()
stars_text_sprites_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


# Creating sprite for each star system
for star in stars:

    # Put correct image depending on star type
    if star.star_type == 1:
        star_image = path.join(dir_images, 'icon_star_o.png')
    elif star.star_type == 2:
        star_image = path.join(dir_images, 'icon_star_a.png')
    elif star.star_type == 3:
        star_image = path.join(dir_images, 'icon_star_b.png')
    elif star.star_type == 4:
        star_image = path.join(dir_images, 'icon_star_f.png')
    elif star.star_type == 5:
        star_image = path.join(dir_images, 'icon_star_g.png')
    elif star.star_type == 6:
        star_image = path.join(dir_images, 'icon_star_k.png')
    elif star.star_type == 7:
        star_image = path.join(dir_images, 'icon_star_m.png')
    else:
        star_image = path.join(dir_images, 'icon_star_m.png')

    # Creating star sprite and adding coordinates
    star_sprite = StarSprite(star.id, star_image)
    star_sprite.rect.x = star.x * grid_x + shift_x
    star_sprite.rect.y = star.y * grid_y + shift_y

    # Creating star name sprite and adding coordinates
    text_sprite = StarTextSprite(star.id, star.name, 12, WHITE, BLACK)
    text_sprite.rect.x = star.x * grid_x + shift_x
    text_sprite.rect.y = star.y * grid_y + shift_y + 50

    # Add this sprite to groups
    stars_sprites_list.add(star_sprite)
    stars_text_sprites_list.add(text_sprite)

    all_sprites_list.add(star_sprite)
    all_sprites_list.add(text_sprite)



while not fl_quit:
    # User input
    for event in pygame.event.get():
        # Keybord detection
        if event.type == pygame.KEYDOWN:
            # Quit this for cycle and loop above if escape key pressed
            if event.key == K_ESCAPE:
                fl_quit = True
                break

            # Scrolling keys
            elif event.key == K_UP:
                shift_y += scroll_speed
                is_scrolled = True
            elif event.key == K_DOWN:
                shift_y -= scroll_speed
                is_scrolled = True
            elif event.key == K_LEFT:
                shift_x += scroll_speed
                is_scrolled = True
            elif event.key == K_RIGHT:
                shift_x -= scroll_speed
                is_scrolled = True

            # Recalculate all coordinates if screen is scrolled
            if is_scrolled:
                is_scrolled = False
                # Looking for element with particular ID in list of stars
                for index, star in enumerate(stars):
                    for s in stars_sprites_list:
                        if star.id == s.id:
                            # Recalculating coordinates
                            s.rect.x = stars[index].x * grid_x + shift_x
                            s.rect.y = stars[index].y * grid_y + shift_y

                    for s in stars_text_sprites_list:
                        if star.id == s.id:
                            # Recalculating coordinates
                            s.rect.x = stars[index].x * grid_x + shift_x
                            s.rect.y = stars[index].y * grid_y + shift_y + 50


        # Mouse detection
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            # Loop througt all sprites
            for s in stars_sprites_list:
                if s.rect.collidepoint(pos):
                    if event.button == 1:
                        print (stars[s.id])



    # Drawing all sprites
    screen.fill(BLACK)
    all_sprites_list.draw(screen)
    pygame.display.flip()

    # End of loop. Tick the clock
    clock.tick(60)


pygame.quit()