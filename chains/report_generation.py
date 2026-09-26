from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class FinalReport(BaseModel):
    title: str = Field(
        description="Title of the final research report."
    )
    executive_summary: str = Field(
        description="Concise executive summary."
    )
    findings: list[str] = Field(
        description="Major research findings supported by the supplied sources."
    )
    insights: list[str] = Field(
        description="Key synthesized insights supported by the supplied sources."
    )
    risks: list[str] = Field(
        description="Important risks and uncertainties supported by the evidence."
    )
    recommendations: list[str] = Field(
        description="Evidence-based recommendations."
    )
    limitations: list[str] = Field(
        description="Research limitations and evidence gaps."
    )
    citations: list[str] = Field(
        description=(
            "Complete source citations. Each citation must identify the "
            "source number and the original source details. For web sources, "
            "include the source title and full URL. For PDF sources, include "
            "the file name and page number. Do not return only 'Source 1', "
            "'Source 2', etc."
        )
    )


def build_report_generation_chain(llm: ChatGroq):
    prompt_path = Path(
        "prompts/report_generation_prompt.txt"
    )

    prompt_text = prompt_path.read_text(
        encoding="utf-8"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_text),
            (
                "human",
                "Research Topic:\n{research_topic}\n\n"
                "Research Summary:\n{research_summary}\n\n"
                "Key Insights:\n{insights}\n\n"
                "Risk Analysis:\n{risk_analysis}\n\n"
                "Recommendations:\n{recommendations}\n\n"
                "Source Material:\n{source_text}"
            ),
        ]
    )

    structured_llm = llm.with_structured_output(
        FinalReport
    )

    return prompt | structured_llm