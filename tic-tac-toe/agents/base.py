from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class Move(BaseModel):
    row: int = Field(ge=0, le=2)
    col: int = Field(ge=0, le=2)
    reasoning: str
    one_line_reasoning: str

class BaseAgent(ABC):

    @abstractmethod
    def get_move(self, board: list[list[str | None]], marker:str) -> Move:
        ...