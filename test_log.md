Test Log — AI Research & Report Generation System
1. Testing Overview

The AI Research & Report Generation System was tested using Python, LangChain, Groq, local PDF documents, and public web sources.

Testing covered:

Input validation
Web source loading
PDF source loading
Source failure handling
Document preprocessing
Duplicate removal
Empty-content removal
Repeated header removal
Session memory
Session isolation
Session reset
Multi-stage research workflow
Structured LangChain chain construction
Source grounding
Insufficient evidence handling
Conflict handling
Token usage monitoring
LangSmith tracing
Markdown report generation
PDF page-level citation metadata
Follow-up source grounding
Ambiguity clarification
2. Input Validation Tests
Test Case 1 — Empty Research Topic
Input

An empty research topic was submitted.

Expected Result

The system should reject the empty topic and should not start the research workflow.

Actual Result
Error: Research topic cannot be empty.

Status: PASS

Test Case 2 — Whitespace-Only Research Topic
Input

A research topic containing only whitespace was submitted.

Expected Result

Whitespace-only input should be rejected.

Actual Result
Error: Research topic cannot be empty.

Status: PASS

3. Web Source Tests
Test Case 3 — Successful Web Research
Research Topic

What are the health impacts of climate change?

Sources
https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health
https://science.nasa.gov/climate-change/
Expected Result

The system should load valid public web pages and generate a research report.

Actual Result
Research completed successfully.
Sources processed: 3
Report saved to: outputs/research_report.md

The three processed sources included the two web sources and the available PDF source.

Status: PASS

Test Case 4 — Failed Web Source With Valid Sources
Sources
https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health
https://this-domain-does-not-exist-123456789.com/test
https://science.nasa.gov/climate-change/
Expected Result

A failed source should be reported while valid sources continue through the workflow.

Actual Result
Research completed successfully.
Sources processed: 2

The invalid URL was reported under source failures, while the valid WHO and NASA sources were processed successfully.

Status: PASS

Test Case 5 — All Sources Unavailable
Input

A valid research topic was supplied with an invalid web URL and no available PDF source.

Expected Result

The system should stop gracefully without attempting the research stages.

Actual Result
Research workflow failed.
Reason: No usable research sources are available.

Status: PASS

4. PDF Loading Tests
Test Case 6 — PDF Loading Using PyPDFLoader
PDF

climate_change_health.pdf

Expected Result

The PDF should be loaded successfully using the configured PDF loader.

Actual Result
Research completed successfully.
Sources processed: 1

Status: PASS

Test Case 7 — PDF Metadata and Page Citation
Expected Result

PDF citations should preserve the filename and page number.

Actual Result
Source 1 — climate_change_health.pdf — Page 1

Status: PASS

Test Case 8 — Multi-Page PDF Metadata
PDF

multi_page_climate_report.pdf

The PDF contained two pages.

Expected Result

Each PDF page should retain its page-level metadata.

Actual Result
Source 3 — multi_page_climate_report.pdf — Page 1
Source 4 — multi_page_climate_report.pdf — Page 2

Status: PASS

5. Preprocessing Tests
Test Case 9 — Whitespace Normalization
Input

Text containing:

Leading spaces
Trailing spaces
Multiple spaces
Multiple blank lines
Expected Result

Excessive whitespace should be normalized.

Actual Result
'Climate change health\n\n Research report'

Status: PASS

Test Case 10 — Duplicate Document Removal
Input

Three documents were supplied:

Document A: Climate change affects health.
Document B: Climate change affects health.
Document C: Different research finding.
Expected Result

The duplicate document should be removed while the first document's metadata is retained.

Actual Result
Documents before: 3
Documents after: 2
Sources: ['A', 'C']

Status: PASS

Test Case 11 — Empty Content Removal
Input

Three documents were supplied:

Empty document
Whitespace-only document
Valid research document
Expected Result

Empty and whitespace-only documents should be removed.

Actual Result
Documents before: 3
Documents after: 1
Sources: ['valid']

Status: PASS

Test Case 12 — Repeated Header Removal
Input

Three documents contained the repeated header:

RESEARCH REPORT
Expected Result

The repeated header should be removed while meaningful content remains.

Actual Result
'Climate change affects health.\nPage 1'
'Climate change affects communities.\nPage 2'
'Climate change affects food security.\nPage 3'

Status: PASS

6. Conversational Memory Tests
Test Case 13 — Session Isolation
Input

Two independent sessions were created.

Session 1

Climate change
Climate report

Session 2

Artificial intelligence
Expected Result

Each session should contain only its own messages.

Actual Result
Session 1 count: 2
Session 2 count: 1

Status: PASS

Test Case 14 — Session Reset
Expected Result

Clearing a session should remove its stored messages and session state.

Actual Result
Before reset:
[{'role': 'user', 'content': 'Climate change'},
 {'role': 'assistant', 'content': 'Research result'}]

Session exists immediately after reset: False

Internal session data: {}

Status: PASS

7. Research Pipeline Tests
Test Case 15 — Six-Stage Research Workflow

The research pipeline was executed successfully using a PDF source.

Stages Tested
Topic Analysis
Research Summarization
Key Insight Extraction
Risk Identification
Recommendation Generation
Final Report Generation
Actual Result
Research completed successfully.
Sources processed: 1
Report saved to: outputs/research_report.md

Status: PASS

Test Case 16 — LangChain Chain Construction

All six chains were constructed successfully.

Actual Result
<class 'langchain_core.runnables.base.RunnableSequence'>
<class 'langchain_core.runnables.base.RunnableSequence'>
<class 'langchain_core.runnables.base.RunnableSequence'>
<class 'langchain_core.runnables.base.RunnableSequence'>
<class 'langchain_core.runnables.base.RunnableSequence'>
<class 'langchain_core.runnables.base.RunnableSequence'>

