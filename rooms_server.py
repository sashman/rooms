import random
import math

from rooms_util import Player, Tile, Room, NetworkClientController, CPUSpinnerController, TextLogView, EventManager, Map
from twisted.spread import pb

background_colour = (200,200,200)
(width, height) = (400, 400)
TILE_SIZE = 10

WEST = 'W'
NORTH = 'N'
EAST = 'E'
SOUTH = 'S'

def main():
    evManager = EventManager()

    log = TextLogView( evManager )
    clientController = NetworkClientController( evManager )

    player = Player('player',(
			0,
			0
			),evManager )
    game_map = Map(evManager, [player])
    
    from twisted.internet import reactor

    reactor.listenTCP( 8000, pb.PBServerFactory(clientController) )

    reactor.run()

if __name__ == '__main__': main()