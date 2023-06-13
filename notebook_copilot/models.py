import enum
from typing import List

from pydantic import BaseModel, Field


class CellType(enum.Enum):
    CODE = "code"
    MARKDOWN = "markdown"
    RAW = "raw"


class CompletionType(enum.Enum):
    CODE = "code"
    EXPLAIN = "explain"
    OPTIMIZE = "optimize"
    VISUALIZE = "visualize"


class CellCompletion(BaseModel):
    cell_type: CellType = Field(description="type of jupyter notebook cell")
    source: str = Field(description="code or markdown text of jupyter notebook cell")


class MarkdownCompletion(BaseModel):
    source: str = Field(
        description="string with valid markdown syntax.")


class CodeCompletion(BaseModel):
    source: str = Field(
        description="string in valid python syntax")


class CellCompletionList(BaseModel):
    cells: List[CellCompletion]
