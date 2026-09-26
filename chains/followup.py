from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class FollowupResponse(BaseModel):
    is_ambiguous: bool = Field(
        description="True if the follow-up question is ambiguous, vague, or requires clarification; False if it is clear and specific."
    )
    clarification_message: Optional[str] = Field(
        default=None,
        description="If is_ambiguous is True, a message asking the user to clarify (e.g. 'Could you clarify which risks you mean?'). Otherwise None."
    )
    clarification_options: List[str] = Field(
        default_factory=list,
        description="If is_ambiguous is True, a list of 3 to 5 options for clarification (e.g. ['1. Security risks', '2. Privacy risks', '3. Operational risks', '4. Implementation risks']). Otherwise empty list."
    )
    answer: Optional[str] = Field(
        default=None,
        description="If is_ambiguous is False, a detailed answer grounded in the source material and research context. Otherwise None."
    )
    citations: List[str] = Field(
        default_factory=list,
        description="Source citations supporting the answer if is_ambiguous is False."
    )


def build_followup_chain(llm: ChatGroq):
    prompt_path = Path("prompts/followup_prompt.txt")

    prompt_text = prompt_path.read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_text),
            (
                "human",
                "Research Topic:\n{research_topic}\n\n"
                "Conversation History:\n{conversation_history}\n\n"
                "Follow-Up Question:\n{question}\n\n"
                "Source Material:\n{source_text}"
            ),
        ]
    )

    structured_llm = llm.with_structured_output(FollowupResponse)

    return prompt | structured_llm
