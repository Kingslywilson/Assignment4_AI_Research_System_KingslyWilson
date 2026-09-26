from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class ResearchSummary(BaseModel):
    summary: str = Field(
        description="A grounded summary of the research evidence."
    )
    major_findings: list[str] = Field(
        description="Major findings supported by the sources."
    )
    evidence_gaps: list[str] = Field(
        description="Important areas where evidence is insufficient."
    )


def build_summarization_chain(llm: ChatGroq):
    prompt_path = Path("prompts/summarization_prompt.txt")
    prompt_text = prompt_path.read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_text),
            (
                "human",
                "Research Topic:\n{research_topic}\n\n"
                "Topic Analysis:\n{topic_analysis}\n\n"
                "Source Material:\n{source_text}"
            ),
        ]
    )

    structured_llm = llm.with_structured_output(ResearchSummary)

    return prompt | structured_llm