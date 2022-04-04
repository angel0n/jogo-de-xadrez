# this class is responsible for storing all the information about the current state of a chess game. It will also be 
# responsible for determining the valid moves at the current wstate. It will also keep a move log 

class GameState():
    def __init__(self):
        #board is an 8X8 2d list, each element of the list has 2 characters. 
        #The first character represents the color of the piece 'b' or 'w'
        #The second character represents the type of the piece 'K', 'Q', 'R', 'B', 'N' or 'P'
        #"--" represents an empty space with no piece 
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []