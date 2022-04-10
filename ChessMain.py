# este é o nosso arquivo de driver principal. ele será responsável por manipular a entrada do usuário e exibir o objeto GameStae atual

import pygame
import ChessEngine

#definiçoes de tamanho
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 
IMAGES ={}

#carrega as imagens
def loadImage():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('images/'+piece+'.png'), (SQ_SIZE,SQ_SIZE) )

#metodo principal, executa o programa
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT)) #seta a tela
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white")) #pinta a tela de branco
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #variável de sinalizador para quando um movimento é feito
    
    loadImage()    
    running = True #flag para controlar o loop principal
    sqSelected = () # inicialmente nenhum quadrado está selecionado, keep track of this last click of the user (tuple:(row,column))
    playerClicks = [] #acompanhar os cliques  (duas tuples: [(6,4),(4,4)])
    while running:
        for e in pygame.event.get(): #loop para capturar eventos
            if e.type == pygame.QUIT: #evento para fechar a janela  
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN: #evento para pegar quando o mouse é clicado
                location = pygame.mouse.get_pos() # pega a posição do mouse
                column = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE 
                if sqSelected == (row,column):
                    sqSelected = () # desmarcar
                    playerClicks = [] #limpa os click do player
                else:
                    sqSelected = (row,column) #seleciona
                    playerClicks.append(sqSelected) # adiciona click de player
                if len(playerClicks) == 2: #verifica se o usuário clicou duas vezes
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () 
                    playerClicks = [] 
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undoMove()
                    moveMade = True
                
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()

#desenha o tabuleiro
def drawGameState(screen,gs): 
    drawBoard(screen)
    drawPiece(screen,gs.board)

#desenha os quadrados do tabuleiro 
def drawBoard(screen): 
   colors = [pygame.Color("white"), pygame.Color("gray")]
   for row in range(DIMENSION):
       for columns in range(DIMENSION):
           color = colors[((row+columns) % 2)]
           pygame.draw.rect(screen, color, pygame.Rect(columns*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE)) 

#desenha as peças do tabuleiro
def drawPiece(screen,board):
    for row in range(DIMENSION):
        for columns in range(DIMENSION):
            piece = board[row][columns]
            if piece != "--":
                screen.blit(IMAGES[piece],pygame.Rect(columns*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))

main()

