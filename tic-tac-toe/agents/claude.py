from agents.base import BaseAgent, Move
from pydantic_ai import Agent

class ClaudeAgent(BaseAgent):

    name = "Claude"

    agent = Agent(
        model="anthropic:claude-sonnet-4-6",
        output_type=Move,
        system_prompt="You are playing tic-tac-toe. You will be given the current board state and your marker. Select a position to maximise your probability of winning."
    )

    def get_move(self, board: list[list[str | None]], marker:str) -> Move:
        
        prompt = f"You are playing as {marker}. Here is the current board:\n\n{self._format_board(board)}"
        result = self.agent.run_sync(prompt)

        return result.output

    def _format_board(self, board: list[list[str | None]]) -> str:
        rows = []
        for row in board:
            rows.append(" | ".join(cell if cell is not None else "." for cell in row))
        return "\n".join(rows)

