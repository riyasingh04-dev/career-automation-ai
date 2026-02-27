import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def test_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    textobject = c.beginText()
    textobject.setTextOrigin(50, height - 50)
    textobject.setFont("Helvetica", 10)
    textobject.textLine("Test line of text")
    c.drawText(textobject)
    c.showPage()
    c.save()
    print("PDF generation successful")

if __name__ == "__main__":
    try:
        test_pdf()
    except Exception as e:
        print(f"PDF generation failed: {e}")
