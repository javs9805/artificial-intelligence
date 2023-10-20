import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, ROWS, COLS
from checkers.game import Game
from minimax.algorithm import minimax, minimax_alpha_beta, get_all_moves
import time
import random
import json

JUEGA_HUMANO = False
DEPTH = 3

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    lista_tiempos = []
    game.update()

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            # MINIMAX
            start1 = time.time()
            value, new_board = minimax(game.get_board(), DEPTH, WHITE, game)
            end1 = time.time()
            # MINIMAX CON PODA ALPHA BETA
            start2 = time.time()
            value2, new_board_2 = minimax_alpha_beta(game.get_board(), DEPTH, WHITE, game, float('-inf'), float('inf'))
            end2 = time.time()
            if value != value2:
                print("error")         
            lista_tiempos.append([(end1 - start1), (end2 - start2)])
            game.ai_move(random.choice([new_board, new_board_2]))
        
        elif game.turn == RED and not JUEGA_HUMANO:
            moves = get_all_moves(game.get_board(), RED, game)
            time.sleep(1)
            game.ai_move(random.choice(moves))

        if game.winner() != None:
            print(game.winner())
            run = False
            print("-------------------------------")
            print ("minimax vs alpha_beta")
            print("-------------------------------")
            for item in lista_tiempos:
                print ('{:.2f}'.format(round(item[0], 2)), "\t\t", '{:.2f}'.format(round(item[1], 2)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    time.sleep(3)
    pygame.quit()

main()