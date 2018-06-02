import pygame
from display import Display

# windows parameters
HEIGTH = 360
WIDTH = 480
SIZE = (WIDTH, HEIGTH)

# fractale parameters
INFINI = 16.0
max_iter = 50
zoom = 1.0
coord_set = {
	'x1': -2.0,
	'x2': 2.0,
	'y1': -2.0,
	'y2': 2.0,
}
refresh = [
	pygame.K_UP,
	pygame.K_DOWN,
	pygame.K_LEFT,
	pygame.K_RIGHT,
	pygame.K_PAGEDOWN,
	pygame.K_PAGEUP,
]

coord_set['width'] = coord_set['x2'] - coord_set['x1']
coord_set['heigth'] = coord_set['y2'] - coord_set['y1']

display = Display(WIDTH, HEIGTH)


def getIter(x, y):
	Cr = coord_set['width'] * x / WIDTH + coord_set['x1'] - 0.5
	Ci = coord_set['heigth'] * y / HEIGTH + coord_set['y1']

	aa, bb, a, b = 0.0, 0.0, Cr, Ci
	for i in range(max_iter):
		aa = a * a - b * b
		bb = 2.0 * a * b
		a = aa + Cr
		b = bb + Ci
		if abs(a + b) > INFINI:
			break
	return (i)


def draw():
	ar = display.getPixelArray()
	for c in range(HEIGTH):
		for r in range(WIDTH):
			iteration = getIter(r, c)
			brigth = (iteration / max_iter) * 255
			if iteration is max_iter:
				ar[r, c] = 0xffffff
			else:
				ar[r, c] = 0, 0, 255 - brigth
		print('\r', round(c * 100 / HEIGTH), '%', end='')
	print('\r', round(c * 100 / HEIGTH), '%\tdone')

	del ar

	display.blitSurface()

def handleKeyDown(key):
	global max_iter
	global coord_set

	if key not in refresh:
		return

	if key == pygame.K_PAGEUP:
		max_iter = round(max_iter * 1.5)
	elif key == pygame.K_PAGEDOWN:
		max_iter = round(max_iter / 1.5)
	elif key == pygame.K_UP:
		move = 0.2 / zoom
		coord_set['y1'] += move
		coord_set['y2'] += move
	elif key == pygame.K_DOWN:
		move = 0.2 / zoom
		coord_set['y1'] -= move
		coord_set['y2'] -= move
	elif key == pygame.K_LEFT:
		move = 0.25 / zoom
		coord_set['x1'] += move
		coord_set['x2'] += move
	elif key == pygame.K_RIGHT:
		move = 0.25 / zoom
		coord_set['x1'] -= move
		coord_set['x2'] -= move

	draw()

def handleMouse(button):
	global zoom
	global coord_set

	if button is not 1 and button is not 3:
		return

	if button == 1:
		zoom *= 1.1
	elif button == 3:
		zoom /= 1.1

	print('zoom', zoom)
	coord_set['x1'] /= zoom
	coord_set['x2'] /= zoom
	coord_set['y1'] /= zoom
	coord_set['y2'] /= zoom

	coord_set['width'] = coord_set['x2'] - coord_set['x1']
	coord_set['heigth'] = coord_set['y2'] - coord_set['y1']

	print('coord', coord_set)
	draw()

def eventHandler(type_event, event):

	if type_event is pygame.QUIT:
		print('quit')
		return True
	if type_event is pygame.KEYDOWN:
		handleKeyDown(event.key)
	elif type_event is pygame.MOUSEBUTTONDOWN:
		handleMouse(event.button)

def main():

	display.initSurface()

	draw()

	display.listenEvent(eventHandler)

if __name__ == '__main__':
	main()
