import pytest
from IPython.testing.globalipapp import get_ipython
from dotenv import load_dotenv

from notebook_copilot.models import MarkdownCompletion, CodeCompletion
from notebook_copilot.notebook_copilot import CopilotMagics

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


from unittest.mock import Mock


def test_code_with_mock(ipython, copilot_magic, mocker):
    # Create a mock of LLMChain
    mock_llm_chain = Mock()

    # Set the return value of predict method
    completion = CodeCompletion(source='print("Hello, world!")')
    mock_llm_chain.predict.return_value = completion.json()

    # Now mock the LLMChain constructor to always return our mock
    mocker.patch('notebook_copilot.chains.LLMChain', return_value=mock_llm_chain)

    # Now proceed with the test. All instances of LLMChain will use the mock
    ipython.run_cell_magic('code', '', 'your test code here')

    mock_llm_chain.predict.assert_called_once()


def test_optimize_with_mock(ipython, copilot_magic, mocker):
    # Create a mock of LLMChain
    mock_llm_chain = Mock()

    # Set the return value of predict method
    completion = CodeCompletion(source='print("Hello, world!")')
    mock_llm_chain.predict.return_value = completion.json()

    # Now mock the LLMChain constructor to always return our mock
    mocker.patch('notebook_copilot.chains.LLMChain', return_value=mock_llm_chain)

    # Now proceed with the test. All instances of LLMChain will use the mock
    ipython.run_cell_magic('optimize', '', 'your test code here')

    mock_llm_chain.predict.assert_called_once()


def test_visualize_with_mock(ipython, copilot_magic, mocker):
    # Create a mock of LLMChain
    mock_llm_chain = Mock()

    # Set the return value of predict method
    completion = CodeCompletion(source='print("Hello, world!")')
    mock_llm_chain.predict.return_value = completion.json()

    # Now mock the LLMChain constructor to always return our mock
    mocker.patch('notebook_copilot.chains.LLMChain', return_value=mock_llm_chain)

    # Now proceed with the test. All instances of LLMChain will use the mock
    ipython.run_cell_magic('visualize', '', 'your test code here')

    mock_llm_chain.predict.assert_called_once()


def test_explain_with_mock(ipython, copilot_magic, mocker):
    # Create a mock of LLMChain
    mock_llm_chain = Mock()

    # Set the return value of predict method
    completion = MarkdownCompletion(source='# This is a markdown cell')
    mock_llm_chain.predict.return_value = completion.json()

    # Now mock the LLMChain constructor to always return our mock
    mocker.patch('notebook_copilot.chains.LLMChain', return_value=mock_llm_chain)

    ipython.run_cell_magic('explain', '', '#complex code')

    mock_llm_chain.predict.assert_called_once()
