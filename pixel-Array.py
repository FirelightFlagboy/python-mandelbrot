from time import sleep

import pygame

HEIGHT = 255
WIDTH = 255

pygame.init()

# create a windows
windows = pygame.display.set_mode((WIDTH, HEIGHT))
# create a surface
surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.flip()

# get pixel array
pxa = pygame.PixelArray( surface )

# create a gradien black to white
for c in range(HEIGHT):
	r, g, b = c, c, c # create rgb color code
	pxa[:, c] = (r, g, b) # set the color for the whole line

del pxa

# set color of the windows white
windows.fill((255, 255, 255))
# add the gradient to the windows
windows.blit(surface, (0, 0))

pygame.display.flip()

run = True
while run:
	event = pygame.event.get()
	for ev in event:
		type_event = ev.type
		if type_event is pygame.QUIT:
			run = False
