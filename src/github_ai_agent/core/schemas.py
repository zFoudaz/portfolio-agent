from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum

class CardDecision(BaseModel):
    is_card: bool = Field(...,description="is this question can be answerd by the predefined answers or llm should answer")
    card: Literal['Me', 'Projects', 'Skills', 'Fun', 'Contact'] | None = Field(description="if a card is needed return the type of the card in this field")
