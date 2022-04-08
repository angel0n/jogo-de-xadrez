# esta classe é responsável por armazenar todas as informações sobre o estado atual de um jogo de xadrez.
# Ele também será responsável por determinar os movimentos válidos no wstate atual. Ele também manterá um registro de movimento.

class GameState():
    def __init__(self):
        #placa é uma lista 2d 8X8, cada elemento da lista tem 2 caracteres.
        # O primeiro caractere representa a cor da peça 'b' ou 'w'
        #O segundo caractere representa o tipo da peça 'K', 'Q', 'R', 'B', 'N' ou 'P'
        #"--" representa um espaço vazio sem peça
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

    #Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en passant)
    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players         
    
    # undo the last move made
    def undoMove(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    
    def getValidMoves(self):
        return self.getAllPossibleMoves() #for now we will not worry about checks
    
    #all moves without considering checks 
    def getAllPossibleMoves(self):
        moves = [Move((6,4),(4,4),self.board)]
        for row in range(len(self.board)):
           for column in range(len(self.board[row])):
             turn = self.board[row][column][0]
             if(turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                 piece = self.board[row][column][1]
                 if piece == 'P':
                     self.getPawnMoves(row, column, moves)
                 elif piece == 'R':
                     self.getRookMoves(row, column, moves)
                     
        return moves
    
    #get all pawn moves for the pawn located at row, col and add these moves to the list
    def getPawnMoves(self,row,column, moves):
        pass
    
    #get all rook moves for the rook located at row, col and add these moves to the list
    def getRookMoves(self,row,column, moves):
        pass


class Move():
     
    # faz o mapeamento das linhas e colunas, sendo contado de baixo para cima 
    # ultima fileira seria a 8 mas na lista board ela é a linha 0 
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    #inverte os valores e chaves da variavel de cima
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    #realiza a mesma coisa mas com as colunas 
    filesToCols = {"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7} 
    colsToFiles = {v:k for k,v in filesToCols.items()}
    
    
    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startColumn = startSq[1]
        self.endRow = endSq[0]
        self.endColumn = endSq[1]
        self.pieceMoved = board[self.startRow][self.startColumn] #peça que foi movida
        self.pieceCaptured = board[self.endRow][self.endColumn] #peça que foi capturada/destino da peça movida
        self.moveID = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn
        
    #Overriding the equals method 
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    
    
    
    
    def getChessNotation(self):
        # adicionar para fazer isso como notações reais de xadrez
        return self.getRankFile(self.startRow,self.startColumn) + self.getRankFile(self.endRow,self.endColumn) 

    def getRankFile(self, row, column):
        return self.colsToFiles[column] + self.rowsToRanks[row] 