from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

def generate_pdf(data):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=LETTER)
    styles = getSampleStyleSheet()
    elements = []

    # Section helper
    def add_section(title, items):
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>{title}</b>", styles['Heading2']))
        elements.append(Spacer(1, 6))
        if isinstance(items, list):
            if not items:
                elements.append(Paragraph("No data available.", styles['Normal']))
            for item in items:
                if isinstance(item, str):
                    elements.append(Paragraph(f"• {item}", styles['Normal']))
                elif isinstance(item, dict):
                    text = "<br/>".join([f"<b>{k.title()}:</b> {v}" for k, v in item.items()])
                    elements.append(Paragraph(text, styles['Normal']))
                    elements.append(Spacer(1, 6))
        elif isinstance(items, str):
            elements.append(Paragraph(items, styles['Normal']))

    # Inject data
    add_section("📌 Profile", data.get("description", "No description available"))
    add_section("🧰 Stack", data.get("stack", []))
    add_section("💼 Experience", data.get("experience", []))
    add_section("🎓 Education", data.get("education", []))

    doc.build(elements)
    return temp_file.name
