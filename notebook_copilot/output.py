from __future__ import annotations

import json
from typing import List

from IPython.core.display import Javascript
from IPython.core.display_functions import display

from notebook_copilot.models import CellCompletion


def generate_notebook_cells(completions: List[CellCompletion] | List[dict]):
    completions = [CellCompletion(source="".join(completion['source']), cell_type=completion["cell_type"]) if type(completion) == dict else completion for completion in completions]
    first_completion = completions[0]
    cell_content_as_json = json.dumps("".join(first_completion.source))
    cell_type = first_completion.cell_type.value
    display(Javascript(f"""
                var cell = IPython.notebook.insert_cell_above('{cell_type}');
                window.firstCellIndex = IPython.notebook.find_cell_index(cell);
                cell.set_text({cell_content_as_json});
            """))
    for completion in completions[1:]:
        cell_content_as_json = json.dumps("".join(completion.source))
        cell_type = completion.cell_type.value
        index_adjustment = ' + 1'
        display(Javascript(f"""
                var cell = IPython.notebook.insert_cell_at_index('{cell_type}', window.firstCellIndex{index_adjustment});
                cell.set_text({cell_content_as_json});
                window.firstCellIndex = IPython.notebook.find_cell_index(cell);
                """))


def generate_notebook_cell_below(completion: CellCompletion):
    cell_content_as_json = json.dumps(completion.source)
    cell_type = completion.cell_type.value
    display(Javascript(f"""
                        var selected_cell_index = IPython.notebook.get_selected_index();
                        var cell = IPython.notebook.insert_cell_at_index('{cell_type}', selected_cell_index);
                        cell.set_text({cell_content_as_json});
                        """))


def generate_notebook_cell_above(completion: CellCompletion):
    cell_content_as_json = json.dumps(completion.source)
    cell_type = completion.cell_type.value
    display(Javascript(f"""
                    var selected_cell_index = IPython.notebook.get_selected_index();
                    var cell = IPython.notebook.insert_cell_at_index('{cell_type}', selected_cell_index - 1);
                    cell.set_text({cell_content_as_json});
                    """))


def reset_first_cell_index():
    display(Javascript("""window.firstCellIndex === undefined;"""))
