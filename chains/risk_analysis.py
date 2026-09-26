from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class RiskAnalysis(BaseModel):
    risks: list[str] = Field(
        description="Risks identified from the available evidence."
    )
    risk_evidence: list[str] = Field(
        description="Evidence supporting the identified risks."
    )
    uncertainties: list[str] = Field(
        description="Uncertainties or limitations in the evidence."
    )


def build_risk_analysis_chain(llm: ChatGroq):
    prompt_path = Path("prompts/risk_analysis_prompt.txt")
    prompt_text = prompt_path.read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_text),
            (
                "human",
                "Research Topic:\n{research_topic}\n\n"
                "Research Summary:\n{research_summary}\n\n"
                "Key Insights:\n{insights}\n\n"
                "Source Material:\n{source_text}"
            ),
        ]
    )

    structured_llm = llm.with_structured_output(RiskAnalysis)

    return prompt | structured_llm