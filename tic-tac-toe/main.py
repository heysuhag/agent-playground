from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")
from board import Board
from game import Game
import random
from agents.claude import ClaudeAgent
from agents.gpt import OAIAgent


claude = ClaudeAgent()
oai = OAIAgent()

def decide_order(p1,p2):
    if random.random() < 0.5:
        return (p1,p2)
    else:
        return (p2,p1)

player1, player2 = decide_order(claude,oai)

board = Board()

game = Game(board, player1=player1, player2=player2)

while not game.game_over():
    print('-'*37)
    current = game.current_player
    print(f"Current player : {current} || Marker : {game.marker[current]}")
    move = current.get_move(board=game.board.board, marker=game.marker[current])
    print(f"Reasoning: {move.reasoning}")
    game.play((move.row, move.col))
    print('-'*37)

