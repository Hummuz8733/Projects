import time
import pygame as p

class GameState():
    def __init__( self ):
        self.board = [
            [ "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR" ],
            [ "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp" ],
            [ "--", "--", "--", "--", "--", "--", "--", "--" ],
            [ "--", "--", "--", "--", "--", "--", "--", "--" ],
            [ "--", "--", "--", "--", "--", "--", "--", "--" ],
            [ "--", "--", "--", "--", "--", "--", "--", "--" ],
            [ "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp" ],
            [ "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR" ],
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = ( 7, 4 )
        self.blackKingLocation = ( 0, 4 )
        self.whiteKingMoved = 0
        self.blackKingMoved = 0
        self.leftWhiteRookMoved = 0
        self.rightWhiteRookMoved = 0
        self.leftBlackRookMoved = 0
        self.rightBlackRookMoved = 0
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.moveFunctions = {
            'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves
        }



    def makeMove( self, move ):
        if move.castle == True:
            if move.endRow == 7:
                if move.endColumn == 0:
                    self.board[ 7 ][ 0 ] = "--"
                    self.board[ 7 ][ 2 ] = "wK"
                    self.board[ 7 ][ 3 ] = "wR"
                    self.board[ 7 ][ 4 ] = "--"
                    self.whiteKingMoved += 1
                    self.leftWhiteRookMoved += 1
                if move.endColumn == 7:
                    self.board[ 7 ][ 4 ] = "--"
                    self.board[ 7 ][ 5 ] = "wR"
                    self.board[ 7 ][ 6 ] = "wK"
                    self.board[ 7 ][ 7 ] = "--"
                    self.whiteKingMoved += 1
                    self.rightWhiteRookMoved += 1
            else:
                if move.endColumn == 0:
                    self.board[ 0 ][ 0 ] = "--"
                    self.board[ 0 ][ 2 ] = "bK"
                    self.board[ 0 ][ 3 ] = "bR"
                    self.board[ 0 ][ 4 ] = "--"
                    self.blackKingMoved += 1
                    self.leftBlackRookMoved += 1
                if move.endColumn == 7:
                    self.board[ 0 ][ 4 ] = "--"
                    self.board[ 0 ][ 5 ] = "bR"
                    self.board[ 0 ][ 6 ] = "bK"
                    self.board[ 0 ][ 7 ] = "--"
                    self.blackKingMoved += 1
                    self.rightBlackRookMoved += 1
            self.whiteToMove = not self.whiteToMove
            self.moveLog.append( move )
            pass
        elif move.promotion == True:
            print( "Choose which piece to promote to:" )
            print( "q: Queen, r: Rook, b: Bishop, n: Knight" )
            flag = False
            while not flag:
                for e in p.event.get():
                    if e.type == p.KEYDOWN:
                        if e.key == p.K_q:
                            piece = 'Q'
                            flag = True
                        if e.key == p.K_r:
                            piece = 'R'
                            flag = True
                        if e.key == p.K_n:
                            piece = 'N'
                            flag = True
                        if e.key == p.K_b:
                            piece = 'B'
                            flag = True
            self.board[ move.startRow ][ move.startColumn ] = "--"
            if self.whiteToMove:
                self.board[ move.endRow ][ move.endColumn ] = "w" + piece
            else:
                self.board[ move.endRow ][ move.endColumn ] = "b" + piece
            self.moveLog.append( move )
            self.whiteToMove = not self.whiteToMove
        else:
            self.board[ move.startRow ][ move.startColumn ] = "--"
            self.board[ move.endRow ][ move.endColumn ] = move.pieceMoved
            self.moveLog.append( move )
            if move.enpassant == True:
                if self.whiteToMove:
                    self.board[ move.endRow + 1 ][ move.endColumn ] = "--"
                else:
                    self.board[ move.endRow - 1 ][ move.endColumn ] = "--"
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingMoved += 1
                self.whiteKingLocation = ( move.endRow, move.endColumn )
            if move.pieceMoved == "bK":
                self.blackKingMoved += 1
                self.blackKingLocation = ( move.endRow, move.endColumn )
            if move.pieceMoved == "wR":
                if move.startRow == 7 and move.startColumn == 0:
                    self.leftWhiteRookMoved += 1
                if move.startRow == 7 and move.startColumn == 7:
                    self.rightWhiteRookMoved += 1
            if move.pieceMoved == "bR": 
                if move.startRow == 0 and move.startColumn == 0:
                    self.leftBlackRookMoved += 1
                if move.startRow == 0 and move.startColumn == 7:
                    self.rightBlackRookMoved += 1

        


    def undoMove( self ):
        if len( self.moveLog ) != 0:
            lastMove = self.moveLog.pop()
            self.board[ lastMove.startRow ][ lastMove.startColumn ] = lastMove.pieceMoved
            self.board[ lastMove.endRow ][ lastMove.endColumn ] = lastMove.pieceCaptured
            if lastMove.enpassant == True:
                if self.whiteToMove == True:
                    self.board[ lastMove.endRow - 1 ][ lastMove.endColumn ] = "wp"
                else:
                    self.board[ lastMove.endRow + 1 ][ lastMove.endColumn ] = "bp"
            if lastMove.castle == True:
                if lastMove.endRow == 7:
                    if lastMove.endColumn == 0:
                        self.board[ 7 ][ 0 ] = "wR"
                        self.board[ 7 ][ 2 ] = "--"
                        self.board[ 7 ][ 3 ] = "--"
                        self.board[ 7 ][ 4 ] = "wK"
                        self.whiteKingMoved -= 1
                        self.leftWhiteRookMoved -= 1
                    if lastMove.endColumn == 7:
                        self.board[ 7 ][ 4 ] = "wK"
                        self.board[ 7 ][ 5 ] = "--"
                        self.board[ 7 ][ 6 ] = "--"
                        self.board[ 7 ][ 7 ] = "wR"
                        self.whiteKingMoved -= 1
                        self.rightWhiteRookMoved -= 1
                else:
                    if lastMove.endColumn == 0:
                        self.board[ 0 ][ 0 ] = "bR"
                        self.board[ 0 ][ 2 ] = "--"
                        self.board[ 0 ][ 3 ] = "--"
                        self.board[ 0 ][ 4 ] = "bK"
                        self.blackKingMoved -= 1
                        self.leftBlackRookMoved -= 1
                    if lastMove.endColumn == 7:
                        self.board[ 0 ][ 4 ] = "bK"
                        self.board[ 0 ][ 5 ] = "--"
                        self.board[ 0 ][ 6 ] = "--"
                        self.board[ 0 ][ 7 ] = "bR"
                        self.blackKingMoved -= 1
                        self.rightBlackRookMoved -= 1
                self.whiteToMove = not self.whiteToMove
            else:
                self.whiteToMove = not self.whiteToMove
                if lastMove.pieceMoved == "wK":
                    self.whiteKingLocation = ( lastMove.startRow, lastMove.startColumn )
                    self.whiteKingMoved -= 1
                if lastMove.pieceMoved == "bK":
                    self.blackKingLocation = ( lastMove.startRow, lastMove.startColumn )
                    self.blackKingMoved -= 1
                if lastMove.pieceMoved == "wR":
                    if self.leftWhiteRookMoved == 1 and lastMove.startColumn == 0:
                        self.leftWhiteRookMoved -= 1
                    if self.rightWhiteRookMoved == 1 and lastMove.startColumn == 7:
                        self.rightWhiteRookMoved -= 1
                else:
                    if self.leftBlackRookMoved == 1 and lastMove.startColumn == 0:
                        self.leftBlackRookMoved -= 1
                    if self.rightBlackRookMoved == 1 and lastMove.startColumn == 7:
                        self.rightBlackRookMoved -= 1


    def getPawnMoves( self, row, column, moves ):
        piecePinned = False
        pinDirection = ()
        for i in range( len( self.pins ) -1, -1, -1 ):
            if self.pins[ i ][ 0 ] == row and self.pins[ i ][ 1 ] == column:
                piecePinned = True
                pinDirection = ( self.pins[ i ][ 2 ], self.pins[ i ][ 3 ])
                self.pins.remove( self.pins[ i ] )
                break
    
        if self.board[ row ][ column ][ 0 ] == 'w':
            if self.board[ row - 1 ][ column ] == "--":
                if not piecePinned or pinDirection == ( -1, 0 ) or pinDirection == ( 1, 0 ):
                    if row - 1 == 0:
                        moves.append( Move( ( row, column ), ( row - 1, column ), self.board, False, False, True ) )
                    else:
                        moves.append( Move( ( row, column ), ( row - 1, column ), self.board ) )
                    if row == 6:    
                        if self.board[ row - 2 ][ column ] == "--":
                            if not piecePinned or pinDirection == ( -1, 0 ) or pinDirection == ( 1, 0 ):
                                moves.append( Move(( row, column ), ( row - 2, column ), self.board ) )
            if column != 0:
                if not piecePinned or pinDirection == ( -1, -1 ) or pinDirection == ( 1, 1 ):
                    if self.board[ row - 1 ][ column - 1 ][ 0 ] == 'b':
                        if row - 1 == 0:
                            moves.append( Move( ( row, column ), ( row - 1, column - 1 ), self.board, False, False, True ) )
                        else:
                            moves.append( Move( ( row, column ), ( row - 1, column - 1 ), self.board ) )
                    if self.board[ row ][ column - 1 ] == "bp" and self.moveLog[ -1 ].pieceMoved == "bp" and row == 3 and self.moveLog[ -1 ].startRow == 1 and self.moveLog[ -1 ].startColumn == ( column - 1 ):
                        moves.append( Move( ( row, column ), ( row - 1, column - 1 ), self.board, True) ) 

            if column != 7:
                if not piecePinned or pinDirection == ( -1, 1 ) or pinDirection == ( 1, -1 ):
                    if self.board[ row - 1 ][ column + 1 ][ 0 ] == 'b':
                        if row - 1 == 0:
                            moves.append( Move( ( row, column ), ( row - 1, column + 1 ), self.board, False, False, True ) )
                        else:
                            moves.append( Move( ( row, column ), ( row - 1, column + 1 ), self.board ) )
                    if self.board[ row ][ column + 1 ] == "bp" and self.moveLog[ -1 ].pieceMoved == "bp" and row == 3 and self.moveLog[ -1 ].startRow == 1 and self.moveLog[ -1 ].startColumn == ( column + 1 ):
                        moves.append( Move( ( row, column ), ( row - 1, column + 1 ), self.board, True ) ) 
                    

        if self.board[ row ][ column ][ 0 ] == 'b':
            if self.board[ row + 1 ][ column ] == "--":
                if not piecePinned or pinDirection == ( 1, 0 ) or pinDirection == ( -1, 0 ):
                    if row + 1 == 7:
                        moves.append( Move( ( row, column ), ( row + 1, column ), self.board, False, False, True ) )
                    else:
                        moves.append( Move( ( row, column ), ( row + 1, column ), self.board ) )
                if row == 1:    
                    if self.board[ row + 2 ][ column ] == "--":
                        if not piecePinned or pinDirection == ( 1, 0 ) or pinDirection( -1, 0 ):
                            moves.append( Move(( row, column ), ( row + 2, column ), self.board ) )
            if column != 0:
                if not piecePinned or pinDirection == ( 1, -1 ) or pinDirection == ( -1, 1 ):
                    if self.board[ row + 1 ][ column - 1 ][ 0 ] == 'w':
                        if row + 1 == 7:
                            moves.append( Move( ( row, column ), ( row + 1, column - 1), self.board, False, False, True ) )
                        else:
                            moves.append( Move( ( row, column ), ( row + 1, column - 1 ), self.board ) )
                    if self.board[ row ][ column - 1 ] == "wp" and self.moveLog[ -1 ].pieceMoved == "wp" and row == 4 and self.moveLog[ -1 ].startRow == 6 and self.moveLog[ -1 ].startColumn == ( column - 1 ):
                        moves.append( Move( ( row, column ), ( row + 1, column - 1 ), self.board, True) ) 
            if column != 7:
                if not piecePinned or pinDirection == ( 1, -1 ) or pinDirection == ( -1, 1 ):
                    if self.board[ row + 1 ][ column + 1 ][ 0 ] == 'w':
                        if row + 1 == 7:
                            moves.append( Move( ( row, column ), ( row + 1, column + 1), self.board, False, False, True ) )
                        else:
                            moves.append( Move( ( row, column ), ( row + 1, column + 1 ), self.board ) )
                    if self.board[ row ][ column + 1 ] == "wp" and self.moveLog[ -1 ].pieceMoved == "wp" and row == 4 and self.moveLog[ -1 ].startRow == 6 and self.moveLog[ -1 ].startColumn == ( column + 1 ):
                        moves.append( Move( ( row, column ), ( row + 1, column + 1 ), self.board, True) ) 
        
        


    def getRookMoves( self, row, column, moves ):
        piecePinned = False
        pinDirection = ()
        for i in range( len( self.pins ) -1, -1, -1 ):
            if self.pins[ i ][ 0 ] == row and self.pins[ i ][ 1 ] == column:
                piecePinned = True
                pinDirection = ( self.pins[ i ][ 2 ], self.pins[ i ][ 3 ])
                if self.board[ row ][ column ][ 1 ] != 'Q':
                    self.pins.remove( self.pins[ i ] )
                break

        opponentColor = 'b'
        if self.board[ row ][ column ][ 0 ] == 'b':
            opponentColor = 'w'
        
        i = row + 1
        if not piecePinned or pinDirection == ( 1, 0 ) or pinDirection == ( -1, 0 ):
            while i < 8:
                if self.board[ i ][ column ] == "--":
                    moves.append( Move( ( row, column ), ( i, column ), self.board ) )
                if self.board[ i ][ column ][ 0 ] == opponentColor:
                    moves.append( Move( ( row, column ), ( i, column ), self.board ) )
                    break
                if self.board[ i ][ column ][ 0 ] == self.board[ row ][ column ][ 0 ]:
                    break
                i += 1

        i = row - 1
        if not piecePinned or pinDirection == ( -1, 0 ) or pinDirection == ( 1, 0 ):
            while i >= 0:   
                if self.board[ i ][ column ] == "--":
                    moves.append( Move( ( row, column ), ( i, column ), self.board ) )
                if self.board[ i ][ column ][ 0 ] == opponentColor:
                    moves.append( Move( ( row, column ), ( i, column ), self.board ) )
                    break
                if self.board[ i ][ column ][ 0 ] == self.board[ row ][ column ][ 0 ]:
                    break
                i -= 1 

        i = column + 1
        if not piecePinned or pinDirection == ( 0, 1 ) or pinDirection == ( 0, -1 ):
            while i < 8:    
                if self.board[ row ][ i ] == "--":
                    moves.append( Move( ( row, column ), ( row, i ), self.board ) )
                if self.board[ row ][ i ][ 0 ] == opponentColor:
                    moves.append( Move( ( row, column ), ( row, i ), self.board ) )
                    break
                if self.board[ row ][ i ][ 0 ] == self.board[ row ][ column ][ 0 ]:
                    break
                i += 1
            
        i = column - 1
        if not piecePinned or pinDirection == ( 0, 1 ) or pinDirection == ( 0, -1 ):
            while i >= 0:
                if self.board[ row ][ i ] == "--":
                    moves.append( Move( ( row, column ), ( row, i ), self.board ) )
                if self.board[ row ][ i ][ 0 ] == opponentColor:
                    moves.append( Move( ( row, column ), ( row, i ), self.board ) )
                    break
                if self.board[ row ][ i ][ 0 ] == self.board[ row ][ column ][ 0 ]:
                    break
                i -= 1

    def getKnightMoves( self, row, column, moves ):
        piecePinned = False
        for i in range( len( self.pins ) -1, -1, -1 ):
            if self.pins[ i ][ 0 ] == row and self.pins[ i ][ 1 ] == column:
                piecePinned = True
                self.pins.remove( self.pins[ i ] )
                break
        
        moveList = {
            ( -2, 1 ), ( -1, 2 ), ( 1, 2 ), ( 2, 1 ),
            ( 2, -1 ), ( 1, -2 ), ( -2, -1 ), ( -1, -2 )
        }
        if not piecePinned:
            for diff in moveList:
                toRow = row + diff[ 0 ]
                toColumn =  column + diff[ 1 ]
                if ( ( 0 <= toRow < 8 ) and ( 0 <= toColumn < 8 ) ):
                    if self.board[ toRow ][ toColumn ][ 0 ] != self.board[ row ][ column ][ 0 ]:
                        moves.append( Move( ( row, column ), ( toRow, toColumn ), self.board ) )

    def getBishopMoves( self, row, column, moves ):
        piecePinned = False
        pinDirection = ()
        for i in range( len( self.pins ) -1, -1, -1 ):
            if self.pins[ i ][ 0 ] == row and self.pins[ i ][ 1 ] == column:
                piecePinned = True
                pinDirection = ( self.pins[ i ][ 2 ], self.pins[ i ][ 3 ])
                if self.board[ row ][ column ][ 1 ] != 'Q':
                    self.pins.remove( self.pins[ i ] )
                break
        
        opponentColor = 'b' if self.whiteToMove else 'w'
        i = row + 1
        j = column + 1
        if not piecePinned or pinDirection == ( 1, 1 ) or pinDirection == ( -1, -1 ):
            while ( i < 8 and j < 8 ):
                if self.board[ i ][ j ] == "--":
                    moves.append( Move( ( row, column ), ( i, j ), self.board ) )
                if self.board[ i ][ j ][ 0 ] == opponentColor:
                    moves.append( Move( ( row, column ), ( i, j ), self.board ) )
                    break
                if self.board[ i ][ j ][ 0 ] == self.board[ row ][ column ][ 0 ]:
                    break
                i += 1
                j += 1

        i = row + 1
        j = column - 1
        if not piecePinned or pinDirection == ( -1, 1 )or pinDirection == ( 1, -1 ):
            while ( i < 8 and j >= 0 ):
                if self.board[ i ][ j ] == "--":
                    moves.append( Move( ( row, column ), ( i, j ), self.board ) )
                if self.board[ i ][ j ][ 0 ] == opponentColor:
                    moves.append( Move( ( row, column ), ( i, j ), self.board ) )
                    break
                if self.board[ i ][ j ][ 0 ] == self.board[ row ][ column ][ 0 ]:
                    break
                i += 1
                j -= 1

        i = row - 1
        j = column + 1
        if not piecePinned or pinDirection == ( -1, 1 ) or pinDirection == ( 1, -1 ):
            while ( i >= 0 and j < 8 ):
                if self.board[ i ][ j ] == "--":
                    moves.append( Move( ( row, column ), ( i, j ), self.board ) )
                if self.board[ i ][ j ][ 0 ] == opponentColor:
                    moves.append( Move( ( row, column ), ( i, j ), self.board ) )
                    break
                if self.board[ i ][ j ][ 0 ] == self.board[ row ][ column ][ 0 ]:
                    break
                i -= 1
                j += 1

        i = row - 1
        j = column - 1
        if not piecePinned or pinDirection == ( -1, -1 ) or pinDirection == ( 1, 1 ):
            while ( i >= 0 and j >= 0 ):
                if self.board[ i ][ j ] == "--":
                    moves.append( Move( ( row, column ), ( i, j ), self.board ) )
                if self.board[ i ][ j ][ 0 ] == opponentColor:
                    moves.append( Move( ( row, column ), ( i, j ), self.board ) )
                    break
                if self.board[ i ][ j ][ 0 ] == self.board[ row ][ column ][ 0 ]:
                    break
                i -= 1
                j -= 1
        

    def getQueenMoves( self, row, column, moves ):
        self.getBishopMoves( row, column, moves )
        self.getRookMoves( row, column, moves )

    def getKingMoves( self, row, column, moves ):
        moveList = {
            ( 1, 1 ), ( -1, 1 ), ( 1, -1 ), ( -1, -1 ),
            ( 1, 0 ), ( -1, 0 ), ( 0, 1 ), ( 0, -1 )
        }
        for diff in moveList:
            toRow = row + diff[ 0 ]
            toColumn =  column + diff[ 1 ]
            if ( ( 0 <= toRow < 8 ) and ( 0 <= toColumn < 8 ) ):
                if self.board[ toRow ][ toColumn ][ 0 ] != self.board[ row ][ column ][ 0 ]:
                    if self.board[ row ][ column ][ 0 ] == 'w':
                        self.whiteKingLocation = ( toRow, toColumn )
                    else:
                        self.blackKingLocation = ( toRow, toColumn )
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append( Move( ( row, column ), ( toRow, toColumn ), self.board ) )
                    if self.board[ row ][ column ][ 0 ] == 'w':
                        self.whiteKingLocation = ( row, column )
                    else:
                        self.blackKingLocation = ( row, column )
        if self.whiteToMove:
            if self.whiteKingMoved == 0:
                if self.leftWhiteRookMoved == 0 and self.board[ 7 ][ 2 ] == "--" and self.board[ 7 ][ 3 ] == "--":
                    self.whiteKingLocation = ( 7, 1 )
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        self.whiteKingLocation = ( 7, 2 )
                        inCheck, pins, checks = self.checkForPinsAndChecks()
                        if not inCheck:
                            self.whiteKingLocation = ( 7, 3 )
                            inCheck, pins, checks = self.checkForPinsAndChecks()
                            if not inCheck:
                                moves.append( Move( ( row, column ), ( 7, 0 ), self.board, False, True ) )
                elif self.rightWhiteRookMoved  == 0 and self.board[ 7 ][ 5 ] == "--" and self.board[ 7 ][ 6 ] == "--":
                    self.whiteKingLocation = ( 7, 5 )
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        self.whiteKingLocation = ( 7, 6 )
                        inCheck, pins, checks = self.checkForPinsAndChecks()
                        if not inCheck:
                            moves.append( Move( ( row, column ), ( 7, 7 ), self.board, False, True ) )
        else:
            if self.blackKingMoved == 0:
                if self.leftBlackRookMoved == 0 and self.board[ 0 ][ 2 ] == "--" and self.board[ 0 ][ 3 ] == "--":
                    self.blackKingLocation = ( 0, 1 )
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        self.blackKingLocation = ( 0, 2 )
                        inCheck, pins, checks = self.checkForPinsAndChecks()
                        if not inCheck:
                            self.blackKingLocation = ( 0, 3 )
                            inCheck, pins, checks = self.checkForPinsAndChecks()
                            if not inCheck:
                                moves.append( Move( ( row, column ), ( 0, 0 ), self.board, False, True ) )
                elif self.rightBlackRookMoved == 0 and self.board[ 0 ][ 5 ] == "--" and self.board[ 0 ][ 6 ] == "--":
                    self.blackKingLocation = ( 0, 5 )
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        self.blackKingLocation = ( 0, 6 )
                        inCheck, pins, checks = self.checkForPinsAndChecks()
                        if not inCheck:
                            moves.append( Move( ( row, column ), ( 0, 7 ), self.board, False, True ) )


                    
    
    def checkForPinsAndChecks( self ):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            opponentColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[ 0 ]
            startColumn = self.whiteKingLocation[ 1 ]
        else:
            opponentColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[ 0 ]
            startColumn = self.blackKingLocation[ 1 ]
        directions = ( ( -1, 0 ), ( 0, -1 ), ( 1, 0 ), ( 0, 1 ), ( -1, -1 ), ( -1, 1 ), ( 1, -1 ), ( 1, 1 ) )
        for i in range( len( directions ) ):
            d = directions[ i ]
            possiblePin = ()
            for j in range( 1, 8 ):
                endRow = startRow + j * d[ 0 ]
                endColumn = startColumn + j * d[ 1 ]
                if 0 <= endRow <= 7 and 0 <= endColumn <= 7:
                    endPiece = self.board[ endRow ][ endColumn ]
                    if endPiece[ 0 ] == allyColor:
                        if possiblePin == ():
                            possiblePin = ( endRow, endColumn, d[ 0 ], d[ 1 ] )
                        else:
                            break
                    elif endPiece[ 0 ] == opponentColor:
                        pieceType = endPiece[ 1 ]
                        if (( pieceType == 'R' and 0 <= i <= 3 ) or \
                                ( pieceType == 'B' and 4 <= i <= 7 ) or \
                                ( pieceType == 'Q' ) or \
                                ( pieceType == 'p' and j == 1 and ( ( opponentColor == 'w' and 6 <= i <= 7 )  or ( opponentColor == 'b' and 4 <= i <= 5 ) ) ) or \
                                ( pieceType == 'K' and j == 1 ) ): 
                            if possiblePin == ():
                                inCheck = True
                                checks.append( ( endRow, endColumn, d[ 0 ], d[ 1 ] ) )
                                break
                            else:
                                pins.append( possiblePin )
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ( ( 2, 1 ), ( 2, -1 ), ( -2, 1 ), ( -2, -1 ), ( 1, 2 ), ( 1, -2 ), ( -1, 2 ), ( -1, -2 ) )
        for m in knightMoves:
            endRow = startRow + m[ 0 ]
            endColumn = startColumn + m[ 1 ]
            if 0 <= endRow <= 7 and 0 <= endColumn <= 7:
                endPiece = self.board[ endRow ][ endColumn ]
                if endPiece[ 0 ] == opponentColor and endPiece[ 1 ] == 'N':
                    inCheck = True
                    checks.append( ( endRow, endColumn, m [ 0 ], m[ 1 ] ) )
        return inCheck, pins, checks



    def getValidMoves( self ):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[ 0 ]
            kingColumn = self.whiteKingLocation[ 1 ]
        else:
            kingRow = self.blackKingLocation[ 0 ]
            kingColumn = self.blackKingLocation[ 1 ]
        if self.inCheck:
            if len( self.checks ) == 1:
                check = self.checks[ 0 ]
                moves = self.getPossibleMoves()
                checkRow = check[ 0 ]
                checkColumn = check[ 1 ]
                pieceChecking = self.board[ checkRow ][ checkColumn ]
                validSquares = []
                if pieceChecking[ 1 ] == 'N':
                    validSquares = [ ( checkRow, checkColumn ) ]
                else:
                    for i in range( 1, 8 ):
                        validSquare = ( kingRow + check[ 2 ] * i, kingColumn + check[ 3 ] * i )
                        validSquares.append( validSquare )
                        if validSquare[ 0 ] == checkRow and validSquare [ 1 ] == checkColumn:
                            break
                for i in range( len( moves ) -1, -1, -1 ):
                    if moves[ i ].pieceMoved[ 1 ] != 'K':
                        if not ( moves[ i ].endRow, moves[ i ].endColumn ) in validSquares:
                            moves.remove( moves[ i ] )
            else:
                self.getKingMoves( kingRow, kingColumn, moves )
        else:
            moves = self.getPossibleMoves()
        return moves

    def getPossibleMoves( self ):
        moves = []
        for i in range( len( self.board ) ):
            for j in range( len( self.board[ i ] ) ):
                color = self.board[ i ][ j ][ 0 ]
                if ( color == 'w' and self.whiteToMove ) or ( color == 'b' and not self.whiteToMove ):
                    piece = self.board[ i ][ j ][ 1 ]
                    self.moveFunctions[ piece ]( i, j, moves )

        return moves
                    




class Move():

    rankToRows = {
        "1" : 7, "2" : 6, "3" : 5, "4" : 4,
        "5" : 3, "6" : 2, "7" : 1, "8" : 0  
    }
    rowsToRanks = { v: k for k , v in rankToRows.items() }
    filesToColumns = {
        "a" : 0, "b" : 1, "c" : 2, "d" : 3,
        "e" : 4, "f" : 5, "g" : 6, "h" : 7  
    }
    columnsToFiles = { v: k for k , v in filesToColumns.items() }

    def __init__( self, startSq, endSq, board, isEnpassant = False, isCastle = False, isPromotion = False ):
        self.startRow = startSq[ 0 ]
        self.startColumn = startSq[ 1 ]
        self.endRow = endSq[ 0 ]
        self.endColumn = endSq[ 1 ]
        self.enpassant = isEnpassant
        self.castle = isCastle
        self.promotion = isPromotion
        self.pieceMoved = board[ self.startRow ][ self.startColumn ]
        self.pieceCaptured = board[ self.endRow ][ self.endColumn ]
        self.moveID = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn

    def __eq__( self, other ):
        if isinstance( other, Move ):
            return self.moveID == other.moveID
        return False


    def getRankFile( self, rank, column ):
        return self.columnsToFiles[ column ] + self.rowsToRanks[ rank ]


    def getChessNotation( self ):
        return self.getRankFile( self.startRow, self.startColumn) + self.getRankFile( self.endRow, self.endColumn )
    


































