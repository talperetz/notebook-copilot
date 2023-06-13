from langchain import PromptTemplate
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
)

from notebook_copilot.parsers import multiple_cells_completion_parser, code_completion_parser

COPILOT_PERSONA = "You are a senior Data Scientist that writes professional and readable jupyter notebooks for the user. You are helpful, polite, honest, sophisticated, and humble-but-knowledgeable. You follow Data science best practices."
COPILOT_TASK = "Begin by understanding what the user want to accomplish. Then help the user by creating new jupyter notebook code & markdown cells to continue this notebook based on ML and Data science best practices with clean code and descriptive markdown."
COPILOT_DIRECTIONS = "Use the provided context and user input to continue this notebook. Be very thorough - before each code cell you create, add descriptive markdown cells to elaborate on the flow and code to make the notebook readable and professional. Before finishing your actions - ask the user if there's something more they want to accomplish."

explain_format_instructions = """
The output should be formatted as a JSON instance that conforms to the JSON schema below.

Here is the output schema:
```
{"properties": {"source": {"title": "Source", "description": "string with valid markdown syntax.", "type": "string"}}, "required": ["source"]}
```

example response: {"source": "## Data Cleaning\nIn the next cell, we clean the data using the following methods:\n* Removing duplicates\n Missing values imputation"}
"""

cells_completion_prompt_template = PromptTemplate(
    input_variables=["run_history", "cell"],
    template="{copilot_persona}\nContext:\nrun history: {run_history}.\n current cell: {cell}\nYour task: Putting most weight on the current cell and code comments, Generate the next Jupyter notebook cells by replying in the following format: {format_instructions}",
    partial_variables={"copilot_persona": COPILOT_PERSONA,
                       "format_instructions": multiple_cells_completion_parser.get_format_instructions()},
)

markdown_explain_prompt_template = PromptTemplate(
    input_variables=["cell"],
    template='You are a professional data science code/pipeline/process instructor and storyteller. You follow Data science best practices and generate beautifully formatted Jupyter Notebook markdown cell (up to 4 lines. no code inside.) to explain the flow in the input code cell.\n\nReply with your output according to the directions below.\nDirections: "{format_instructions}\n\nHere is the code cell source code to explain:\n{cell}.',
    partial_variables={"format_instructions": explain_format_instructions},
)

code_generation_prompt_template = PromptTemplate(
    input_variables=["run_history", "cell"],
    template="You are a data science code generator. You follow Data science best practices and generate Jupyter notebook code cells based on user requests.\n\nGenerate python code based on the user input\nuser input: {cell}.\n\nReply with your output according to the directions below.\nDirections: {format_instructions}\n\nipython run history for context (optional): {run_history}.",
    partial_variables={"format_instructions": code_completion_parser.get_format_instructions()},
)

code_optimization_prompt_template = PromptTemplate(
    input_variables=["cell"],
    template="You are an experienced software engineer. Please help me improve the time complexity of the the following code cell\n{cell}.\n\nGenerate python code that is optimized for performance.\n\nReply with your output according to the directions below.\nDirections: {format_instructions}\n\n",
    partial_variables={"format_instructions": code_completion_parser.get_format_instructions()},
)

code_visualization_prompt_template = PromptTemplate(
    input_variables=["run_history", "cell"],
    template="You are a data science code generator. You follow Data science best practices and generate Jupyter notebook code cells based on user requests.\n\nGenerate python code to visualize the data in the following code block. you can use seaborn, matplotlib etc…\ncode block: {cell}.\n\nReply with your output according to the directions below.\nDirections: {format_instructions}\n\nipython run history for context (optional): {run_history}.",
    partial_variables={"format_instructions": code_completion_parser.get_format_instructions()},
)



copilot_system_message_prompt = SystemMessagePromptTemplate.from_template(COPILOT_PERSONA)
