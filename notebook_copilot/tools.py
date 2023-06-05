from typing import Optional

from IPython import get_ipython
from langchain.tools import BaseTool, HumanInputRun

from notebook_copilot.context import get_ipython_run_history
from notebook_copilot.output import generate_notebook_cell_below
from notebook_copilot.prompts import CellType, CellCompletion


class NewCodeCellTool(BaseTool):
    name = "Notebook New Code Cell"
    description = (
        "use this tool when you want to create a new Code cell in the notebook. "
        "To use the tool you must provide the following parameter: 'content' (string)"
    )

    def _run(
            self,
            content: Optional[str] = None,
    ):
        generate_notebook_cell_below(CellCompletion(type=CellType.CODE, content=content))

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


class NewMarkdownCellTool(BaseTool):
    name = "Notebook New Markdown Cell"
    description = (
        "use this tool when you want to create a new Markdown cell in the notebook. "
        "To use the tool you must provide the following parameter: 'content' (string)."
    )

    def _run(
            self,
            content: Optional[str] = None,
    ):
        generate_notebook_cell_below(CellCompletion(type=CellType.MARKDOWN, content=content))

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


class NotebookHistoryTool(BaseTool):
    name = "Notebook Run History"
    description = (
        "use this tool when you need to know what has been ran in this notebook in the past."
    )

    def _run(
            self
    ):
        return get_ipython_run_history()

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


class InstalledPackagesTool(BaseTool):
    name = "Notebook Installed Packages"
    description = (
        "use this tool when you need to know what packages are installed in this python environment."
    )

    def _run(
            self
    ):
        return get_ipython().system('pip freeze')

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


HumanInTheLoopTool = HumanInputRun(input_func=input)
HumanInTheLoopTool.description = "Useful for when you need to ask the user a question."
