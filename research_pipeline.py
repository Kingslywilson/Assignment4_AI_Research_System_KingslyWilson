from typing import Any, Dict, List, Optional

from langchain_groq import ChatGroq
from langchain_core.documents import Document

from data_loader import load_all_sources
from preprocess import preprocess_documents, prepare_source_text
from memory import ResearchMemory
from monitoring import ResearchMonitoringCallback

from chains.topic_analysis import build_topic_analysis_chain
from chains.summarization import build_summarization_chain
from chains.insight_extraction import build_insight_extraction_chain
from chains.risk_analysis import build_risk_analysis_chain
from chains.recommendation import build_recommendation_chain
from chains.report_generation import build_report_generation_chain
from chains.followup import build_followup_chain


INSUFFICIENT_EVIDENCE = (
    "Insufficient evidence is available in the supplied sources."
)


def format_report_markdown(report: dict) -> str:
    final_report = report.get("final_report", report)
    topic_str = final_report.get("research_topic", report.get("research_topic", ""))

    lines = [
        "# Research Report",
        "",
        "## Research Topic",
        "",
        topic_str,
        "",
        "## Executive Summary",
        "",
        final_report.get("executive_summary", ""),
        "",
        "## Research Scope",
        "",
        final_report.get("research_scope", ""),
        "",
        "## Key Findings",
        "",
    ]

    for finding in final_report.get("key_findings", []):
        lines.append(f"- {finding}")

    lines.extend(
        [
            "",
            "## Key Insights",
            "",
        ]
    )

    for insight in final_report.get("key_insights", []):
        lines.append(f"- {insight}")

    lines.extend(
        [
            "",
            "## Risks / Challenges",
            "",
        ]
    )

    for risk in final_report.get("risks_and_challenges", []):
        lines.append(f"- {risk}")

    lines.extend(
        [
            "",
            "## Recommendations",
            "",
        ]
    )

    for recommendation in final_report.get("recommendations", []):
        lines.append(f"- {recommendation}")

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            final_report.get("conclusion", ""),
            "",
            "## Sources / Citations",
            "",
        ]
    )

    for citation in final_report.get("citations", []):
        lines.append(f"- {citation}")

    return "\n".join(lines)


