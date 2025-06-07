from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit

def save_insights_to_pdf(insight_text, filename="resume_insights.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    text_object = c.beginText(50, 750)  # Set the starting position
    text_object.setFont("Helvetica", 12)  # Set font for readability

    max_width = 450  # Maximum width for text wrapping
    min_y_position = 50  # Minimum Y-position before adding a new page
    y_position = 750  # Track current Y position dynamically

    lines = insight_text.strip().split("\n")

    for line in lines:
        wrapped_lines = simpleSplit(line, "Helvetica", 12, max_width)  # Wrap long text
        for wrapped_line in wrapped_lines:
            if y_position < min_y_position:  # If text reaches the bottom, create a new page
                c.drawText(text_object)  # Save current page
                c.showPage()  # Create a new page
                text_object = c.beginText(50, 750)  # Reset text position for new page
                text_object.setFont("Helvetica", 12)  # Reapply font settings
                y_position = 750  # Reset Y position

            text_object.setTextOrigin(50, y_position)  # Correctly position text
            text_object.textLine(wrapped_line)  # Add text to PDF
            y_position -= 20  # Move down for the next line

    c.drawText(text_object)  # Save the final page
    c.save()

def save_insights_to_txt(insight_text, filename="resume_insights.txt"):
    with open(filename, "w") as f:
        f.write(insight_text)

# Example Usage:
insight_text = """This is a long insight. If it overflows, it will automatically wrap and move to a new page while keeping proper alignment. Nothing will be lost from the output."""
save_insights_to_pdf(insight_text)