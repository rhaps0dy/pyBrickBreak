import pygame
import math

class Ship():
	color=None
	length=0
	height=0
	x=0
	y=0
	bbox = None
	def __init__(self, x, y, length=70, height=24):
		self.x = int(x)
		self.y = int(y)
		self.length = int(length)
		self.height = int(height)

		#height determines the radius of the caps 
		self.bbox = pygame.Rect(0,0,0,0)
		self.bbox.w = self.length+self.height
		self.bbox.h = self.height
		self.bbox.center = (self.x, self.y)

		self.color = pygame.Color(0, 0, 0)
		self.bboxcolor = pygame.Color(0, 255, 0)

	def update(self, x):
		self.x = x
		self.bbox.centerx = self.x

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, (self.x-self.length/2, self.y), self.height/2)
		pygame.draw.circle(surface, self.color, (self.x+self.length/2, self.y), self.height/2)
		pygame.draw.rect(surface, self.color, (self.x-self.length/2, self.y-self.height/2, self.length, self.height))

	def checkBallCollision(self, ball):
		"""
		Returns true if the ball has collided with the ship
		"""
		res, cornx, corny = ball.collWithRect(self.bbox)
		# print res,cornx, corny
		if res==0:
			return False

		left = self.x-self.length/2
		if ball.x >= left and ball.x <= self.x+self.length/2:
			#bounce normally
			magnitude = math.sqrt(ball.vx**2+ball.vy**2)
			for i in range(1, 7):
				if ball.x < left+self.length/7*i:
					angle = math.radians(120.-10.*(i-1))
					ball.vx = magnitude*math.cos(angle)
					ball.vy = -magnitude*math.sin(angle)
					return True
			#maximum right
			angle = math.radians(60.)
			ball.vx = magnitude*math.cos(angle)
			ball.vy = -magnitude*math.sin(angle)
			return True
			return True

		#bounce with the caps
		if ball.collWithCircle(self.x-self.length/2, self.y, self.height/2):
			ball.bouncePoint(self.x-self.length/2, self.y)
			return True
		elif ball.collWithCircle(self.x+self.length/2, self.y, self.height/2):
			ball.bouncePoint(self.x+self.length/2, self.y)
			return True
		return False
