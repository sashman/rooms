import pygame
import random
import math

background_colour = (200,200,200)
(width, height) = (400, 400)
TILE_SIZE = 10

WEST = 'W'
NORTH = 'N'
EAST = 'E'
SOUTH = 'S'


class Square(object):
	def __init__(self, (x,y)):
		
		self.x = x
		self.y = y

	def get_center(self):
		return self.x + TILE_SIZE/2, self.y + TILE_SIZE/2


class Entity(Square):
	def __init__(self, (x,y), colour):
		super(Entity, self).__init__((x,y))
		self.colour = colour
	
	def display(self, screen):
		pygame.draw.rect(screen, self.colour, (self.x, self.y, TILE_SIZE,TILE_SIZE))


class LivingEntity(Entity):
	
	def __init__(self, (x,y), colour):
		super(LivingEntity, self).__init__((x,y), colour)
		self.alive = True
		
	def moveX(self,x, t):
		if self.alive:
			self.x += x * t
		
	def moveY(self,y, t):
		if self.alive:
			self.y += y * t

	def wall_collision(self, rooms):
		for room in rooms:
			#in the room
			if self.x + TILE_SIZE > room.x and self.x < room.x + room.w + TILE_SIZE and self.y + TILE_SIZE > room.y and self.y < room.y + room.h  + TILE_SIZE:
				#if in the room
				for wall_tile in room.tiles:
					#check all wall tiles
					if wall_tile.type == 'wall':
						if self.x + TILE_SIZE > wall_tile.x and self.x < wall_tile.x + TILE_SIZE and self.y + TILE_SIZE > wall_tile.y and self.y < wall_tile.y + TILE_SIZE:

							#tile collision
							#wall_tile.type = 'floor'
							xc,yc = self.get_center()
							
							if yc < wall_tile.y:
								self.y = wall_tile.y - TILE_SIZE
							elif yc > wall_tile.y + TILE_SIZE:
								self.y = wall_tile.y + TILE_SIZE

							if xc < wall_tile.x:
								self.x = wall_tile.x - TILE_SIZE
							elif xc > wall_tile.x + TILE_SIZE:
								self.x = wall_tile.x + TILE_SIZE


class Player(LivingEntity):
	def __init__(self, (x,y)):
		super(Player, self).__init__((x,y), (100,200,150))
		self.K_DOWN = False
		self.K_UP = False
		self.K_LEFT = False
		self.K_RIGHT = False
		self.speed = 0.1

	def movement_events(self, t):
		if(self.K_UP):
			self.moveY(-self.speed,t)
		elif(self.K_DOWN):
			self.moveY(self.speed, t)

		if(self.K_LEFT):
			self.moveX(-self.speed, t)
		elif(self.K_RIGHT):
			self.moveX(self.speed, t)


class Tile(Square):
	
	def __init__(self, (x,y), type = "", facing = ""):
		self.x = x
		self.y = y
		self.type = type
		self.facing = facing
		

class Room():

	def __init__(self, (x,y), (w,h), tile=None):
		self.x = x
		self.y = y
		self.h = h
		self.w = w
		self.colour = (0,0,0)
		self.floor_colour = (50,50,50)
		self.tiles = []

		adjacent = (None, None)
		if(tile):
			if(tile.facing == NORTH):
				self.y = tile.y-self.h-TILE_SIZE
				min_x = tile.x-self.w+TILE_SIZE
				max_x = tile.x - TILE_SIZE
				x_range = (max_x-min_x)/TILE_SIZE
				self.x = min_x+random.randint(0,x_range)*TILE_SIZE
				adjacent = (tile.x, tile.y-TILE_SIZE)
			elif(tile.facing == SOUTH):
				self.y = tile.y+TILE_SIZE
				min_x = tile.x-self.w+TILE_SIZE
				max_x = tile.x - TILE_SIZE
				x_range = (max_x-min_x)/TILE_SIZE
				self.x = min_x+random.randint(0,x_range)*TILE_SIZE
				adjacent = (tile.x, tile.y+TILE_SIZE)
			elif(tile.facing == EAST):
				self.x = tile.x+TILE_SIZE
				min_y = tile.y-self.h+TILE_SIZE
				max_y = tile.y - TILE_SIZE
				y_range = (max_y-min_y)/TILE_SIZE
				self.y = min_y+random.randint(0,y_range)*TILE_SIZE
				adjacent = (tile.x+TILE_SIZE, tile.y)
			elif(tile.facing == WEST):
				self.x = tile.x-self.w-TILE_SIZE
				min_y = tile.y-self.h+TILE_SIZE
				max_y = tile.y - TILE_SIZE
				y_range = (max_y-min_y)/TILE_SIZE
				self.y = min_y+random.randint(0,y_range)*TILE_SIZE
				adjacent = (tile.x-TILE_SIZE, tile.y)


			

		for x in xrange(self.x,self.x+self.w+1, TILE_SIZE):
			for y in xrange(self.y,self.y+self.h+1, TILE_SIZE):
				if(x == self.x or y == self.y or x == self.x+self.w or y == self.y+self.h):
					exists = False
					for tile in self.tiles: 
						if(tile.x == x and tile.y == y): exists = True
					if not exists:
						if(x==self.x): facing = WEST
						if(y==self.y): facing = NORTH
						if(x==self.x+self.w): facing = EAST
						if(y==self.y+self.h): facing = SOUTH
						adj_x, adj_y = adjacent
						tile_type = 'wall'
						if x == adj_x and y == adj_y: tile_type = 'door'
						self.tiles.append(Tile((x,y), type=tile_type, facing=facing))
				else:
					self.tiles.append(Tile((x,y), type='floor'))
				
	def get_wall_tile(self):
		return random.choice([tile for tile in self.tiles if tile.type == 'wall' and ((not (tile.x == self.x and tile.y == self.y))
											and (not (tile.x == (self.x + self.w) and tile.y == self.y))
											and (not (tile.x == self.x and tile.y == (self.y + self.h)))
											and (not (tile.x == (self.x + self.w) and tile.y == (self.y + self.h)))) ])

		

	def display(self, screen):

		for tile in self.tiles:
			if(tile.type == 'wall'):
				pygame.draw.rect(screen, self.colour, (tile.x, tile.y, TILE_SIZE,TILE_SIZE))
			elif(tile.type == 'floor' or tile.type == 'door'):
				pygame.draw.rect(screen, self.floor_colour, (tile.x, tile.y, TILE_SIZE,TILE_SIZE))

	def collides_with_room(self, room):
		return (room.x + room.w > self.x and room.x < self.x+self.w) and (room.y +room.h > self.y and room.y < self.y+self.h)

	def collides_with_boundaries(self):
		return (self.x < 0 or self.y < 0 or self.x + self.w + TILE_SIZE > width or self.y + self.h + TILE_SIZE > height)

	def collides(self, rooms):
		return any([self.collides_with_boundaries(), any([self.collides_with_room(room) for room in rooms])])

	def __str__(self):
		return "x: " + str(self.x) + "\ny: " + str(self.y) + "\nw: " + str(self.w) + "\nh: " + str(self.h)