class ResearchPipeline:

    def __init__(
        self,
        llm: ChatGroq,
        memory: Optional[ResearchMemory] = None,
    ):
        self.llm = llm
        self.memory = memory or ResearchMemory()
        self.monitoring = ResearchMonitoringCallback()
        self.session_sources: Dict[str, Dict[str, Any]] = {}

        self.topic_analysis_chain = (
            build_topic_analysis_chain(llm)
        )

        self.summarization_chain = (
            build_summarization_chain(llm)
        )

        self.insight_extraction_chain = (
            build_insight_extraction_chain(llm)
        )

        self.risk_analysis_chain = (
            build_risk_analysis_chain(llm)
        )

        self.recommendation_chain = (
            build_recommendation_chain(llm)
        )

        self.report_generation_chain = (
            build_report_generation_chain(llm)
        )

        self.followup_chain = (
            build_followup_chain(llm)
        )

    def validate_topic(
        self,
        research_topic: str
    ) -> str:
        if not research_topic or not research_topic.strip():
            raise ValueError(
                "Research topic cannot be empty."
            )

        return research_topic.strip()

    def collect_sources(
        self,
        urls: List[str],
        pdf_directory: str = "data/pdfs",
        article_directory: str = "data/articles",
    ) -> Dict[str, Any]:
        documents, failures = load_all_sources(
            urls=urls,
            pdf_directory=pdf_directory,
            article_directory=article_directory,
        )

        return {
            "documents": documents,
            "failures": failures,
        }

    def preprocess_sources(
        self,
        documents: List[Document]
    ) -> List[Document]:
        return preprocess_documents(documents)

    def _ensure_sources(
        self,
        documents: List[Document]
    ) -> None:
        if not documents:
            raise ValueError(
                "No usable research sources are available."
            )

    def _stage_config(
        self,
        stage_name: str
    ) -> Dict[str, Any]:
        self.monitoring.start_stage(stage_name)

        return {
            "callbacks": [
                self.monitoring
            ]
        }

    def build_citations(
        self,
        documents: List[Document]
    ) -> List[str]:
        citations = []

        for index, document in enumerate(
            documents,
            start=1
        ):
            metadata = document.metadata or {}

            source_type = metadata.get(
                "source_type",
                "unknown"
            )

            if source_type == "web":
                title = metadata.get(
                    "title",
                    "Untitled Web Source"
                )

                url = metadata.get(
                    "url",
                    metadata.get(
                        "source",
                        "Unknown URL"
                    )
                )

                citations.append(
                    f"Source {index} — "
                    f"{title} — "
                    f"{url}"
                )

            elif source_type == "pdf":
                file_name = metadata.get(
                    "file_name",
                    metadata.get(
                        "source",
                        "Unknown PDF"
                    )
                )

                page_number = metadata.get(
                    "page_number",
                    metadata.get(
                        "page",
                        "Unknown"
                    )
                )

                citations.append(
                    f"Source {index} — "
                    f"{file_name} — "
                    f"Page {page_number}"
                )

            elif source_type == "article":
                file_name = metadata.get(
                    "file_name",
                    metadata.get(
                        "source",
                        "Unknown Article"
                    )
                )

                citations.append(
                    f"Source {index} — "
                    f"{file_name}"
                )

            else:
                source = metadata.get(
                    "source",
                    "Unknown Source"
                )

                citations.append(
                    f"Source {index} — "
                    f"{source}"
                )

        return citations

    def run(
        self,
        session_id: str,
        research_topic: str,
        urls: Optional[List[str]] = None,
        pdf_directory: str = "data/pdfs",
        article_directory: str = "data/articles",
    ) -> Dict[str, Any]:

        research_topic = self.validate_topic(
            research_topic
        )

        urls = urls or []

        source_result = self.collect_sources(
            urls=urls,
            pdf_directory=pdf_directory,
            article_directory=article_directory,
        )

        documents = self.preprocess_sources(
            source_result["documents"]
        )

        self._ensure_sources(documents)

        source_text = prepare_source_text(
            documents
        )

        self.session_sources[session_id] = {
            "research_topic": research_topic,
            "documents": documents,
            "source_text": source_text,
        }

        self.memory.add_message(
            session_id,
            "user",
            research_topic
        )
        topic_analysis = (
            self.topic_analysis_chain.invoke(
                {
                    "research_topic": research_topic,
                    "source_text": source_text,
                },
                config=self._stage_config(
                    "topic_analysis"
                ),
            )
        )
        research_summary = (
            self.summarization_chain.invoke(
                {
                    "research_topic": research_topic,
                    "topic_analysis": (
                        topic_analysis.model_dump_json()
                    ),
                    "source_text": source_text,
                },
                config=self._stage_config(
                    "summarization"
                ),
            )
        )
        insights = (
            self.insight_extraction_chain.invoke(
                {
                    "research_topic": research_topic,
                    "research_summary": (
                        research_summary.model_dump_json()
                    ),
                    "source_text": source_text,
                },
                config=self._stage_config(
                    "insight_extraction"
                ),
            )
        )
        risk_analysis = (
            self.risk_analysis_chain.invoke(
                {
                    "research_topic": research_topic,
                    "research_summary": (
                        research_summary.model_dump_json()
                    ),
                    "insights": (
                        insights.model_dump_json()
                    ),
                    "source_text": source_text,
                },
                config=self._stage_config(
                    "risk_analysis"
                ),
            )
        )
        recommendations = (
            self.recommendation_chain.invoke(
                {
                    "research_topic": research_topic,
                    "research_summary": (
                        research_summary.model_dump_json()
                    ),
                    "insights": (
                        insights.model_dump_json()
                    ),
                    "risk_analysis": (
                        risk_analysis.model_dump_json()
                    ),
                    "source_text": source_text,
                },
                config=self._stage_config(
                    "recommendation"
                ),
            )
        )
        final_report = (
            self.report_generation_chain.invoke(
                {
                    "research_topic": research_topic,
                    "research_summary": (
                        research_summary.model_dump_json()
                    ),
                    "insights": (
                        insights.model_dump_json()
                    ),
                    "risk_analysis": (
                        risk_analysis.model_dump_json()
                    ),
                    "recommendations": (
                        recommendations.model_dump_json()
                    ),
                    "source_text": source_text,
                },
                config=self._stage_config(
                    "report_generation"
                ),
            )
        )
        final_report.citations = (
            self.build_citations(documents)
        )
        report_dict = final_report.model_dump()
        assistant_message = format_report_markdown({"final_report": report_dict})

        self.memory.add_message(
            session_id,
            "assistant",
            assistant_message
        )
        return {
            "research_topic": research_topic,

            "source_count": len(documents),

            "source_failures": (
                source_result["failures"]
            ),

            "topic_analysis": (
                topic_analysis.model_dump()
            ),

            "research_summary": (
                research_summary.model_dump()
            ),

            "insights": (
                insights.model_dump()
            ),

            "risk_analysis": (
                risk_analysis.model_dump()
            ),

            "recommendations": (
                recommendations.model_dump()
            ),

            "final_report": (
                final_report.model_dump()
            ),

            "monitoring": (
                self.monitoring.get_all_usage()
            ),

            "conversation_history": (
                self.memory.get_history(
                    session_id
                )
            ),
        }

    def answer_followup(
        self,
        session_id: str,
        question: str,
    ) -> Dict[str, Any]:
        if not question or not question.strip():
            raise ValueError(
                "Follow-up question cannot be empty."
            )

        question = question.strip()

        session_data = self.session_sources.get(session_id)
        if not session_data:
            raise ValueError(
                f"No research session found for session_id '{session_id}'. Run research first."
            )

        research_topic = session_data["research_topic"]
        source_text = session_data["source_text"]
        documents = session_data["documents"]

        history_list = self.memory.get_history(session_id)
        history_formatted = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in history_list]
        )

        followup_res = self.followup_chain.invoke(
            {
                "research_topic": research_topic,
                "conversation_history": history_formatted,
                "question": question,
                "source_text": source_text,
            },
            config=self._stage_config("followup"),
        )

        self.memory.add_message(session_id, "user", question)

        if followup_res.is_ambiguous:
            opts = followup_res.clarification_options or []
            assistant_content = f"{followup_res.clarification_message}\n" + "\n".join(opts)
            self.memory.add_message(session_id, "assistant", assistant_content)
            return {
                "is_ambiguous": True,
                "clarification_message": followup_res.clarification_message or "Could you clarify which risks you mean?",
                "clarification_options": opts,
                "answer": None,
                "citations": [],
            }
        else:
            citations = followup_res.citations
            if not citations:
                citations = self.build_citations(documents)
            self.memory.add_message(session_id, "assistant", followup_res.answer or "")
            return {
                "is_ambiguous": False,
                "clarification_message": None,
                "clarification_options": [],
                "answer": followup_res.answer,
                "citations": citations,
            }

    def get_session_history(
        self,
        session_id: str
    ) -> List[Dict[str, Any]]:
        return self.memory.get_history(
            session_id
        )

    def reset_session(
        self,
        session_id: str
    ) -> None:
        self.memory.clear_session(
            session_id
        )
        self.session_sources.pop(session_id, None)