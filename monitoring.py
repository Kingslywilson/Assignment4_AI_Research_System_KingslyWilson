import os
from typing import Any, Dict, Optional

from langchain_core.callbacks import BaseCallbackHandler


class ResearchMonitoringCallback(BaseCallbackHandler):

    def __init__(self):
        super().__init__()

        self.stage_usage: Dict[str, Dict[str, Any]] = {}
        self.current_stage: Optional[str] = None

    def start_stage(self, stage_name: str) -> None:
        self.current_stage = stage_name

        self.stage_usage[stage_name] = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "calls": 0,
        }

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: list[str],
        **kwargs: Any,
    ) -> None:
        if self.current_stage is None:
            return

        self.stage_usage[self.current_stage]["calls"] += 1

    def on_llm_end(
        self,
        response: Any,
        **kwargs: Any,
    ) -> None:
        if self.current_stage is None:
            return

        usage = {}

        if hasattr(response, "llm_output") and response.llm_output:
            usage = response.llm_output.get(
                "token_usage",
                {}
            )

        input_tokens = usage.get(
            "prompt_tokens",
            usage.get("input_tokens", 0)
        )

        output_tokens = usage.get(
            "completion_tokens",
            usage.get("output_tokens", 0)
        )

        total_tokens = usage.get(
            "total_tokens",
            input_tokens + output_tokens
        )

        self.stage_usage[self.current_stage][
            "input_tokens"
        ] += input_tokens

        self.stage_usage[self.current_stage][
            "output_tokens"
        ] += output_tokens

        self.stage_usage[self.current_stage][
            "total_tokens"
        ] += total_tokens

    def get_stage_usage(
        self,
        stage_name: str
    ) -> Dict[str, Any]:
        return self.stage_usage.get(
            stage_name,
            {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "calls": 0,
            }
        )

    def get_all_usage(self) -> Dict[str, Dict[str, Any]]:
        """
        Return usage information for all stages.
        """
        return self.stage_usage


def get_langsmith_config() -> Dict[str, str]:
    return {
        "tracing": os.getenv(
            "LANGSMITH_TRACING",
            "false"
        ),
        "api_key": os.getenv(
            "LANGSMITH_API_KEY",
            ""
        ),
        "project": os.getenv(
            "LANGSMITH_PROJECT",
            "ai-research-system"
        ),
    }