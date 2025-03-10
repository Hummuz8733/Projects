import pygame as p
import chessengine
from chessengine import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = [ "wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ" ]
    for piece in pieces:
        IMAGES[ piece ] = p.transform.scale( p.image.load( "GitHub/Projects/chessbotpython/images/" + piece + ".png" ), ( SQ_SIZE, SQ_SIZE ) )


def drawBoard( screen,  ):
    colors = [ p.Color( "antiquewhite1" ), p.Color( "burlywood3" ) ]
    colorsHighlighted = [ p.Color( "coral1" ), p.Color( "brown1" ) ]
    for i in range( DIMENSION ):
        for j in range( DIMENSION ):
            color = colors[ ( ( i + j ) % 2 ) ]
            p.draw.rect( screen, color, p.Rect( j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE ) ) 

def drawPieces( screen, board ):
    for i in range( DIMENSION ):
        for j in range( DIMENSION ):
            piece = board[ i ][ j ]
            if piece != "--":
                screen.blit( IMAGES[ piece ], p.Rect( j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE ) )

def drawGameState( screen, gs ):
    drawBoard( screen )
    drawPieces( screen, gs.board )

def main():
    p.init()
    screen = p.display.set_mode( ( WIDTH, HEIGHT ) )
    clock = p.time.Clock() 
    screen.fill( p.Color( "white" ) )
    gs = chessengine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                column = location[ 0 ] // SQ_SIZE
                row = location[ 1 ] // SQ_SIZE
                if sqSelected == ( row, column ):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = ( row, column )
                    playerClicks.append( sqSelected )
                if len( playerClicks ) == 2:
                    if ( playerClicks[ 0 ] == ( 7, 4 ) and ( playerClicks [ 1 ] == ( 7, 0 ) or playerClicks[ 1 ] == ( 7, 7 ) ) ) or ( playerClicks[ 0 ] == ( 0, 4 ) and ( playerClicks [ 1 ] == ( 0, 0 ) or playerClicks[ 1 ] == ( 0, 7 ) ) ):
                        move = chessengine.Move( playerClicks[ 0 ], playerClicks[ 1 ], gs.board, False, True )
                    else:
                        move = chessengine.Move( playerClicks[ 0 ], playerClicks[ 1 ], gs.board )
                    print( move.getChessNotation() )
                    for i in range( len( validMoves ) ):
                        if move == validMoves[ i ]:
                            gs.makeMove( validMoves[ i ] )
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [ sqSelected ]
                        print("illegal")
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState( screen, gs )
        clock.tick( MAX_FPS )
        p.display.flip()



if __name__ == "__main__":
    main()

