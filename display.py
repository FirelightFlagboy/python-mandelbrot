import pygame
from time import sleep

class Display():
	def __init__(self, WIDTH, HEIGTH):
		"""
		construtor:
			init pygame
			create windows
			save dimension of windows
		"""
		pygame.init()
		self.windows = pygame.display.set_mode((WIDTH, HEIGTH))
		pygame.display.flip()
		self.width = WIDTH
		self.heigth = HEIGTH

	def getSurface(self):
		""" return a surface of the dimension of the windows """
		return pygame.Surface((self.width, self.heigth))

	def initSurface(self):
		""" create a default surface for the class """
		self.surface = self.getSurface()

	def getPixelArray(self):
		""" return Pixel Array of the surface save by the class """
		return pygame.PixelArray(self.surface)

	def setSurface(self, surface):
		""" function that set surface given in params """
		self.surface = surface

	def blitSurface(self, x=0, y=0):
		""" add saved surface to the windows at the coord x and y """
		self.windows.fill(0xffffff)
		self.windows.blit(self.surface, (x, y))
		pygame.display.flip()

	def listenEvent(self, eventHandler):
		""" listen the event and use given handler """
		while True:
			for event in pygame.event.get():
				if eventHandler(event.type, event) == True:
					return True
			sleep(0.05)
