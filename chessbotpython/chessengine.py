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

    def makeMove( self, move ):
        self.board[ move.startRow ][ move.startColumn ] = "--"
        self.board[ move.endRow ][ move.endColumn ] = move.pieceMoved
        self.moveLog.append( move )
        self.whiteToMove = not self.whiteToMove

    def undoMove( self ):
        if len( self.moveLog ) != 0:
            lastMove = self.moveLog.pop()
            self.board[ lastMove.startRow ][ lastMove.startColumn ] = lastMove.pieceMoved
            self.board[ lastMove.endRow ][ lastMove.endColumn ] = lastMove.pieceCaptured
            self.whiteToMove = not self.whiteToMove



    def getValidMoves( self ):
        return self.getPossibleMoves()

    def getPossibleMoves( self ):
        moves = []
        for i in range( len( self.board ) ):
            for j in range( len( self.board[ i ] ) ):
                color = self.board[ i ][ j ][ 0 ]




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

    def getRankFile( self, rank, column ):
        return self.columnsToFiles[ column ] + self.rowsToRanks[ rank ]


    def getChessNotation( self ):
        return self.getRankFile( self.startRow, self.startColumn) + self.getRankFile( self.endRow, self.endColumn )
    


































