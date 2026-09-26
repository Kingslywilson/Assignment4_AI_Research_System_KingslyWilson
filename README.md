# AI Research & Report Generation System

## 1. Project Overview

The AI Research & Report Generation System is a LangChain-based research application that collects information from public web sources and PDF documents, processes the collected content, analyzes the research topic, extracts insights, identifies risks, generates recommendations, and produces a structured research report.

The system uses Groq as the LLM provider and LangSmith for tracing and monitoring.

The research workflow is divided into multiple stages so that each stage has a dedicated prompt and structured output.

---

## 2. Objectives

The main objectives of the system are to:

- Accept a research topic from the user.
- Validate the research topic.
- Collect information from public web sources.
- Load research information from PDF documents.
- Preserve source metadata.
- Clean and preprocess collected documents.
- Remove duplicate and empty content.
- Remove repeated headers and formatting noise.
- Analyze the research topic.
- Generate a grounded research summary.
- Extract key insights.
- Identify research risks and uncertainties.
- Generate evidence-based recommendations.
- Generate a structured final research report.
- Preserve source citations.
- Handle conflicting sources explicitly.
- Avoid fabricating unsupported information.
- Maintain conversational session memory.
- Isolate different user sessions.
- Support session reset.
- Track LLM token usage.
- Support LangSmith tracing.

---

## 3. Technology Stack

The application uses:

- Python
- LangChain
- LangChain Community
- LangChain Groq
- Groq
- LangSmith
- PyPDF
- BeautifulSoup
- python-dotenv
- Pydantic

### Main Components

| Component | Purpose |
|---|---|
| LangChain | Research workflow orchestration |
| Groq | Large language model provider |
| WebBaseLoader | Public web page loading |
| PyPDFLoader | PDF document loading |
| Pydantic | Structured output validation |
| LangSmith | LLM tracing and monitoring |
| BeautifulSoup | Web content processing |
| python-dotenv | Environment variable configuration |

---

## 4. Project Structure

