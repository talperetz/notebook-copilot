import argparse
import contextlib
import os

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from langchain.document_loaders import NotebookLoader

from notebook_copilot.agents import get_cot_notebook_agent, AgentStrategy, agent_strategy_type, \
    get_plan_execute_notebook_agent
from notebook_copilot.chains import get_llm, get_cells_completion
from notebook_copilot.context import get_ipython_run_history, compress_notebook_context
from notebook_copilot.models import CellType, CellCompletion, CompletionType
from notebook_copilot.output import reset_first_cell_index, generate_notebook_cell_above, \
    generate_notebook_cell_below
from notebook_copilot.prompts import COPILOT_PERSONA, COPILOT_TASK, COPILOT_DIRECTIONS
from notebook_copilot.utils import stringify_docs, check_environment, JupyterEnvironment


@magics_class
class CopilotMagics(Magics):
    def build_llm_from_args(self, line):
        parser = argparse.ArgumentParser()
        parser.add_argument('-m', '--model', default='gpt-3.5-turbo',
                            help='Model name to use.  e.g gpt-3.5-turbo')

        args = parser.parse_args(line.split())

        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            raise ValueError('API key not provided and OPENAI_API_KEY environment variable is not set.')

        return get_llm(key=api_key, model_name=args.model)

    @cell_magic
    def code(self, line, cell):
        with contextlib.suppress(KeyboardInterrupt):
            run_history = get_ipython_run_history()
            cell = cell.replace(line, '')
            code_completion = get_cells_completion(self.build_llm_from_args(line), CompletionType.CODE, run_history,
                                                   cell=cell)
            generate_notebook_cell_below(CellCompletion(cell_type=CellType.CODE, source=code_completion.source))

    @cell_magic
    def optimize(self, line, cell):
        with contextlib.suppress(KeyboardInterrupt):
            run_history = get_ipython_run_history()
            cell = cell.replace(line, '')
            code_completion = get_cells_completion(self.build_llm_from_args(line), CompletionType.OPTIMIZE, run_history,
                                                   cell=cell)
            generate_notebook_cell_below(CellCompletion(cell_type=CellType.CODE, source=code_completion.source))

    @cell_magic
    def visualize(self, line, cell):
        with contextlib.suppress(KeyboardInterrupt):
            run_history = get_ipython_run_history()
            cell = cell.replace(line, '')
            code_completion = get_cells_completion(self.build_llm_from_args(line), CompletionType.VISUALIZE,
                                                   run_history, cell=cell)
            generate_notebook_cell_below(CellCompletion(cell_type=CellType.CODE, source=code_completion.source))

    @cell_magic
    def explain(self, line, cell):
        with contextlib.suppress(KeyboardInterrupt):
            run_history = get_ipython_run_history()
            cell = cell.replace(line, '')
            md_completion = get_cells_completion(self.build_llm_from_args(line), CompletionType.EXPLAIN, run_history,
                                                 cell=cell)
            generate_notebook_cell_above(CellCompletion(cell_type=CellType.MARKDOWN, source=md_completion.source))

    @line_magic
    def copilot(self, line):
        with contextlib.suppress(KeyboardInterrupt):
            parser = argparse.ArgumentParser()
            parser.add_argument(
                '-s',
                '--strategy',
                type=agent_strategy_type,
                default=AgentStrategy.COT,
                help='The strategy to use. one of: cot, tot, plan_execute',
            )
            parser.add_argument('-n', '--notebook-name', default=None,
                                help='the current name e.g -n Untitled')

            args = parser.parse_args(line.split())
            notebook_docs = None
            if args.notebook_name and check_environment() is JupyterEnvironment.JUPYTER_NOTEBOOK:
                notebook_path = os.path.join(os.getcwd(), f"{args.notebook_name}.ipynb")
                notebook = NotebookLoader(notebook_path, remove_newline=True).load()
                notebook_docs = compress_notebook_context(notebook)
            context = f'here\'s the relevant notebook text:\n"{stringify_docs(notebook_docs)}"' if notebook_docs else f'here\'s the notebook run history:\n"{get_ipython_run_history()}'
            user_input = input("What do you want to accomplish with the Jupyter notebook?")
            agent_prompt = f"{COPILOT_PERSONA}\n\nyour task:{COPILOT_TASK}\n\ndirections:{COPILOT_DIRECTIONS}\n\ncontext:{context} user_input:{user_input}"
            reset_first_cell_index()
            if args.strategy in [AgentStrategy.COT, AgentStrategy.TOT]:
                cot_agent = get_cot_notebook_agent(self.build_llm_from_args(line))
                cot_agent.run(agent_prompt)
            elif args.strategy == AgentStrategy.PLAN_EXECUTE:
                plan_execute_agent = get_plan_execute_notebook_agent()
                plan_execute_agent.run(agent_prompt)


def load_ipython_extension(ipython):
    """
    This function is called when the extension is loaded.
    """
    ipython.register_magics(CopilotMagics)
