from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class ResearchInsights(BaseModel):
    insights: list[str] = Field(
        description="Key insights synthesized from the research evidence."
    )
    supporting_evidence: list[str] = Field(
        description="Evidence supporting each major insight."
    )
    source_references: list[str] = Field(
        description="Sources supporting the extracted insights."
    )


def build_insight_extraction_chain(llm: ChatGroq):
    prompt_path = Path("prompts/insight_extraction_prompt.txt")
    prompt_text = prompt_path.read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_text),
            (
                "human",
                "Research Topic:\n{research_topic}\n\n"
                "Research Summary:\n{research_summary}\n\n"
                "Source Material:\n{source_text}"
            ),
        ]
    )

    structured_llm = llm.with_structured_output(ResearchInsights)

    return prompt | structured_llm