```text
Assignment4_AI_Research_System_YourName/
│
├── app.py
├── data_loader.py
├── preprocess.py
├── research_pipeline.py
├── memory.py
├── monitoring.py
│
├── chains/
│   ├── __init__.py
│   ├── topic_analysis.py
│   ├── summarization.py
│   ├── insight_extraction.py
│   ├── risk_analysis.py
│   ├── recommendation.py
│   └── report_generation.py
│
├── prompts/
│   ├── topic_analysis_prompt.txt
│   ├── summarization_prompt.txt
│   ├── insight_extraction_prompt.txt
│   ├── risk_analysis_prompt.txt
│   ├── recommendation_prompt.txt
│   └── report_generation_prompt.txt
│
├── data/
│   ├── pdfs/
│   └── articles/
│
├── outputs/
│   └── research_report.md
│
├── web_sources.txt
├── research_strategy.md
├── test_log.md
├── README.md
├── requirements.txt
└── .env.example

5. Environment Configuration

Create a .env file in the project root.

Example:

GROQ_API_KEY=your_groq_api_key_here

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=Assignment4-AI-Research-System

USER_AGENT=AI-Research-System/1.0

Do not commit the .env file or API keys to the project repository.

The provided .env.example file contains placeholder values for configuration.

6. Installation

Create and activate a Python virtual environment.

Windows PowerShell
python -m venv venv

Activate the environment:

.\venv\Scripts\Activate.ps1

Install the required dependencies:

pip install -r requirements.txt
7. Data Sources

The system supports:

Public Web Sources

Public web pages can be provided as URLs.

Example sources used during testing:

https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health
https://www.un.org/en/climatechange/science/climate-issues
https://science.nasa.gov/climate-change/

Additional public sources can be placed in:

web_sources.txt
PDF Documents

PDF files can be placed in:

data/pdfs/

The application uses PyPDFLoader to extract PDF content.

PDF metadata includes:

Filename
Source
Page number
8. Running the Application

From the project root:

python app.py

The application displays:

============================================================
AI Research & Report Generation System
============================================================

Enter research topic:

Enter a research topic, for example:

What are the health impacts of climate change?

The application then asks for public web source URLs.

Enter one URL per line and press Enter on an empty line when finished.

Example:

> https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health
> https://science.nasa.gov/climate-change/
>

The application processes the available web and PDF sources and generates the research report.

9. Research Workflow

The system follows a multi-stage research workflow:

Research Topic
      |
      v
Data Collection
      |
      v
Preprocessing
      |
      v
Topic Analysis
      |
      v
Research Summarization
      |
      v
Key Insight Extraction
      |
      v
Risk Identification
      |
      v
Recommendation Generation
      |
      v
Final Report Generation
      |
      v
Citations

Each major research stage uses a dedicated prompt and structured output model.

10. Research Stages
Stage 1 — Topic Analysis

The topic analysis stage identifies:

Main research question
Research scope
Key areas to investigate
Evidence requirements

It does not generate unsupported recommendations.

Stage 2 — Research Summarization

The summarization stage creates a grounded summary of the collected source material.

It preserves:

Major findings
Important evidence
Evidence gaps
Differences between sources
Stage 3 — Key Insight Extraction

This stage identifies meaningful patterns and insights supported by the collected sources.

Insights must remain grounded in the supplied research material.

Stage 4 — Risk Identification

The system identifies:

Research risks
Uncertainties
Evidence limitations
Areas where available evidence is insufficient

Unsupported risks should not be fabricated.

Stage 5 — Recommendation Generation

Recommendations are generated from the available evidence, findings, insights, and identified risks.

Recommendations are separated from direct source facts.

Stage 6 — Final Report Generation

The final stage combines the outputs from previous stages into a structured research report.

The final report contains:

Title
Executive Summary
Findings
Key Insights
Risks
Recommendations
Limitations
Citations
11. Prompt Management

Each major research stage has its own prompt file.

prompts/
├── topic_analysis_prompt.txt
├── summarization_prompt.txt
├── insight_extraction_prompt.txt
├── risk_analysis_prompt.txt
├── recommendation_prompt.txt
└── report_generation_prompt.txt

Separating prompts from application code makes the research workflow easier to maintain and modify.

12. Source Metadata

Source metadata is preserved throughout the research workflow.

Web Sources

Web source metadata includes:

Source type
URL
Page title
Source name

Example:

Source 1 — Climate change — https://example.com/article
PDF Sources

PDF metadata includes:

Source type
Filename
Source
Page number

Example:

Source 1 — climate_change_health.pdf — Page 1

This metadata is used to generate traceable citations in the final report.

13. Document Preprocessing

The preprocessing stage performs several cleaning operations.

Whitespace Normalization

The system removes excessive spaces and blank lines.

Empty Content Removal

Empty and whitespace-only documents are skipped.

Duplicate Removal

Duplicate document content is removed while preserving the first document's metadata.

Repeated Header/Footer Removal

Repeated first and last lines across documents are detected and removed when they occur repeatedly.

The preprocessing stage helps reduce unnecessary content before sending source material to the LLM.

14. Source Grounding

The system is designed to keep research outputs grounded in the supplied sources.

The research prompts instruct the LLM to:

Use supplied source material.
Avoid unsupported claims.
Preserve evidence gaps.
Distinguish source facts from synthesized findings.
Identify uncertainty.
Provide source citations.

The final report citations are also constructed from the document metadata in the research pipeline.

15. Insufficient Evidence Handling

The system should not invent information when the supplied sources do not contain sufficient evidence.

For example, if a source does not provide an exact economic value, the system should state that the requested figure is not available in the supplied evidence rather than creating a numerical estimate.

Testing verified this behavior using a question about the exact global economic cost of climate change in 2030.

16. Conflict Handling

When different sources provide conflicting information, the system is instructed not to silently select one source.

Instead, the report should:

Identify the disagreement.
Describe the relevant positions from the sources.
Preserve the citations for the sources involved.
Avoid presenting an unsupported resolution.

This behavior was tested using two PDF documents containing different assessments of heat-related health risks.

17. Conversational Memory

The system contains a session-based memory implementation.

The memory stores:

role
content

for each message.

Sessions are identified using a session ID.

This allows different sessions to maintain separate conversation histories.

The system also provides session reset functionality.

Testing verified:

Session creation
Message storage
Session isolation
Session reset
18. Monitoring and Token Tracking

The application includes a monitoring callback that tracks LLM usage by research stage.

Tracked values include:

Number of calls
Input tokens
Output tokens
Total tokens

Example stages tracked:

topic_analysis
summarization
insight_extraction
risk_analysis
recommendation
report_generation

This provides visibility into the token usage of each stage.

19. LangSmith Tracing

LangSmith tracing is configured through environment variables.

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=Assignment4-AI-Research-System

Credentials are not hardcoded in the application.

During testing, the configured LangSmith project recorded application traces.

20. Failure Handling

The system handles several source-related failure conditions.

Invalid Source

If one web source fails, other valid sources can continue through the workflow.

Empty Source

Empty documents are skipped during preprocessing.

No Usable Sources

If no usable sources remain, the research workflow stops with an informative error:

No usable research sources are available.
Invalid Research Topic

Empty or whitespace-only research topics are rejected before the research workflow begins.

21. Output

The generated research report is saved to:

outputs/research_report.md

The report contains:

# Report Title

## Executive Summary

## Findings

## Key Insights

## Risks

## Recommendations

## Limitations

## Citations
22. Testing

The system was tested against the major functional requirements.

Testing included:

Empty topic validation
Whitespace-only topic validation
Successful web research
Failed web source handling
Complete source failure handling
PDF loading
PDF metadata
Multi-page PDF metadata
Whitespace normalization
Duplicate removal
Empty-content removal
Repeated header removal
Session isolation
Session reset
Six-stage research workflow
LangChain chain construction
Source grounding
Insufficient evidence handling
Conflict handling
Per-stage token tracking
LangSmith tracing
Markdown report generation
Citation traceability
Follow-up source grounding
Ambiguity clarification

Detailed results are available in:

test_log.md
23. Research Strategy

The detailed research architecture and strategy are documented in:

research_strategy.md

The strategy document describes:

Data collection
Preprocessing
Metadata preservation
Research stages
Prompt separation
Grounding
Conflict handling
Insufficient evidence handling
Memory
Monitoring
Failure handling
24. Security and Configuration

The following information must not be committed to the project:

Groq API keys
LangSmith API keys
.env files
Personal credentials
Authentication tokens

Use .env.example as the configuration template.

The project .gitignore excludes .env, virtual environments, Python cache files, IDE configuration, and temporary files.

25. Groq Request Size Observation

During testing, a Groq request-size error occurred when multiple large source contents were supplied.

The observed error was:

413 - Request too large
TPM Limit: 8000
Requested: 8096

The source-material character limit was reduced from 9000 to 6000 characters.

After this adjustment, the multi-source workflow completed successfully.

This adjustment reduces the amount of source material included in each LLM request while maintaining the required research workflow.

26. Example Research Topic

Example:

What are the health impacts of climate change?

The system can combine public web sources and local PDF research documents to produce a structured report with findings, insights, risks, recommendations, limitations, and citations.
## 27. Submission Checklist

Before submission, verify that the project contains:

- [ ] app.py
- [ ] data_loader.py
- [ ] preprocess.py
- [ ] research_pipeline.py
- [ ] memory.py
- [ ] monitoring.py
- [ ] chains/
- [ ] prompts/
- [ ] data/
- [ ] outputs/
- [ ] web_sources.txt
- [ ] research_strategy.md
- [ ] test_log.md
- [ ] README.md
- [ ] requirements.txt
- [ ] .env.example

Do not include:

- [ ] .env
- [ ] API keys
- [ ] venv/
- [ ] .venv/
- [ ] __pycache__/
- [ ] IDE configuration
- [ ] temporary files
- [ ] unnecessary test scripts
- [ ] unrelated project files

## 28. Conclusion

The AI Research & Report Generation System provides a structured LangChain-based workflow for collecting, preprocessing, analyzing, and synthesizing research information from public web sources and PDF documents.

The system separates each research stage into dedicated chains and prompts, preserves source metadata, generates structured reports, identifies conflicting evidence, handles insufficient evidence, maintains session memory, tracks token usage, and supports LangSmith tracing.