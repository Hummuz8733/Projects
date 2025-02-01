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
        self.blackKingLocation = ( 1, 4 )
        self.checkMate = False
        self.staleMate = False
        self.moveFunctions = {
            'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves
        }

    def makeMove( self, move ):
        self.board[ move.startRow ][ move.startColumn ] = "--"
        self.board[ move.endRow ][ move.endColumn ] = move.pieceMoved
        self.moveLog.append( move )
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = ( move.endRow, move.endColumn )
        if move.pieceMoved == "bK":
            self.blackKingLocation = ( move.endRow, move.endColumn )
        


    def undoMove( self ):
        if len( self.moveLog ) != 0:
            lastMove = self.moveLog.pop()
            self.board[ lastMove.startRow ][ lastMove.startColumn ] = lastMove.pieceMoved
            self.board[ lastMove.endRow ][ lastMove.endColumn ] = lastMove.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if lastMove.pieceMoved == "wK":
                self.whiteKingLocation = ( lastMove.startRow, lastMove.startColumn )
            if lastMove.pieceMoved == "bK":
                self.blackKingLocation = ( lastMove.startRow, lastMove.startColumn )

    def getPawnMoves( self, row, column, moves ):
        if self.board[ row ][ column ][ 0 ] == 'w':
            if self.board[ row - 1 ][ column ] == "--":
                moves.append( Move( ( row, column ), ( row - 1, column ), self.board ) )
                if row == 6:    
                    if self.board[ row - 2 ][ column ] == "--":
                        moves.append( Move(( row, column ), ( row - 2, column ), self.board ) )
            if column != 0:
                if self.board[ row - 1 ][ column - 1 ][ 0 ] == 'b':
                    moves.append( Move( ( row, column ), ( row - 1, column - 1 ), self.board ) )
            if column != 7:
                if self.board[ row - 1 ][ column + 1 ][ 0 ] == 'b':
                    moves.append( Move( ( row, column ), ( row - 1, column + 1 ), self.board ) )

        if self.board[ row ][ column ][ 0 ] == 'b':
            if self.board[ row + 1 ][ column ] == "--":
                moves.append( Move( ( row, column ), ( row + 1, column ), self.board ) )
                if row == 1:    
                    if self.board[ row + 2 ][ column ] == "--":
                        moves.append( Move(( row, column ), ( row + 2, column ), self.board ) )
            if column != 0:
                if self.board[ row + 1 ][ column - 1 ][ 0 ] == 'w':
                    moves.append( Move( ( row, column ), ( row + 1, column - 1 ), self.board ) )
            if column != 7:
                if self.board[ row + 1 ][ column + 1 ][ 0 ] == 'w':
                    moves.append( Move( ( row, column ), ( row + 1, column + 1 ), self.board ) )
        


    def getRookMoves( self, row, column, moves ):
        opponentColor = 'b'
        if self.board[ row ][ column ][ 0 ] == 'b':
            opponentColor = 'w'
        
        i = row + 1
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
        moveList = {
            ( -2, 1 ), ( -1, 2 ), ( 1, 2 ), ( 2, 1 ),
            ( 2, -1 ), ( 1, -2 ), ( -2, -1 ), ( -1, -2 )
        }
        for diff in moveList:
            toRow = row + diff[ 0 ]
            toColumn =  column + diff[ 1 ]
            if ( ( 0 <= toRow < 8 ) and ( 0 <= toColumn < 8 ) ):
                if self.board[ toRow ][ toColumn ][ 0 ] != self.board[ row ][ column ][ 0 ]:
                    moves.append( Move( ( row, column ), ( toRow, toColumn ), self.board ) )

    def getBishopMoves( self, row, column, moves ):
        opponentColor = 'b' if self.whiteToMove else 'w'
        i = row + 1
        j = column + 1
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
                    moves.append( Move( ( row, column ), ( toRow, toColumn ), self.board ) )
        
    def inCheck( self ):
        if self.whiteToMove:
            return self.sqUnderAttack( self.whiteKingLocation[ 0 ], self.whiteKingLocation[ 1 ] )
        else:
            return self.sqUnderAttack( self.blackKingLocation[ 0 ], self.blackKingLocation[ 1 ] )
            
    def sqUnderAttack( self, row, column ):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endColumn == column:
                return True
        return False

    def getValidMoves( self ):
        moves = self.getPossibleMoves()
        for i in range( len( moves ) - 1, -1, -1 ):
            self.makeMove( moves[ i ] )
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove( moves[ i ] )
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len( moves ) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
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

    def __init__( self, startSq, endSq, board ):
        self.startRow = startSq[ 0 ]
        self.startColumn = startSq[ 1 ]
        self.endRow = endSq[ 0 ]
        self.endColumn = endSq[ 1 ]
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
    


































