import json
from typing import List

from IPython.core.display import Javascript
from IPython.core.display_functions import display

from notebook_copilot.prompts import CellCompletion


def generate_notebook_cells(completions: List[CellCompletion]):
    first_completion = completions[0]
    cell_content_as_json = json.dumps(first_completion.content)
    cell_type = first_completion.type.value
    display(Javascript(f"""
                var cell = IPython.notebook.insert_cell_above('{cell_type}');
                window.firstCellIndex = IPython.notebook.find_cell_index(cell);
                cell.set_text({cell_content_as_json});
            """))
    for completion in completions[1:]:
        cell_content_as_json = json.dumps(completion.content)
        cell_type = completion.type.value
        index_adjustment = ' + 1'
        display(Javascript(f"""
                var cell = IPython.notebook.insert_cell_at_index('{cell_type}', window.firstCellIndex{index_adjustment});
                cell.set_text({cell_content_as_json});
                window.firstCellIndex = IPython.notebook.find_cell_index(cell);
                """))


def generate_notebook_cell_below(completion: CellCompletion):
    cell_content_as_json = json.dumps(completion.content)
    cell_type = completion.type.value
    display(Javascript(f"""
            if (window.firstCellIndex === undefined) {{
                var cell = IPython.notebook.insert_cell_below('{cell_type}');
                window.firstCellIndex = IPython.notebook.find_cell_index(cell);
                cell.set_text({cell_content_as_json});
            }} else {{
                var cell = IPython.notebook.insert_cell_at_index('{cell_type}', window.firstCellIndex + 1);
                cell.set_text({cell_content_as_json});
                window.firstCellIndex = IPython.notebook.find_cell_index(cell);
            }}
            """))


def generate_notebook_cell_above(completion: CellCompletion):
    cell_content_as_json = json.dumps(completion.content)
    cell_type = completion.type.value
    display(Javascript(f"""
                    var selected_cell_index = IPython.notebook.get_selected_index();
                    var cell = IPython.notebook.insert_cell_at_index('{cell_type}', selected_cell_index - 1);
                    cell.set_text({cell_content_as_json});
                    """))


def reset_first_cell_index():
    display(Javascript(f"""window.firstCellIndex === undefined;"""))
