from pathlib import Path

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class Recommendations(BaseModel):
    recommendations: list[str] = Field(
        description="Recommendations supported by the research evidence."
    )
    rationale: list[str] = Field(
        description="Evidence-based rationale for each recommendation."
    )
    limitations: list[str] = Field(
        description="Limitations that should be considered before applying recommendations."
    )


def build_recommendation_chain(llm: ChatGroq):
    prompt_path = Path("prompts/recommendation_prompt.txt")
    prompt_text = prompt_path.read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_text),
            (
                "human",
                "Research Topic:\n{research_topic}\n\n"
                "Research Summary:\n{research_summary}\n\n"
                "Key Insights:\n{insights}\n\n"
                "Risk Analysis:\n{risk_analysis}\n\n"
                "Source Material:\n{source_text}"
            ),
        ]
    )

    structured_llm = llm.with_structured_output(Recommendations)

    return prompt | structured_llm