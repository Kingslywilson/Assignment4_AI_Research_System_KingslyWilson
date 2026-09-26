import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from research_pipeline import ResearchPipeline, format_report_markdown


load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


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

    report_text = format_report_markdown(report)

    output_path.write_text(
        report_text,
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

        session_id = "default"

        result = pipeline.run(
            session_id=session_id,
            research_topic=research_topic,
            urls=urls,
            pdf_directory="data/pdfs",
            article_directory="data/articles",
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
        print(format_report_markdown(result))

        print("\n" + "=" * 60)
        print("Interactive Follow-Up Session")
        print("Enter your follow-up questions below. Type 'exit' or 'quit' to end.")
        print("=" * 60)

        while True:
            try:
                followup_input = input("\nFollow-up question > ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not followup_input or followup_input.lower() in ["exit", "quit"]:
                print("Ending research session. Goodbye!")
                break

            followup_result = pipeline.answer_followup(
                session_id=session_id,
                question=followup_input
            )

            if followup_result.get("is_ambiguous"):
                print(f"\n{followup_result['clarification_message']}")
                for idx, opt in enumerate(followup_result.get("clarification_options", []), 1):
                    if opt.strip().startswith(str(idx)):
                        print(opt)
                    else:
                        print(f"{idx}. {opt}")
            else:
                print(f"\nAnswer:\n{followup_result['answer']}")
                if followup_result.get("citations"):
                    print("\nCitations:")
                    for citation in followup_result["citations"]:
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