from __future__ import annotations

import os

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI

from notebook_copilot.models import CellCompletion, CellCompletionList, CompletionType
from notebook_copilot.parsers import code_completion_parser, markdown_completion_parser
from notebook_copilot.prompts import markdown_explain_prompt_template, \
    code_generation_prompt_template, code_optimization_prompt_template, code_visualization_prompt_template

completion_type_to_prompt_template = {
    CompletionType.CODE: (code_generation_prompt_template, code_completion_parser),
    CompletionType.EXPLAIN: (markdown_explain_prompt_template, markdown_completion_parser),
    CompletionType.OPTIMIZE: (code_optimization_prompt_template, code_completion_parser),
    CompletionType.VISUALIZE: (code_visualization_prompt_template, code_completion_parser)
}


def get_llm(model_name='gpt-3.5-turbo', key=None):
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


def get_cells_completion(llm, completion_type, run_history, cell=None) -> CellCompletionList | CellCompletion:
    """Get a completion from the LangChain API."""
    prompt, output_parser = completion_type_to_prompt_template[completion_type]
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.predict(run_history=run_history, cell={cell})
    return output_parser.parse(output)
