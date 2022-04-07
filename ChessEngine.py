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
        

class Moves():
    
    # maps keys to values 
    # key: value 
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
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
        
        