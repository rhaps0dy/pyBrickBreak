import pygame
from random import randint

class Block(pygame.Rect):
	color=None
	def __init__(self, x, y, w=35, h=16, color=None):
		pygame.Rect.__init__(self, x, y, w, h)
		if color is None:
			self.color = pygame.Color(randint(0,255), randint(0,255), randint(0,255))
		else:
			self.color = color
	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self)

class BlockArray:
	list = []
	def __init__(self, w, h):
		for i in range(w):
			for j in range(h):
				self.list.append(Block(i*50, j*30, 50, 30))

	def draw(self, surface):
		for b in self.list:
			b.draw(surface)

	def update(self, ball):
		collided = []
		for b in self.list:
			res, cx, cy = ball.collWithRect(b)
			if res!=0:
				collided.append((b, res, cx, cy))
		if len(collided)==0:
			return

		if collided[0][1]==1 or len(collided)>1:
			#normal bounce
			if ball.x < b.left or ball.x > b.right:
				ball.vx = -ball.vx
			if ball.y < b.top or ball.y > b.bottom:
				ball.vy = -ball.vy
		if collided[0][1]==2:
			#corner bounce
			ball.bouncePoint(collided[0][2], collided[0][3])

		for entry in collided:
			self.list.remove(entry[0])



