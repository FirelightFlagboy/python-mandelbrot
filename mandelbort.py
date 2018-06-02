import pygame
from display import Display

# windows parameters
HEIGTH = 360
WIDTH = 480
SIZE = (WIDTH, HEIGTH)

# fractale parameters
INFINI = 16.0
MAX_ITER = 100
coord_set = {
	'x1': -2.5,
	'x2': 1.0,
	'y1': -2.0,
	'y2': 2.0
}
coord_set['width'] = coord_set['x2'] - coord_set['x1']
coord_set['heigth'] = coord_set['y2'] - coord_set['y1']

def getIter(x, y):
	Cr = coord_set['width'] * x / WIDTH + coord_set['x1']
	Ci = coord_set['heigth'] * y / HEIGTH + coord_set['y1']

	aa, bb, a, b = 0.0, 0.0, Cr, Ci
	for i in range(MAX_ITER):
		aa = a * a - b * b
		bb = 2.0 * a * b
		a = aa + Cr
		b = bb + Ci
		if abs(a + b) > INFINI:
			break
	return (i)

def eventHandler(type_event):
	if type_event is pygame.QUIT:
		print('here')
		return True

def main():
	display = Display(WIDTH, HEIGTH)

	display.initSurface()

	ar = display.getPixelArray()

	for c in range(HEIGTH):
		for r in range(WIDTH):
			iteration = getIter(r, c)
			brigth = (iteration / MAX_ITER) * 255
			ar[r, c] = brigth, brigth, brigth
		print('\r', c * 100 / HEIGTH, end='')
	print('\r', c * 100 / HEIGTH, '\tdone')

	del ar

	display.blitSurface()

	display.listenEvent(eventHandler)

if __name__ == '__main__':
	main()
