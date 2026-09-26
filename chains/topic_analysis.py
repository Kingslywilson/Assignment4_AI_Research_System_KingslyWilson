from pathlib import Path
from typing import List

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class TopicAnalysis(BaseModel):
    research_question: str = Field(
        description="The main research question derived from the topic."
    )
    scope: str = Field(
        description="The scope and boundaries of the research."
    )
    key_areas: List[str] = Field(
        description="Important areas that should be investigated."
    )
    evidence_requirements: List[str] = Field(
        description="Types of evidence needed to support the research."
    )


def build_topic_analysis_chain(llm: ChatGroq):
    prompt_path = Path("prompts/topic_analysis_prompt.txt")
    prompt_text = prompt_path.read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_text),
            (
                "human",
                "Research Topic:\n{research_topic}\n\n"
                "Source Material:\n{source_text}"
            ),
        ]
    )

    structured_llm = llm.with_structured_output(TopicAnalysis)

    return prompt | structured_llm