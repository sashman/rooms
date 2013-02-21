import pygame
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




# MAIN

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('rooms')


def main():
		
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
	player = Player((
					floor_tile.x,
					floor_tile.y
					))



	clock = pygame.time.Clock()
	fps_update_counter = 0


	running = True
	while running:
		tickFPS = clock.tick()
		pygame.display.set_caption("Press Esc to quit. FPS: %.2f" % (clock.get_fps()))

		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
				elif event.key == pygame.K_UP:
					player.K_UP = True
				elif event.key == pygame.K_DOWN:
					player.K_DOWN = True
				elif event.key == pygame.K_LEFT:
					player.K_LEFT = True
				elif event.key == pygame.K_RIGHT:
					player.K_RIGHT = True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					player.K_UP = False
				elif event.key == pygame.K_DOWN:
					player.K_DOWN = False
				elif event.key == pygame.K_LEFT:
					player.K_LEFT = False
				elif event.key == pygame.K_RIGHT:
					player.K_RIGHT = False
			
		player.movement_events(tickFPS)
		player.wall_collision(rooms)

		screen.fill(background_colour)

		for room in rooms:
			room.display(screen)

		player.display(screen)

		pygame.display.flip()


	pygame.quit()



if __name__ == '__main__': main()