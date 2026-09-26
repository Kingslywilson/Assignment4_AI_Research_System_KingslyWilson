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


INSUFFICIENT_EVIDENCE = (
    "Insufficient evidence is available in the supplied sources."
)


class ResearchPipeline:

    def __init__(
        self,
        llm: ChatGroq,
        memory: Optional[ResearchMemory] = None,
    ):
        self.llm = llm
        self.memory = memory or ResearchMemory()
        self.monitoring = ResearchMonitoringCallback()

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
    ) -> Dict[str, Any]:
        documents, failures = load_all_sources(
            urls=urls,
            pdf_directory=pdf_directory,
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
    ) -> Dict[str, Any]:

        research_topic = self.validate_topic(
            research_topic
        )

        urls = urls or []

        source_result = self.collect_sources(
            urls=urls,
            pdf_directory=pdf_directory,
        )

        documents = self.preprocess_sources(
            source_result["documents"]
        )

        self._ensure_sources(documents)

        source_text = prepare_source_text(
            documents
        )
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
        assistant_message = (
            final_report.model_dump_json()
        )

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