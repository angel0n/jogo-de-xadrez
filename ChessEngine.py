# esta classe é responsável por armazenar todas as informações sobre o estado atual de um jogo de xadrez.
# Ele também será responsável por determinar os movimentos válidos no wstate atual. Ele também manterá um registro de movimento.

from shutil import move


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
        self.moveFunctions = {'P': self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

    #Toma um movimento como parâmetro e o executa (isso não funcionará para roque, promoção de peões)
    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players         
    
    #desfaz o ultimo movimento
    def undoMove(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    
    def getValidMoves(self):
        return self.getAllPossibleMoves() #por enquanto não vamos nos preocupar com cheques
    
    # todos os movimentos sem considerar cheques
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
           for column in range(len(self.board[row])):
             turn = self.board[row][column][0]
             if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                 piece = self.board[row][column][1]
                 self.moveFunctions[piece](row,column,moves) #chama a função de movimento apropriada com base no tipo de peça
                     
        return moves
    
    #obtenha todos os movimentos de peão para o peão localizado na linha, coluna e adicione esses movimentos à lista
    def getPawnMoves(self,row,column, moves):
        if self.whiteToMove: #verifica peões brancos
            if row - 1 >= 0:
                if self.board[row - 1][column] == '--': # peão avança 1 quadrado
                    moves.append( Move( (row,column),(row-1,column),self.board ) )
                    if row == 6 and self.board[row - 2][column] == '--':# peão avança 2 quadrado
                        moves.append( Move( (row,column),(row-2,column),self.board ) )
                if column - 1 >= 0: #captura para a esquerda
                    if self.board[row - 1][column - 1][0] == 'b': #captura a peça
                        moves.append( Move( (row,column),(row-1,column-1),self.board))
                if column + 1 <= 7:#captura para a direita
                    if self.board[row-1][column+1][0] == 'b': #captura a peça
                        moves.append( Move( (row,column),(row-1,column+1),self.board))
        else: #verifica peões pretos
            if row + 1 <= 7:
                if self.board[row+1][column] == '--':
                    moves.append( Move( (row,column),(row+1,column),self.board))
                    if row == 1 and self.board[row+2][column] == '--':
                        moves.append( Move( (row,column),(row+2,column),self.board))
                if column - 1 >= 0:
                    if self.board[row+1][column-1][0] == 'w': 
                        moves.append( Move( (row,column),(row+1,column-1),self.board))
                if column +1 <= 7:
                    if self.board[row+1][column+1][0] == 'w':
                        moves.append( Move( (row,column),(row+1,column+1),self.board))  

    #obtenha todos os movimentos de torre para a torre localizada na linha, coluna e adicione esses movimentos à lista
    def getRookMoves(self,row,column, moves):
        direcoes = ((-1,0),(0,-1),(1,0),(0,1)) # cima, esquerda, baixo,direita
        enemy = 'b' if self.whiteToMove else 'w'
        for direcao in direcoes:
            for i in range(1,8):
                endRow = row + direcao[0] * i
                endColumn = column + direcao[1] * i
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    endPiece = self.board[endRow][endColumn]
                    if endPiece == '--':
                        moves.append( Move( (row,column),(endRow,endColumn),self.board))
                    elif endPiece[0] == enemy:
                        moves.append( Move( (row,column),(endRow,endColumn),self.board))
                        break
                    else:
                        break
                else:
                    break
    
    #obtenha todos os movimentos de cavalo para o cavalo localizada na linha, coluna e adicione esses movimentos à lista
    def getKnightMoves(self,row,column, moves):
        enemy = 'b' if self.whiteToMove else 'w'
        if row + 2 < 8:
            if column + 1 < 8:
                if self.board[row+2][column+1]  == '--' or self.board[row+2][column+1][0] == enemy: 
                    moves.append( Move( (row,column),(row+2,column+1),self.board))
            if column - 1 >= 0:
                if self.board[row+2][column-1]  == '--' or self.board[row+2][column-1][0] == enemy: 
                    moves.append( Move( (row,column),(row+2,column-1),self.board))
        if row - 2 >= 0:
            if column + 1 < 8:
                if self.board[row-2][column+1]  == '--' or self.board[row-2][column+1][0] == enemy: 
                    moves.append( Move( (row,column),(row-2,column+1),self.board))
            if column - 1 >= 0:
                if self.board[row-2][column-1]  == '--' or self.board[row-2][column-1][0] == enemy: 
                    moves.append( Move( (row,column),(row-2,column-1),self.board))
        if column + 2 < 8:
            if row + 1 < 8:
                if self.board[row+1][column+2]  == '--' or self.board[row+1][column+2][0] == enemy: 
                    moves.append( Move( (row,column),(row+1,column+2),self.board))
            if row - 1 >= 0:
                if self.board[row-1][column+2]  == '--' or self.board[row-1][column+2][0] == enemy: 
                    moves.append( Move( (row,column),(row-1,column+2),self.board))
        if column - 2 >= 0:
            if row + 1 < 8:
                if self.board[row+1][column-2]  == '--' or self.board[row+1][column-2][0] == enemy: 
                    moves.append( Move( (row,column),(row+1,column-2),self.board))
            if row - 1 >= 0:
                if self.board[row-1][column-2]  == '--' or self.board[row-1][column-2][0] == enemy: 
                    moves.append( Move( (row,column),(row-1,column-2),self.board))
        
                    


    #obtenha todos os movimentos do bispo para o bispo localizada na linha, coluna e adicione esses movimentos à lista
    def getBishopMoves(self,row,column, moves):
        pass

    #obtenha todos os movimentos da rainha para a rainha localizada na linha, coluna e adicione esses movimentos à lista
    def getQueenMoves(self,row,column, moves):
        pass

    #obtenha todos os movimentos do rei para o rei localizada na linha, coluna e adicione esses movimentos à lista
    def getKingMoves(self,row,column, moves):
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
        
    #Substituindo o método equals
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    
    
    
    
    def getChessNotation(self):
        # adicionar para fazer isso como notações reais de xadrez
        return self.getRankFile(self.startRow,self.startColumn) + self.getRankFile(self.endRow,self.endColumn) 

    def getRankFile(self, row, column):
        return self.colsToFiles[column] + self.rowsToRanks[row] 