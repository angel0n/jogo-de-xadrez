# this is our main driver file. it will be responsible for hendling user input and displaying the current GameStae object

import pygame
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 
IMAGES ={}

def loadImage():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('images/'+piece+'.png'), (SQ_SIZE,SQ_SIZE) )
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    loadImage( )    
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def drawGameState(screen,gs):
    drawBoard(screen)
    drawPiece(screen,gs.board)
    
def drawBoard(screen):
   colors = [pygame.Color("white"), pygame.Color("gray")]
   for row in range(DIMENSION):
       for columns in range(DIMENSION):
           color = colors[((row+columns) % 2)]
           pygame.draw.rect(screen, color, pygame.Rect(columns*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE)) 

def drawPiece(screen,board):
    for row in range(DIMENSION):
        for columns in range(DIMENSION):
            piece = board[row][columns]
            if piece != "--":
                screen.blit(IMAGES[piece],pygame.Rect(columns*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))

main()