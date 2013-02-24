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



class Event:
	"""this is a superclass for any events that might be generated by an
	object and sent to the EventManager
	"""
	def __init__(self):
		self.name = "Generic Event"

class TickEvent(Event):
	def __init__(self, game_map):
		self.name = "CPU Tick Event"
		self.game_map = game_map

class QuitEvent(Event):
	def __init__(self):
		self.name = "Program Quit Event"

class MapBuiltEvent(Event):
	def __init__(self, map_):
		self.name = "Map Finished Building Event"
		self.map = map_

class EntityMoveEvent(Event):
	def __init__(self, entity):
		self.name = "Entity Move Event"
		self.entity = entity
		

class EventManager:
	"""this object is responsible for coordinating most communication
	between the Model, View, and Controller.
	"""
	def __init__(self ):
		from weakref import WeakKeyDictionary
		self.listeners = WeakKeyDictionary()

	#----------------------------------------------------------------------
	def RegisterListener( self, listener ):
		self.listeners[ listener ] = 1

	#----------------------------------------------------------------------
	def UnregisterListener( self, listener ):
		if listener in self.listeners.keys():
			del self.listeners[ listener ]
		
	#----------------------------------------------------------------------
	def Post( self, event ):
		"""Post a new event.  It will be broadcast to all listeners"""
		for listener in self.listeners.keys():
			#NOTE: If the weakref has died, it will be 
			#automatically removed, so we don't have 
			#to worry about it.
			listener.Notify( event )


class KeyboardController:

	"""KeyboardController takes Pygame events generated by the
	keyboard and uses them to control the model, by sending Requests
	or to control the Pygame display directly, as with the QuitEvent
	"""
	def __init__(self, evManager, player):
		self.evManager = evManager
		self.evManager.RegisterListener( self )
		self.player = player
	
	def Notify(self, event):
		if isinstance( event, TickEvent ):
			#Handle Input Events
			for event in pygame.event.get():
					if event.type == pygame.QUIT:
						event = QuitEvent()
						self.evManager.Post( event )
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							event = QuitEvent()
							self.evManager.Post( event )
						elif event.key == pygame.K_UP:
							self.player.K_UP = True
						elif event.key == pygame.K_DOWN:
							self.player.K_DOWN = True
						elif event.key == pygame.K_LEFT:
							self.player.K_LEFT = True
						elif event.key == pygame.K_RIGHT:
							self.player.K_RIGHT = True
					elif event.type == pygame.KEYUP:
						if event.key == pygame.K_UP:
							self.player.K_UP = False
						elif event.key == pygame.K_DOWN:
							self.player.K_DOWN = False
						elif event.key == pygame.K_LEFT:
							self.player.K_LEFT = False
						elif event.key == pygame.K_RIGHT:
							self.player.K_RIGHT = False
			


class CPUSpinnerController:

	def __init__(self, evManager, clock, game_map=[]):
		self.clock = clock

		self.evManager = evManager
		self.evManager.RegisterListener( self )

		self.keepGoing = 1

		self.game_map = game_map
		
	
	def Run(self):

		while self.keepGoing:			

			tickFPS = self.clock.tick()

			if not self.game_map.state == Map.STATE_BUILT:
				self.game_map.Build()

			for entity in self.game_map.present_entities:
				
				entity.movement_events(tickFPS)
				entity.wall_collision(self.game_map.rooms)

			event = TickEvent(self.game_map)
			self.evManager.Post( event )

	def Notify(self, event):
		if isinstance( event, QuitEvent ):
			self.keepGoing = False
			


class PygameView:

	def __init__(self, evManager,clock):
		self.clock = clock
		self.evManager = evManager
		self.evManager.RegisterListener( self )

		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('rooms')
	
	def Notify(self, event):
		if isinstance( event, TickEvent ):
			
			pygame.display.set_caption("rooms. FPS: %.2f" % (self.clock.get_fps()))
			#Draw Everything
			self.screen.fill(background_colour)

			gameMap = event.game_map
			self.ShowMap( gameMap )

		#elif isinstance( event, EntityMoveEvent ):
			for entity in gameMap.present_entities:
				self.ShowEntity(entity)

		#elif isinstance( event, MapBuiltEvent ):


		pygame.display.flip()

	def ShowMap(self, gameMap):

		for room in gameMap.rooms:
				room.display(self.screen)

		

	def ShowEntity(self, entity):
		entity.display(self.screen)

		


class Square(object):
	def __init__(self, (x,y)):
		
		self.x = x
		self.y = y

	def get_center(self):
		return self.x + TILE_SIZE/2, self.y + TILE_SIZE/2


class Entity(Square):
	def __init__(self, (x,y), colour, evManager):
		super(Entity, self).__init__((x,y))
		self.colour = colour
		self.evManager = evManager

	
	def display(self, screen):
		pygame.draw.rect(screen, self.colour, (self.x, self.y, TILE_SIZE,TILE_SIZE))


class LivingEntity(Entity):
	
	def __init__(self, (x,y), colour, evManager):
		super(LivingEntity, self).__init__((x,y), colour, evManager)
		self.alive = True
		
	def moveX(self,x, t):
		if self.alive:
			self.x += x * t
			ev = MapBuiltEvent( self )
			self.evManager.Post( ev )

		
	def moveY(self,y, t):
		if self.alive:
			self.y += y * t
			ev = MapBuiltEvent( self )
			self.evManager.Post( ev )

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


							ev = MapBuiltEvent( self )
							self.evManager.Post( ev )






class Player(LivingEntity):
	def __init__(self, (x,y), evManager):
		super(Player, self).__init__((x,y), (100,200,150), evManager)
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

class Map:
	

	STATE_PREPARING = 0
	STATE_BUILT = 1
	MAX_ROOMS = 50


	#----------------------------------------------------------------------
	def __init__(self, evManager, present_entities = []):
		self.evManager = evManager
		#self.evManager.RegisterListener( self )

		self.state = Map.STATE_PREPARING

		self.sectors = []
		self.startSectorIndex = 0
		self.present_entities = present_entities
		self.rooms = []


	def get_random_room_dimentions(self):
		sizeh = random.randint(3, 6) * TILE_SIZE
		sizew = random.randint(3, 6) * TILE_SIZE
		x = random.randint(sizew, width-(sizew))
		y = random.randint(sizeh, height-(sizeh))
		return x,y,sizew,sizeh

	#----------------------------------------------------------------------
	def Build(self):

		self.number_of_rooms = Map.MAX_ROOMS
	
		
		# for n in range(number_of_rooms):
			
		x,y,sizew,sizeh = self.get_random_room_dimentions()

		x = int(width/2)
		y = int(height/2)

		room = Room((x,y), (sizew,sizeh))	
		self.rooms.append(room)	



		cs = []

		for n in range(self.number_of_rooms):

			
			c = random.choice(self.rooms).get_wall_tile()

			x,y,sizew,sizeh = self.get_random_room_dimentions()

			new_room = Room((0,0), (sizew,sizeh), tile = c)	
			
			if(not new_room.collides(self.rooms)):
				self.rooms.append(new_room)
				c.type = 'door'
				cs.append(c)


		self.floor_tile = random.choice([tile for tile in room.tiles if tile.type == 'floor'])

		self.state = Map.STATE_BUILT

		ev = MapBuiltEvent( self )
		self.evManager.Post( ev )