import pygame
import random
import math

from rooms_util import Player, Tile, Room, KeyboardController, CPUSpinnerController, PygameView, EventManager, Map

background_colour = (200,200,200)
(width, height) = (400, 400)
TILE_SIZE = 10

WEST = 'W'
NORTH = 'N'
EAST = 'E'
SOUTH = 'S'


def main():

	clock = pygame.time.Clock()
	evManager = EventManager()

	

	global player
	player = Player('player',(
			0,
			0
			),evManager )

	game_map = Map(evManager, [player])
	

	keybd = KeyboardController(evManager,player)
	spinner = CPUSpinnerController(evManager,clock, game_map)
	pygameView = PygameView(evManager,clock)

	
	
	evManager.RegisterListener( keybd )
	evManager.RegisterListener( spinner )
	evManager.RegisterListener( pygameView )

	spinner.Run()



if __name__ == '__main__': main()