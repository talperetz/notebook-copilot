import os

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI

from notebook_copilot.prompts import cells_completion_prompt_template, multiple_cells_completion_parser, \
    CellCompletionList, markdown_explain_prompt_template


def get_llm(model_type='openai', model_name='gpt-3.5-turbo', key=None):
    """Get a language model from the LangChain API."""
    if key is None:
        key = os.getenv('LANGCHAIN_API_KEY')
    if key is None:
        raise ValueError('API key not provided and LANGCHAIN_API_KEY environment variable is not set.')
    llm = ChatOpenAI()
    llm.temperature = 0.0
    llm.max_tokens = 1000
    llm.openai_api_key = key
    llm.model_name = model_name
    return llm


def get_cells_completion(llm, run_history, cell=None) -> CellCompletionList:
    """Get a completion from the LangChain API."""
    chain = LLMChain(llm=llm, prompt=cells_completion_prompt_template)
    output = chain.predict(run_history=run_history, cell=cell)
    return multiple_cells_completion_parser.parse(output)


def explain_cell_completion(llm, run_history, cell=None) -> str:
    """Get a markdown explanation for current cell"""
    chain = LLMChain(llm=llm, prompt=markdown_explain_prompt_template)
    return chain.predict(run_history=run_history, cell=cell)
