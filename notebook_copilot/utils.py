import os
import sys
from enum import Enum
from typing import List

from IPython import get_ipython
from langchain.schema import Document


class JupyterEnvironment(Enum):
    GOOGLE_COLAB = 'Google Colab'
    JUPYTER_NOTEBOOK = 'Jupyter Notebook'
    DATABRICKS = 'Databricks'
    JUPYTER_LAB = 'Jupyter Lab'
    SAGEMAKER = 'Amazon SageMaker'
    UNKNOWN = 'Unknown environment'


def check_environment():
    if 'google.colab' in str(get_ipython()):
        return JupyterEnvironment.GOOGLE_COLAB
    elif 'databricks' in sys.modules:
        return JupyterEnvironment.DATABRICKS
    elif 'sagemaker' in sys.modules:
        return JupyterEnvironment.SAGEMAKER
    elif 'jpnotebook' in os.environ.get('JUPYTER_SERVER_TYPE', '').lower():
        return JupyterEnvironment.JUPYTER_LAB
    elif 'IPython' in sys.modules or 'ipykernel' in sys.modules:
        return JupyterEnvironment.JUPYTER_NOTEBOOK
    else:
        return JupyterEnvironment.UNKNOWN

def pretty_print_docs(docs: List[Document]):
    print(f"\n{'-' * 100}\n".join([f"Document {i + 1}:\n\n" + d.page_content for i, d in enumerate(docs)]))


def stringify_docs(docs: List[Document]):
    return f"\n".join([d.page_content for d in docs])
