from board import Board
from game import Game

board = Board()
p1 = 'ant'
p2 = 'gem'

game = Game(board, player1=p1, player2=p2)

#moves = [(0,0), (1,0), (0,1), (1,1), (0,2), (2,2)]
#moves = [(0,0), (0,1), (0,2), (1,1), (1,0), (1,2), (2,2), (2,0), (2,1)]
moves = [(0,0), (1,0), (0,1), (1,1), (2,2), (1,2)]

for move in moves:
    if game.game_over():
        break
    else:
        game.play(move)