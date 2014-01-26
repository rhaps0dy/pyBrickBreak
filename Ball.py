import pygame

class Ball:
	x=0
	y=0
	vx=0
	vy=0
	r=0
	color=None

	def __init__(self, p, s=None, r=None, color=None):
		self.x = float(p[0])
		self.y = float(p[1])
		if s is None:
			self.vx = 400.
			self.vy = -400.
		else:
			self.vx = float(s[0])
			self.vy = float(s[1])
		if r is None:
			self.r = 10
		else:
			self.r = int(r)
		if color is None:
			self.color = pygame.Color(255, 0, 0)

	def update(self, dt, boundary):
		self.x += self.vx*dt
		self.y += self.vy*dt

		if self.vx < 0 and self.x-self.r < 0:
			self.x = self.r
			self.vx = abs(self.vx)
		elif self.vx > 0 and self.x+self.r > boundary.get_width():
			self.x = boundary.get_width()-self.r
			self.vx = -abs(self.vx)

		if self.vy < 0 and self.y-self.r < 0:
			self.y = self.r
			self.vy = abs(self.vy)


	def draw(self, surface):
		pygame.draw.circle(surface, self.color, (int(round(self.x)), int(round(self.y))), self.r)

	def collWithRect(self, rect):
		"""
		Are we colliding with the rect. Returns tuple with (colliding, cornx, corny)
		Where colliding is 0 when no collision, 1 when edge collision, 2 corner collision
		and cornx corny the coordinates of the corner the ball has collided with
		"""
		def testNoCollide(left1, top1, right1, bottom1, r):
			return (left1 > r.right or right1 < r.left) or (top1 > r.bottom or bottom1 < r.top)

		if testNoCollide(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, rect):
			return 0, None, None
		#did the bounding box hit a corner of the rect? Also set x and y of corner
		totalhit=0
		cornx=corny=0

		if not testNoCollide(self.x-self.r, self.y-self.r, self.x, self.y, rect):
			totalhit+=1
			#lower right corner
			cornx = rect.right
			corny = rect.bottom
		if not testNoCollide(self.x, self.y-self.r, self.x+self.r, self.y, rect):
			totalhit+=1
			#lower left corner
			cornx = rect.left
			corny = rect.bottom
		if not testNoCollide(self.x-self.r, self.y, self.x, self.y+self.r, rect):
			totalhit+=1
			#upper right corner
			cornx = rect.right
			corny = rect.top
		if not testNoCollide(self.x, self.y, self.x+self.r, self.y+self.r, rect):
			totalhit+=1
			#upper left corner
			cornx = rect.left
			corny = rect.top

		if totalhit > 1:
			return 1, None, None

		#check if circle didn't hit rect after all
		if (self.x-cornx)**2 + (self.y-corny)**2 > self.r**2:
			return 0, None, None
		return 2, cornx, corny

	def collWithCircle(self, x, y, r):
		return (self.x-x)**2 + (self.y-y)**2 <= (self.r+r)**2

	def bouncePoint(self, x, y):
		"""
		Bounce from a point with coordinates x y
		"""
		#get direction vector and perpendicular vector
		dirx = x-self.x
		diry = y-self.y
		perpx = -diry
		perpy = dirx
		#express speed of ball in coordinates (a, b) of these vectors
		cachedp = dirx/perpx
		cachevp = self.vx/perpx
		a  =  (-self.vy+perpy*cachevp)/(perpy*cachedp-diry)
		b = cachevp - a*cachedp
		#reverse direction and reconvert
		self.vx = -abs(a*dirx) + b*perpx
		self.vy = -abs(a*diry) + b*perpy