Status: PASS

8. Source Grounding Tests
Test Case 17 — Answer Grounded in Supplied PDF
Research Topic

What does the document say about climate change and mental health?

Expected Result

The answer should use information from the supplied document.

Actual Result

The generated report discussed:

Extreme weather
Displacement
Loss of homes
Community disruption
Stress
Anxiety
Psychological difficulties
Evidence gaps
Citation
Source 1 — climate_change_health.pdf — Page 1

Status: PASS

9. Insufficient Evidence Test
Test Case 18 — Unsupported Exact Economic Figure
Research Topic

What is the exact cost of climate change to the global economy in 2030?

Expected Result

The system should not invent an exact figure when the supplied source does not contain sufficient evidence.

Actual Result

The report explicitly stated that the supplied source did not provide a monetary valuation or global GDP-loss estimate and that the exact cost remained undefined.

Status: PASS

10. Conflict Handling Test
Test Case 19 — Conflicting Sources
Sources
climate_change_health.pdf
conflicting_climate_report.pdf

The documents contained different assessments of heat-related health risks by 2030.

Expected Result

The system should identify the disagreement rather than silently selecting one source.

Actual Result

The generated report explicitly identified the disagreement:

Two recent assessments offer conflicting conclusions about the trajectory
of heat-related health risks by 2030.

The report separately described both sources and preserved their citations:

Source 1 — climate_change_health.pdf — Page 1
Source 2 — conflicting_climate_report.pdf — Page 1

Status: PASS

11. Monitoring and Token Tracking
Test Case 20 — Per-Stage Token Usage

The monitoring callback was tested during a complete research pipeline execution.

Actual Result
Stage	Calls	Input Tokens	Output Tokens	Total Tokens
Topic Analysis	1	773	656	1,429
Summarization	1	1,170	1,046	2,216
Insight Extraction	1	1,515	1,240	2,755
Risk Analysis	1	2,262	874	3,136
Recommendation	1	2,916	1,136	4,052
Report Generation	1	4,081	2,043	6,124

Each stage recorded one LLM call and token usage.

Status: PASS

12. LangSmith Tracing
Test Case 21 — LangSmith Trace Verification

The configured LangSmith project was checked after running the research pipeline.

Project
Assignment4-AI-Research-System
Observed
Trace Count: 93
Error Rate: 3%
P50 Latency: 6.92s
P99 Latency: 53.25s

The project contained recorded traces from the application workflow.

Status: PASS

13. Final Report Generation
Test Case 22 — Markdown Report Generation
Expected Result

The system should save the final research report to:

outputs/research_report.md
Actual Result
Report saved to: outputs/research_report.md

The generated Markdown report contained:

Executive Summary
Findings
Key Insights
Risks
Recommendations
Limitations
Citations

Status: PASS

14. Citation Verification
Test Case 23 — Source Citation Traceability
Web Source Example
Source 1 — Climate change — https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health
PDF Source Example
Source 1 — climate_change_health.pdf — Page 1
Multi-Page PDF Example
Source 3 — multi_page_climate_report.pdf — Page 1
Source 4 — multi_page_climate_report.pdf — Page 2

Status: PASS

15. Follow-Up and Ambiguity Tests
Test Case 24 — Follow-Up Question With Source Grounding
Input

Initial research topic:

What are the health impacts of climate change?

Follow-up question:

What does the source say specifically about mental health?

Expected Result

The follow-up interaction should use the existing research session and remain grounded in the supplied sources.

Actual Result

The response used information from the supplied climate-change document and referenced the corresponding source citation.

Status: PASS

Test Case 25 — Ambiguous Research Question
Input

A deliberately ambiguous research question was submitted.

Expected Result

The system should request clarification instead of making unsupported assumptions.

Actual Result

The system requested clarification before proceeding.

Status: PASS

16. Test Summary
Category	Result
Input validation	PASS
Web loading	PASS
Source failure handling	PASS
PDF loading	PASS
PDF metadata	PASS
Multi-page PDF metadata	PASS
Whitespace preprocessing	PASS
Duplicate removal	PASS
Empty-content removal	PASS
Header removal	PASS
Session memory	PASS
Session isolation	PASS
Session reset	PASS
Six-stage workflow	PASS
LangChain chain construction	PASS
Source grounding	PASS
Insufficient evidence handling	PASS
Conflict handling	PASS
Token monitoring	PASS
LangSmith tracing	PASS
Report generation	PASS
Citation traceability	PASS
Follow-up source grounding	PASS
Ambiguity clarification	PASS
17. Known Observations

During testing, the Groq API initially returned a request-size error when multiple large web sources were supplied.

Error
413 - Request too large
TPM Limit: 8000
Requested: 8096

To reduce the request size, the source-material character limit was reduced from 9000 characters to 6000 characters in the preprocessing stage.

After this adjustment, the multi-source research workflow completed successfully.

The final report also showed some character-encoding/display artifacts when viewed through PowerShell, such as:

â€‘
â€™
â€”

The application writes the Markdown file using UTF-8 encoding.

18. Final Testing Conclusion

The implemented AI Research & Report Generation System was tested across its major functional requirements.

The tests verified:

Input validation
Web and PDF data collection
Source failure handling
Document preprocessing
Metadata preservation
Multi-stage LangChain research workflow
Source-grounded research
Insufficient-evidence handling
Conflict identification
Session-based memory
Session isolation and reset
Follow-up source grounding
Ambiguity clarification
Token usage monitoring
LangSmith tracing
Report generation
Citation traceability

Overall Testing Status: PASS

This version preserves the test results from your uploaded log while cleaning the Markdown formatting and organizing the test cases into a submission-ready structure.