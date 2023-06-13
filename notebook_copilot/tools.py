from typing import Optional

from IPython import get_ipython
from langchain.tools import BaseTool, Tool

from notebook_copilot.context import get_ipython_run_history
from notebook_copilot.models import CellType, CellCompletion, CellCompletionList
from notebook_copilot.output import generate_notebook_cell_below, generate_notebook_cells


class AddNotebookCellsTool(BaseTool):
    name = "Notebook New Cells"
    description = (
        "Use this tool when you want to create new cells in the notebook. "
        "To use the tool you must provide the following parameter: 'cells' according to the CellCompletionList model."
    )
    
    def _run(
            self,
            cells: Optional[CellCompletionList] = None,
    ):
        cells = cells.cells if type(cells) == CellCompletionList else cells
        generate_notebook_cells(cells)
        return "created new cells"

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


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


UserInputTool = Tool.from_function(
    func=input,
    name="User Input Tool",
    description="Use it to get user input and direction before acting."
)
