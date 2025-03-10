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


def drawBoard( screen, lastMove, sqSelected ):
    colors = [ p.Color( "antiquewhite1" ), p.Color( "burlywood3" ) ]
    colorsHighlighted = [ p.Color( "coral1" ), p.Color( "brown1" ) ]
    colorsSelected = [ p.Color( "darkolivegreen3" ), p.Color( "darkolivegreen3" ) ]
    for i in range( DIMENSION ):
        for j in range( DIMENSION ):
            if lastMove != () and ( ( i, j ) == lastMove[ 0 ] or ( i, j ) == lastMove[ 1 ] ):
                color = colorsHighlighted[ ( ( i + j ) % 2 ) ]
            elif sqSelected != () and ( i, j ) == sqSelected:
                color = colorsSelected[ ( ( i + j ) % 2 ) ]
            else:
                color = colors[ ( ( i + j ) % 2 ) ]
            p.draw.rect( screen, color, p.Rect( j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE ) ) 

def drawPieces( screen, board ):
    for i in range( DIMENSION ):
        for j in range( DIMENSION ):
            piece = board[ i ][ j ]
            if piece != "--":
                screen.blit( IMAGES[ piece ], p.Rect( j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE ) )

def drawGameState( screen, gs, lastMove, sqSelected ):
    drawBoard( screen, lastMove, sqSelected )
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
    lastMove = ()

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
                    drawGameState( screen, gs, lastMove, sqSelected )
                else:
                    sqSelected = ( row, column )
                    playerClicks.append( sqSelected )
                    drawGameState( screen, gs, lastMove, sqSelected )
                if len( playerClicks ) == 2:
                    if ( playerClicks[ 0 ] == ( 7, 4 ) and ( playerClicks [ 1 ] == ( 7, 0 ) or playerClicks[ 1 ] == ( 7, 7 ) ) ) or ( playerClicks[ 0 ] == ( 0, 4 ) and ( playerClicks [ 1 ] == ( 0, 0 ) or playerClicks[ 1 ] == ( 0, 7 ) ) ):
                        move = chessengine.Move( playerClicks[ 0 ], playerClicks[ 1 ], gs.board, False, True )
                    else:
                        move = chessengine.Move( playerClicks[ 0 ], playerClicks[ 1 ], gs.board )
                    print( move.getChessNotation() )
                    for i in range( len( validMoves ) ):
                        if move == validMoves[ i ]:
                            gs.makeMove( validMoves[ i ] )
                            lastMove = ( playerClicks[ 0 ], playerClicks[ 1 ] )
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
                    move = ( ( gs.moveLog[ -1 ].startRow, gs.moveLog[ -1 ].startColumn ), ( gs.moveLog[ -1 ].endRow, gs.moveLog[ -1 ].endColumn ) )

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState( screen, gs, lastMove, sqSelected )
        clock.tick( MAX_FPS )
        p.display.flip()



if __name__ == "__main__":
    main()

