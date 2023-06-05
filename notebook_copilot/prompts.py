import enum
from typing import List

from langchain import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

COPILOT_PERSONA = "You are a senior Data Scientist and staff Software Engineer that is helpful, polite, honest, sophisticated, and humble-but-knowledgeable. You follow Data science best practices."
COPILOT_TASK = "Create new jupyter notebook code & markdown cells (take one action at each step!) to continue this notebook based on ML and Data science best practices with clean code and descriptive markdown."
COPILOT_DIRECTIONS = "Use the provided context to infer the continuation of this notebook. Be very thorough - before each code cell you create, add descriptive markdown cells to elaborate on the flow and code to make the notebook readable and professional. After finishing with the notebook - ask the user if there's something more they want to accomplish."


class CellType(enum.Enum):
    CODE = "code"
    MARKDOWN = "markdown"


class CellCompletion(BaseModel):
    type: CellType = Field(description="type of jupyter notebook cell")
    content: str = Field(description="the content of jupyter notebook cell based on type")


class MarkdownCompletion(BaseModel):
    content: str = Field(
        description="string in valid markdown syntax. you can use headings, text, lists, links, and latex formulas")


class CellCompletionList(BaseModel):
    cell_completions: List[CellCompletion]


cell_completion_parser = PydanticOutputParser(pydantic_object=CellCompletion)
markdown_completion_parser = PydanticOutputParser(pydantic_object=MarkdownCompletion)
multiple_cells_completion_parser = PydanticOutputParser(pydantic_object=CellCompletionList)

cells_completion_prompt_template = PromptTemplate(
    input_variables=["run_history", "cell"],
    template="{copilot_persona}\nContext:\nrun history: {run_history}.\n current cell: {cell}\nYour task: Putting most weight on the current cell and code comments, Generate the next Jupyter notebook cells by replying in the following format: {format_instructions}",
    partial_variables={"copilot_persona": COPILOT_PERSONA,
                       "format_instructions": multiple_cells_completion_parser.get_format_instructions()},
)

markdown_explain_prompt_template = PromptTemplate(
    input_variables=["run_history", "cell"],
    template="{copilot_persona}\nYour task: Generate a markdown cell to explain what we're trying to achieve in the next cell professionally. Directions: Reply with a string. use markdown syntax only, don't share any code, set a descriptive heading for your markdown cell (e.g ## Feature Engineering).\nrun history: {run_history}.\n next cell: {cell}",
    partial_variables={"copilot_persona": COPILOT_PERSONA},
)
