from typing import Any, Dict

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish
from tqdm import tqdm


class ProgressHandler(BaseCallbackHandler):
    def __init__(self):
        self.pbar = None

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""
        print("Running chain...")
        self.pbar = tqdm(total=None)
        self.pbar.update()

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        self.pbar.update()

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
        self.pbar.close()
