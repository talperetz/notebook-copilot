import pytest
from IPython.testing.globalipapp import get_ipython
from dotenv import load_dotenv

from notebook_copilot.notebook_copilot import CopilotMagics
from notebook_copilot.prompts import CellCompletionList, CellCompletion

# Load the .env file
load_dotenv()


@pytest.fixture(scope='module')
def ipython():
    return get_ipython()


@pytest.fixture(scope='module')
def copilot_magic(ipython):
    copilot_magic = CopilotMagics(shell=ipython)
    ipython.register_magics(copilot_magic)
    return copilot_magic


def test_copilot_init(ipython, copilot_magic):
    # call your magic with
    ipython.run_line_magic('copilot_init',
                           '--model gpt-3.5-turbo --strategy COT --notebook-path ../examples/copilot_example_notebook.ipynb')
    # assert something about the result or state
    assert copilot_magic.llm is not None
    assert copilot_magic.notebook_docs is not None


from unittest.mock import Mock


def test_generate_with_mock(ipython, copilot_magic, mocker):
    # Create a mock of LLMChain
    mock_llm_chain = Mock()

    # Set the return value of predict method
    completion = CellCompletion(content='print("Hello, world!")', type='code')
    mock_llm_chain.predict.return_value = CellCompletionList(cell_completions=[completion]).json()

    # Now mock the LLMChain constructor to always return our mock
    mocker.patch('notebook_copilot.chains.LLMChain', return_value=mock_llm_chain)

    # Now proceed with the test. All instances of LLMChain will use the mock
    ipython.run_cell_magic('generate', '', 'your test code here')

    mock_llm_chain.predict.assert_called_once()


def test_explain_with_mock(ipython, copilot_magic, mocker):
    # Create a mock of LLMChain
    mock_llm_chain = Mock()

    # Set the return value of predict method
    mock_llm_chain.predict.return_value = "# This is a markdown cell"

    # Now mock the LLMChain constructor to always return our mock
    mocker.patch('notebook_copilot.chains.LLMChain', return_value=mock_llm_chain)

    ipython.run_cell_magic('explain', '', '!pip install pandas')

    mock_llm_chain.predict.assert_called_once()
