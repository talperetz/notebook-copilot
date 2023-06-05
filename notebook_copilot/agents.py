import argparse
from enum import Enum

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.experimental import load_chat_planner, load_agent_executor, PlanAndExecute
from langchain.memory import ConversationSummaryBufferMemory

from notebook_copilot.tools import NewMarkdownCellTool, NewCodeCellTool, InstalledPackagesTool, \
    NotebookHistoryTool, HumanInTheLoopTool


class AgentStrategy(Enum):
    COT = "cot"
    TOT = "tot"
    PLAN_EXECUTE = "plan_execute"


def agent_strategy_type(strategy):
    try:
        return AgentStrategy[strategy.upper()]
    except KeyError as e:
        raise argparse.ArgumentTypeError(f"Unknown strategy {strategy}") from e


def get_cot_notebook_agent(llm):
    tools = [NewMarkdownCellTool(), NewCodeCellTool(), HumanInTheLoopTool, InstalledPackagesTool()]
    conversational_memory = ConversationSummaryBufferMemory(
        max_token_limit=1000,
        llm=llm,
    )
    return initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=12,
        early_stopping_method='generate',
        handle_parsing_errors=True,
        memory=conversational_memory,
    )


def get_plan_execute_notebook_agent():
    tools = [NewMarkdownCellTool(), NewCodeCellTool(), HumanInTheLoopTool, NotebookHistoryTool(),
             InstalledPackagesTool()]
    model = ChatOpenAI(temperature=0)
    planner = load_chat_planner(model)
    executor = load_agent_executor(model, tools, verbose=True)
    return PlanAndExecute(planner=planner, executor=executor, verbose=True)
