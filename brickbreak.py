#!/usr/bin/python2
import os, platform
import pygame, sys
from pygame.locals import *
from Block import Block, BlockArray
from Ball import Ball
from Ship import Ship

class BrickBreakGame:
	def __init__(self, w=800, h=600):
		if platform.system() == 'Windows':
		    os.environ['SDL_VIDEODRIVER'] = 'windib'
		os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
		pygame.init()
		self.clock = pygame.time.Clock()
		self.window = pygame.display.set_mode((w, h), pygame.DOUBLEBUF|pygame.HWSURFACE)
		pygame.display.set_caption('Brick Break!')

		self.ship = Ship(w/2, h-14)
		self.ball = Ball((self.ship.x, self.ship.y-self.ship.height/2), (400., 0.))
		self.backgroundColor = pygame.Color(255,255,255)

		pygame.mouse.set_visible(False)
		pygame.mouse.set_pos(100+w/2, 100+h/2)

		self.blocks = BlockArray(16,11) 
		self.shipx = pygame.mouse.get_pos()[0]
		self.goLeft = self.goRight = False


	def run(self):
		while True:
			self.mainLoop()

	def mainLoop(self):
		#EVENTS
		for event in pygame.event.get():
			if event.type == MOUSEMOTION:
				self.shipx = event.pos[0]
			elif event.type == KEYDOWN:
				if event.key == K_LEFT:
					self.goLeft = True
				elif event.key == K_RIGHT:
					self.goRight = True
				elif event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))
			elif event.type == KEYUP:
				if event.key == K_LEFT:
					self.goLeft = False
				elif event.key == K_RIGHT:
					self.goRight = False
			elif event.type == QUIT:
				pygame.quit()
				sys.exit(0)

		if self.goLeft:
			self.shipx -= self.clock.get_time()*2/3
		elif self.goRight:
			self.shipx += self.clock.get_time()*2/3

		#LOGIC
		self.ball.update(self.clock.get_time()/1000., self.window)
		self.ship.update(self.shipx)
		self.blocks.update(self.ball)
		self.ship.checkBallCollision(self.ball)

		if self.ball.y > self.window.get_height():
			pygame.event.post(pygame.event.Event(QUIT))

		#DRAW
		self.window.fill(self.backgroundColor)
		self.blocks.draw(self.window)
		self.ship.draw(self.window)
		self.ball.draw(self.window)

		pygame.display.update()
		self.clock.tick(60)


if __name__ == '__main__':
	b = BrickBreakGame()
	b.run()
