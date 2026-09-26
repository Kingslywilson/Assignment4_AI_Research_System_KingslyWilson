from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet


output_folder = Path("data/pdfs")
output_folder.mkdir(parents=True, exist_ok=True)

pdf_path = output_folder / "multi_page_climate_report.pdf"

document = SimpleDocTemplate(
    str(pdf_path),
    pagesize=A4,
    rightMargin=50,
    leftMargin=50,
    topMargin=50,
    bottomMargin=50,
)

styles = getSampleStyleSheet()

story = [
    Paragraph("Climate Change Report - Page One", styles["Title"]),
    Paragraph(
        "Page one discusses extreme heat, heat exhaustion, heatstroke, "
        "cardiovascular problems, and vulnerable populations.",
        styles["BodyText"],
    ),
    PageBreak(),
    Paragraph("Climate Change Report - Page Two", styles["Title"]),
    Paragraph(
        "Page two discusses infectious diseases, food and water security, "
        "mental health, climate-resilient health systems, and evidence gaps.",
        styles["BodyText"],
    ),
]

document.build(story)

print(f"Created: {pdf_path.resolve()}")