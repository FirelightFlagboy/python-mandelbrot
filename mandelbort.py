import pygame
from display import Display
from time import process_time
import numpy
from numba import jit

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

# @jit
# def mandelbrot_cal(z):
# 	# is an array
# 	c = z
# 	for n in range(max_iter):
# 		sqrZ = z * z
# 		if sqrZ > 4:
# 			return n
# 		z = sqrZ + c
# 	return 0

# @jit
# def mandelbrot(xMin, xMax, yMin, yMax):
# 	x_line = numpy.linspace(xMin, xMax, WIDTH, dtype=numpy.float64)
# 	y_line = numpy.linspace(yMin, yMax, HEIGTH, dtype=numpy.float64)
# 	pxa = numpy.empty((WIDTH, HEIGTH))
# 	for i in range(WIDTH):
# 		for j in range(HEIGTH):
# 			pxa[i, j] = mandelbrot_cal(x_line[i] + 1j * y_line[j])
# 	return x_line, y_line, pxa

def mandelbrot_cal(c):
	output = numpy.zeros(c.shape)
	z = numpy.zeros(c.shape, numpy.complex64)
	for n in range(max_iter):
		small = numpy.less(z.real * z.real + z.imag * z.imag, 4.0)
		output[small] = n
		z[small] = z[small] * z[small] + c[small]
	output[output == max_iter - 1] = 0
	return output

def mandelbrot(xMin, xMax, yMin, yMax):
	x_line = numpy.linspace(xMin, xMax, WIDTH, dtype=numpy.float64)
	y_line = numpy.linspace(yMin, yMax, HEIGTH, dtype=numpy.float64)
	c = x_line + 1j * y_line[:, None]
	pxa = mandelbrot_cal(c)
	return x_line, y_line, pxa.T

def draw():

	start = process_time()
	_, _, arMap = mandelbrot(coord_set['x1'] / zoom, coord_set['x2'] / zoom, coord_set['y1'] / zoom, coord_set['y2'] / zoom)
	end = process_time()
	print('done in ', end - start)
	display.setSurface(pygame.surfarray.make_surface(arMap))

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
		zoom *= 1.25
	elif button == 3:
		zoom /= 1.25

	print('zoom', zoom)

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

	draw()

	display.listenEvent(eventHandler)

if __name__ == '__main__':
	main()
