import argparse
import contextlib
import os

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from langchain.document_loaders import NotebookLoader

from notebook_copilot.agents import get_cot_notebook_agent, AgentStrategy, agent_strategy_type, \
    get_plan_execute_notebook_agent
from notebook_copilot.chains import get_llm, get_cells_completion, explain_cell_completion
from notebook_copilot.context import get_ipython_run_history, compress_notebook_context
from notebook_copilot.output import generate_notebook_cells, reset_first_cell_index, generate_notebook_cell_above
from notebook_copilot.prompts import CellCompletion, COPILOT_PERSONA, COPILOT_TASK, COPILOT_DIRECTIONS
from notebook_copilot.utils import stringify_docs


@magics_class
class CopilotMagics(Magics):
    llm = None
    notebook_docs = None
    agent_strategy = None

    @line_magic
    def copilot_init(self, line):
        with contextlib.suppress(KeyboardInterrupt):
            parser = argparse.ArgumentParser()
            parser.add_argument('-m', '--model', default='gpt-3.5-turbo',
                                help='Model name to use.  e.g gpt-3.5-turbo')
            parser.add_argument('-k', '--api-key', default=None,
                                help='API key to use. If not provided, OPENAI_API_KEY environment variable will be used.')
            valid_agent_strategies = ", ".join([strategy.name for strategy in AgentStrategy])
            parser.add_argument('-s', '--strategy', type=agent_strategy_type, default=AgentStrategy.COT,
                                help=f'The strategy to use. one of: {valid_agent_strategies}')
            parser.add_argument('-n', '--notebook-path', default=None,
                                help='the current notebook path e.g /home/user/notebooks/this_notebook.ipynb')
            parser.add_argument('-i', '--ignore-notebook', default=None,
                                help='run copilot without the notebook context')

            # Parse the line input
            args = parser.parse_args(line.split())

            # Check if the API key is provided in the arguments
            api_key = os.getenv('OPENAI_API_KEY') if args.api_key is None else args.api_key
            if api_key is None:
                raise ValueError('API key not provided and OPENAI_API_KEY environment variable is not set.')

            if args.notebook_path is None:
                raise ValueError(
                    'Notebook path must be set. e.g %copilot_init -n /home/user/notebooks/this_notebook.ipynb')

            self.llm = get_llm(key=api_key, model_name=args.model)
            self.agent_strategy = args.strategy
            notebook = NotebookLoader(args.notebook_path,
                                      remove_newline=True).load()
            self.notebook_docs = compress_notebook_context(notebook)

    @cell_magic
    def generate(self, line, cell):
        with contextlib.suppress(KeyboardInterrupt):
            run_history = get_ipython_run_history()
            cell = cell.replace(line, '')
            completions = get_cells_completion(self.llm, run_history, cell=cell)
            generate_notebook_cells(completions.cell_completions)

    @cell_magic
    def explain(self, line, cell):
        with contextlib.suppress(KeyboardInterrupt):
            run_history = get_ipython_run_history()
            cell = cell.replace(line, '')
            markdown = explain_cell_completion(self.llm, run_history, cell=cell)
            generate_notebook_cell_above(CellCompletion(content=markdown, type='markdown'))

    @line_magic
    def copilot(self, _):
        with contextlib.suppress(KeyboardInterrupt):
            context = f'here\'s the relevant notebook text:\n"{stringify_docs(self.notebook_docs)}"\nhere\'s the notebook run history:\n"{get_ipython_run_history()}"'
            agent_prompt = f"{COPILOT_PERSONA}\n\nyour task:{COPILOT_TASK}\n\ndirections:{COPILOT_DIRECTIONS}\n\ncontext:{context}"
            reset_first_cell_index()
            if self.agent_strategy in [AgentStrategy.COT, AgentStrategy.TOT]:
                cot_agent = get_cot_notebook_agent(self.llm)
                cot_agent.run(agent_prompt)
            elif self.agent_strategy == AgentStrategy.PLAN_EXECUTE:
                plan_execute_agent = get_plan_execute_notebook_agent()
                plan_execute_agent.run(agent_prompt)


def load_ipython_extension(ipython):
    """
    This function is called when the extension is loaded.
    """
    ipython.register_magics(CopilotMagics)
