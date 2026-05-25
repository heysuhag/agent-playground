from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

import random

from agents.claude import ClaudeAgent
from agents.gpt import OAIAgent
from board import Board
from game import Game
from gui import GameRenderer
from voice import Voice

claude = ClaudeAgent()
oai   = OAIAgent()

def decide_order(p1, p2):
    if random.random() < 0.5:
        return (p1, p2)
    else:
        return (p2, p1)

player1, player2 = decide_order(claude, oai)
player1_voice = Voice(gender='female')
player2_voice = Voice()

board = Board()
game  = Game(board, player1=player1, player2=player2)
renderer = GameRenderer(x_name=player1.name, o_name=player2.name)

x_reasoning = ""
o_reasoning  = ""

while not game.game_over():
    if not renderer.handle_events():
        break

    current = game.current_player
    marker  = game.marker[current]

    renderer.draw(game.board.board, x_reasoning, o_reasoning, marker)

    move = current.get_move(board=game.board.board, marker=marker)

    if marker == "X":
        x_reasoning = move.one_line_reasoning
        player1_voice.speak(x_reasoning)
    else:
        o_reasoning = move.one_line_reasoning
        player2_voice.speak(o_reasoning)

    game.play((move.row, move.col))

winner = game.board.win_detection()
if winner:
    winner_name = player1.name if winner == "X" else player2.name
    renderer.draw_winner(game.board.board, winner_name, x_reasoning, o_reasoning)
else:
    renderer.draw_draw(game.board.board, x_reasoning, o_reasoning)

renderer.wait_for_close()
