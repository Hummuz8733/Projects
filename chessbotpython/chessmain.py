import pygame as p
import chessengine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = [ "wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ" ]
    for piece in pieces:
        IMAGES[ piece ] = p.transform.scale( p.image.load( "images/" + piece + ".png" ), ( SQ_SIZE, SQ_SIZE ) )

def main():
    p.init()
    screen = p.display.set_mode( WIDTH, HEIGHT )
    clock = p.time.Clock() 
    screen.fill( p.Color( "white" ) )
    gs = chessengine.GameState()
    print(gs.board)
    

