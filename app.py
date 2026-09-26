import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from research_pipeline import ResearchPipeline


load_dotenv()


def create_llm() -> ChatGroq:

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured. "
            "Add it to the .env file."
        )

    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=api_key,
    )


def save_report(report: dict) -> str:

    output_path = Path(
        "outputs/research_report.md"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    final_report = report["final_report"]

    lines = [
        f"# {final_report['title']}",
        "",
        "## Executive Summary",
        "",
        final_report["executive_summary"],
        "",
        "## Findings",
        "",
    ]

    for finding in final_report["findings"]:
        lines.append(f"- {finding}")

    lines.extend(
        [
            "",
            "## Key Insights",
            "",
        ]
    )

    for insight in final_report["insights"]:
        lines.append(f"- {insight}")

    lines.extend(
        [
            "",
            "## Risks",
            "",
        ]
    )

    for risk in final_report["risks"]:
        lines.append(f"- {risk}")

    lines.extend(
        [
            "",
            "## Recommendations",
            "",
        ]
    )

    for recommendation in final_report[
        "recommendations"
    ]:
        lines.append(f"- {recommendation}")

    lines.extend(
        [
            "",
            "## Limitations",
            "",
        ]
    )

    for limitation in final_report[
        "limitations"
    ]:
        lines.append(f"- {limitation}")

    lines.extend(
        [
            "",
            "## Citations",
            "",
        ]
    )

    for citation in final_report[
        "citations"
    ]:
        lines.append(f"- {citation}")

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    return str(output_path)


def main():

    print("=" * 60)
    print("AI Research & Report Generation System")
    print("=" * 60)

    research_topic = input(
        "\nEnter research topic: "
    ).strip()

    if not research_topic:
        print(
            "\nError: Research topic cannot be empty."
        )
        return

    urls = []

    print(
        "\nEnter public web source URLs."
    )
    print(
        "Enter one URL per line."
    )
    print(
        "Press Enter on an empty line when finished."
    )

    while True:
        url = input("> ").strip()

        if not url:
            break

        urls.append(url)

    try:
        llm = create_llm()

        pipeline = ResearchPipeline(
            llm=llm
        )

        result = pipeline.run(
            session_id="default",
            research_topic=research_topic,
            urls=urls,
            pdf_directory="data/pdfs",
        )

        report_path = save_report(
            result
        )

        print(
            "\nResearch completed successfully."
        )

        print(
            f"Sources processed: "
            f"{result['source_count']}"
        )

        if result["source_failures"]:
            print("\nSource failures:")

            for failure in result[
                "source_failures"
            ]:
                print(f"- {failure}")

        print(
            f"\nReport saved to: {report_path}"
        )

        print("\nResearch report:")
        print("-" * 60)

        final_report = result[
            "final_report"
        ]

        print(
            final_report[
                "executive_summary"
            ]
        )

        print("\nCitations:")

        for citation in final_report[
            "citations"
        ]:
            print(f"- {citation}")

    except Exception as exc:
        print(
            "\nResearch workflow failed."
        )
        print(
            f"Reason: {exc}"
        )


if __name__ == "__main__":
    main()