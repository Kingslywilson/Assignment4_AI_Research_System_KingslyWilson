# Research Strategy

## 1. Objective

The system accepts a research topic and generates a grounded research
report using publicly accessible web sources and PDF documents.

The system uses Retrieval-Augmented-style source grounding through
document collection, preprocessing, structured research stages, and
source-aware report generation.

---

## 2. Research Workflow

The workflow follows these stages:

1. Research Topic
2. Data Collection
3. Topic Analysis
4. Research Summarization
5. Key Insight Extraction
6. Risk Identification
7. Recommendation Generation
8. Final Report
9. Citations

Each major research stage uses a dedicated LangChain prompt and
structured output model.

---

## 3. Data Collection

### Web Sources

Publicly accessible web pages are loaded using LangChain
`WebBaseLoader`.

The system does not attempt to bypass:

- Authentication
- Paywalls
- CAPTCHA
- Bot protection
- Access restrictions

If a web source fails, the failure is recorded and other valid sources
continue through the workflow.

### PDF Sources

PDF documents are loaded using LangChain `PyPDFLoader`.

PDF metadata includes:

- File name
- Source
- Page number
- Source type

---

## 4. Preprocessing

Collected documents are cleaned before being passed to the research
stages.

The preprocessing process includes:

- Removing empty content
- Normalizing whitespace
- Cleaning broken line formatting
- Removing repeated headers
- Removing repeated footers
- Removing exact duplicate documents
- Preserving source metadata

The preprocessing stage is intentionally conservative so that meaningful
research content is not accidentally removed.

---

## 5. Source Metadata

Web sources preserve:

- URL
- Title
- Source name
- Source type

PDF sources preserve:

- File name
- Source
- Page number
- Source type

This metadata is included in the source text supplied to later research
stages.

---

## 6. Topic Analysis

The topic analysis stage identifies:

- Main research question
- Research scope
- Key research areas
- Evidence requirements

This stage does not generate recommendations.

---

## 7. Research Summarization

The summarization stage produces:

- Grounded research summary
- Major findings
- Evidence gaps

Conflicting source claims are not silently resolved.

When sources disagree, the disagreement is preserved for later reporting.

---

## 8. Key Insight Extraction

The insight stage identifies meaningful patterns and relationships from
the supplied evidence.

Every insight should be traceable to supporting research material.

Unsupported assumptions are not treated as facts.

---

## 9. Risk Identification

The risk stage identifies:

- Evidence-supported risks
- Supporting evidence
- Research uncertainties
- Evidence limitations

The system does not invent unsupported risks.

---

## 10. Recommendation Generation

Recommendations are generated only after reviewing:

- Research findings
- Key insights
- Identified risks
- Available evidence

Recommendations must be supported by the supplied research material.

Limitations are explicitly identified where evidence is incomplete.

---

## 11. Final Report

The final report contains:

- Title
- Executive summary
- Findings
- Key insights
- Risks
- Recommendations
- Limitations
- Citations

The report distinguishes between:

### Source Facts

Information directly supported by the collected sources.

### Synthesized Findings

Conclusions produced by combining information from multiple sources.

### Recommendations

Evidence-based actions generated from the findings and risk analysis.

---

## 12. Conflict Handling

If two or more sources provide conflicting information, the system does
not silently select one source.

Instead, the disagreement is identified and the relevant sources are
preserved in the report.

---

## 13. Insufficient Evidence

When the supplied sources do not contain enough information to answer a
research question, the system explicitly indicates that evidence is
insufficient.

The system must not fabricate facts to fill missing information.

---

## 14. Conversational Memory

The system maintains conversation history using a session identifier.

Each session has independent conversation history.

This prevents one research session from mixing its context with another
session.

Follow-up questions can therefore use the conversation history associated
with the same session.

---

## 15. Monitoring

LangSmith tracing is configured through environment variables.

The system also tracks available token usage information through a
LangChain callback handler.

No API credentials are hardcoded into the application.

---

## 16. Failure Handling

The system handles failures at multiple levels.

### Source Failure

If one web page or PDF fails to load, valid sources continue through
the workflow.

### Empty Source

Empty documents are removed during preprocessing.

### Stage Failure

An overall workflow exception is caught by the application and reported
without exposing application credentials.

### Insufficient Sources

If no usable research sources remain, the research workflow stops instead
of generating unsupported information.

---

## 17. Grounding Strategy

The system supplies the collected and preprocessed source material to
each research stage.

Prompts explicitly instruct the model to:

- Use only supplied evidence
- Avoid fabrication
- Preserve source disagreements
- Identify insufficient evidence
- Preserve citations

This provides traceability from research findings back to source material.