import random
import math

from rooms_util import Player, Tile, Room

background_colour = (200,200,200)
(width, height) = (400, 400)
TILE_SIZE = 10

WEST = 'W'
NORTH = 'N'
EAST = 'E'
SOUTH = 'S'

def get_random_room_dimentions():
	sizeh = random.randint(3, 6) * TILE_SIZE
	sizew = random.randint(3, 6) * TILE_SIZE
	x = random.randint(sizew, width-(sizew))
	y = random.randint(sizeh, height-(sizeh))
	return x,y,sizew,sizeh


number_of_rooms = 50
rooms = []

# for n in range(number_of_rooms):
	
x,y,sizew,sizeh = get_random_room_dimentions()

x = int(width/2)
y = int(height/2)

room = Room((x,y), (sizew,sizeh))	
rooms.append(room)	



cs = []

for n in range(number_of_rooms):

	
	c = random.choice(rooms).get_wall_tile()

	x,y,sizew,sizeh = get_random_room_dimentions()

	new_room = Room((0,0), (sizew,sizeh), tile = c)	
	
	if(not new_room.collides(rooms)):
		rooms.append(new_room)
		c.type = 'door'
		cs.append(c)


floor_tile = random.choice([tile for tile in room.tiles if tile.type == 'floor'])