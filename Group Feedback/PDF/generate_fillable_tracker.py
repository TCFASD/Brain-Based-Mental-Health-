"""Generate a fillable PDF version of the Feedback Task Tracker."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfform

PAGE_W, PAGE_H = letter
MARGIN = 0.6 * inch

# Colors
GREEN_BG = "#5b7a6a"
HEADER_BG = "#f0eeea"
HEADER_TEXT = "#3a5a4a"
BORDER = "#d4d0c8"

# Table layout
COL_WIDTHS = [2.2 * inch, 1.8 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch]
TABLE_W = sum(COL_WIDTHS)
ROW_H = 28
HEADER_ROW_H = 32
SECTION_H = 30

STATUS_OPTIONS = ["--", "Sent", "In Progress", "Received", "Finalized"]

WEBSITE_ROWS = [
    "Home Page Feedback",
    "Overall Layout Feedback",
    "About Us Page Feedback",
    "Professionals Page Feedback",
]

THERAPY_ROWS = [
    "CBT Feedback",
    "TF-CBT Feedback",
    "DBT Feedback",
    "Play Therapy Feedback",
    "EMDR Feedback",
    "Somatic Experiencing Feedback",
    "Theraplay Feedback",
    "DDP Feedback",
    "TBRI Feedback",
    "CPS Feedback",
    "Parent Training Programs Feedback",
]


def draw_section_header(c, x, y, text):
    c.setFillColor(HexColor(GREEN_BG))
    c.roundRect(x, y - SECTION_H + 6, TABLE_W, SECTION_H, 4, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Times-Bold", 13)
    c.drawString(x + 10, y - 16, text)
    return y - SECTION_H


def draw_table_header(c, x, y):
    headers = ["Review Document", "Person(s) Assigned", "Date Due", "Date Received", "Status"]
    c.setFillColor(HexColor(HEADER_BG))
    c.rect(x, y - HEADER_ROW_H + 4, TABLE_W, HEADER_ROW_H, fill=1, stroke=0)
    c.setStrokeColor(HexColor(BORDER))
    c.rect(x, y - HEADER_ROW_H + 4, TABLE_W, HEADER_ROW_H, fill=0, stroke=1)

    cx = x
    c.setFont("Times-Bold", 9)
    c.setFillColor(HexColor(HEADER_TEXT))
    for i, h in enumerate(headers):
        c.drawString(cx + 6, y - 18, h.upper())
        if i < len(headers) - 1:
            cx += COL_WIDTHS[i]
            c.line(cx, y + 4, cx, y - HEADER_ROW_H + 4)
    return y - HEADER_ROW_H


def draw_data_row(c, x, y, label, row_idx, section_prefix):
    """Draw one data row with fillable fields."""
    c.setStrokeColor(HexColor(BORDER))

    # Alternating row background
    if row_idx % 2 == 1:
        c.setFillColor(HexColor("#faf9f7"))
        c.rect(x, y - ROW_H + 4, TABLE_W, ROW_H, fill=1, stroke=0)

    # Row border
    c.rect(x, y - ROW_H + 4, TABLE_W, ROW_H, fill=0, stroke=1)

    # Column dividers
    cx = x
    for i in range(len(COL_WIDTHS) - 1):
        cx += COL_WIDTHS[i]
        c.line(cx, y + 4, cx, y - ROW_H + 4)

    # Document name (static text)
    c.setFillColor(black)
    c.setFont("Times-Bold", 10)
    c.drawString(x + 6, y - 15, label)

    # Field name prefix
    fn = f"{section_prefix}_{row_idx}"
    cx = x + COL_WIDTHS[0]

    # Assigned (text field)
    form = c.acroForm
    field_y = y - ROW_H + 8
    field_h = ROW_H - 10

    form.textfield(
        name=f"{fn}_assigned",
        x=cx + 4, y=field_y,
        width=COL_WIDTHS[1] - 8, height=field_h,
        borderWidth=0,
        fillColor=Color(0, 0, 0, 0),
        textColor=black,
        fontSize=10,
        fontName="Times-Roman",
    )
    cx += COL_WIDTHS[1]

    # Date Due (text field)
    form.textfield(
        name=f"{fn}_due",
        x=cx + 4, y=field_y,
        width=COL_WIDTHS[2] - 8, height=field_h,
        borderWidth=0,
        fillColor=Color(0, 0, 0, 0),
        textColor=black,
        fontSize=9,
        fontName="Times-Roman",
    )
    cx += COL_WIDTHS[2]

    # Date Received (text field)
    form.textfield(
        name=f"{fn}_received",
        x=cx + 4, y=field_y,
        width=COL_WIDTHS[3] - 8, height=field_h,
        borderWidth=0,
        fillColor=Color(0, 0, 0, 0),
        textColor=black,
        fontSize=9,
        fontName="Times-Roman",
    )
    cx += COL_WIDTHS[3]

    # Status (dropdown)
    form.choice(
        name=f"{fn}_status",
        options=STATUS_OPTIONS,
        value="--",
        x=cx + 4, y=field_y,
        width=COL_WIDTHS[4] - 8, height=field_h,
        borderWidth=1,
        borderColor=HexColor(BORDER),
        fillColor=white,
        textColor=black,
        fontSize=9,
        fontName="Times-Roman",
    )

    return y - ROW_H


def main():
    out_path = r"C:\Users\Tamra\Documents\Brain-Based Mental Health Website\Group Feedback\PDF\Feedback-Task-Tracker.pdf"
    c = canvas.Canvas(out_path, pagesize=letter)

    # Title
    y = PAGE_H - MARGIN
    c.setFont("Times-Bold", 18)
    c.setFillColor(black)
    title = "Brain-Based Mental Health Community"
    c.drawCentredString(PAGE_W / 2, y - 10, title)

    c.setFont("Times-Roman", 12)
    c.setFillColor(HexColor("#555555"))
    c.drawCentredString(PAGE_W / 2, y - 28, "Feedback Task Tracker")

    # Divider
    y -= 42
    c.setStrokeColor(HexColor(GREEN_BG))
    c.setLineWidth(2)
    c.line(MARGIN, y, PAGE_W - MARGIN, y)
    c.setLineWidth(1)
    y -= 16

    x = MARGIN

    # Website Page Feedback section
    y = draw_section_header(c, x, y, "Website Page Feedback")
    y = draw_table_header(c, x, y)
    for i, label in enumerate(WEBSITE_ROWS):
        y = draw_data_row(c, x, y, label, i, "web")

    y -= 20

    # Therapy Modality Feedback section
    y = draw_section_header(c, x, y, "Therapy Modality Feedback - Caregiver's Guide")
    y = draw_table_header(c, x, y)
    for i, label in enumerate(THERAPY_ROWS):
        y = draw_data_row(c, x, y, label, i, "therapy")

    # Footer
    y -= 20
    c.setStrokeColor(HexColor(GREEN_BG))
    c.setLineWidth(2)
    c.line(MARGIN, y, PAGE_W - MARGIN, y)
    c.setFont("Times-Roman", 10)
    c.setFillColor(HexColor("#777777"))
    c.drawCentredString(PAGE_W / 2, y - 16, "Brain-Based Mental Health Community - Feedback Task Tracker")

    c.save()
    print(f"Fillable PDF saved to: {out_path}")


if __name__ == "__main__":
    main()
