from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class FinalReport(BaseModel):
    title: str = Field(
        default="Research Report",
        description="Title of the final research report."
    )
    research_topic: str = Field(
        description="The research topic being analyzed."
    )
    executive_summary: str = Field(
        description="Concise executive summary."
    )
    research_scope: str = Field(
        description="Scope and coverage of the research analysis."
    )
    key_findings: list[str] = Field(
        description="Major research findings supported by the supplied sources."
    )
    key_insights: list[str] = Field(
        description="Key synthesized insights supported by the supplied sources."
    )
    risks_and_challenges: list[str] = Field(
        description="Important risks, challenges, and uncertainties supported by the evidence."
    )
    recommendations: list[str] = Field(
        description="Evidence-based recommendations."
    )
    conclusion: str = Field(
        description="Concluding synthesis and takeaways of the research report."
    )
    citations: list[str] = Field(
        default_factory=list,
        description=(
            "Complete source citations. Each citation must identify the "
            "source number and original source details."
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