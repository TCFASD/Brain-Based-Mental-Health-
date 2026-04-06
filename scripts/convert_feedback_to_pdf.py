"""
Convert Group Feedback HTML forms to fillable PDFs using ReportLab.
Parses each HTML file and creates a matching PDF with AcroForm fields.
"""

import os
import re
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER

PAGE_W, PAGE_H = letter
MARGIN_L = 60
MARGIN_R = 60
MARGIN_T = 50
MARGIN_B = 50
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R
FIELD_COUNTER = 0

GREEN = HexColor('#5b7a6a')
DARK_GREEN = HexColor('#3a5a4a')
LIGHT_BG = HexColor('#f0eeea')
ACCENT_BG = HexColor('#eef4f0')
BLUE_LINK = HexColor('#2c5aa0')
GRAY = HexColor('#555555')
LIGHT_GRAY = HexColor('#cccccc')
DARK = HexColor('#2c2c2c')


def unique_name(prefix):
    global FIELD_COUNTER
    FIELD_COUNTER += 1
    return f"{prefix}_{FIELD_COUNTER}"


def new_page_if_needed(c, y, needed=80):
    if y < MARGIN_B + needed:
        c.showPage()
        c.setFont('Helvetica', 11)
        return PAGE_H - MARGIN_T
    return y


def draw_header(c, y, title, subtitle):
    # Green header bar
    bar_h = 60
    c.setFillColor(GREEN)
    c.roundRect(MARGIN_L, y - bar_h, CONTENT_W, bar_h, 6, fill=1, stroke=0)

    # Title text
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(PAGE_W / 2, y - 24, title)

    c.setFont('Helvetica', 11)
    c.setFillColor(HexColor('#d0e8dc'))
    c.drawCentredString(PAGE_W / 2, y - 44, subtitle)

    c.setFillColor(DARK)
    return y - bar_h - 20


def draw_name_date(c, y, form):
    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(GRAY)
    c.drawString(MARGIN_L, y + 4, 'NAME')
    form.textfield(
        name=unique_name('name'), x=MARGIN_L, y=y - 18,
        width=220, height=20, borderWidth=1,
        borderColor=LIGHT_GRAY, fontSize=11,
        fontName='Helvetica'
    )

    c.drawString(MARGIN_L + 280, y + 4, 'DATE')
    form.textfield(
        name=unique_name('date'), x=MARGIN_L + 280, y=y - 18,
        width=180, height=20, borderWidth=1,
        borderColor=LIGHT_GRAY, fontSize=11,
        fontName='Helvetica'
    )

    # Divider
    y = y - 35
    c.setStrokeColor(HexColor('#e0ddd6'))
    c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
    return y - 15


def draw_website_link(c, y, url):
    c.setFillColor(ACCENT_BG)
    c.setStrokeColor(GREEN)
    box_h = 36
    c.roundRect(MARGIN_L, y - box_h, CONTENT_W, box_h, 4, fill=1, stroke=1)

    c.setFillColor(DARK_GREEN)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(PAGE_W / 2, y - 14, 'Review the live website before providing feedback:')
    c.setFillColor(BLUE_LINK)
    c.setFont('Helvetica', 9)
    c.drawCentredString(PAGE_W / 2, y - 28, url)

    return y - box_h - 15


def draw_section_number(c, y, text):
    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(GREEN)
    c.drawString(MARGIN_L, y, text.upper())
    return y - 16


def draw_section_title(c, y, text):
    c.setFont('Helvetica-Bold', 14)
    c.setFillColor(DARK)
    c.drawString(MARGIN_L, y, text)
    return y - 16


def draw_section_intro(c, y, text):
    c.setFont('Helvetica', 10)
    c.setFillColor(GRAY)
    lines = wrap_text(text, 'Helvetica', 10, CONTENT_W)
    for line in lines:
        y = new_page_if_needed(c, y, 20)
        c.drawString(MARGIN_L, y, line)
        y -= 14
    return y - 4


def draw_question_label(c, y, text):
    y = new_page_if_needed(c, y, 60)
    c.setFont('Helvetica-Bold', 11)
    c.setFillColor(DARK)
    lines = wrap_text(text, 'Helvetica-Bold', 11, CONTENT_W)
    for line in lines:
        y = new_page_if_needed(c, y, 20)
        c.drawString(MARGIN_L, y, line)
        y -= 15
    return y - 2


def draw_textarea(c, y, form, rows=3):
    h = rows * 18
    y = new_page_if_needed(c, y, h + 10)
    form.textfield(
        name=unique_name('text'), x=MARGIN_L, y=y - h,
        width=CONTENT_W, height=h, borderWidth=1,
        borderColor=LIGHT_GRAY, fontSize=10,
        fontName='Helvetica', fieldFlags='multiline'
    )
    return y - h - 12


def draw_checkbox_row(c, y, form, options):
    y = new_page_if_needed(c, y, 25)
    x = MARGIN_L
    for opt in options:
        form.checkbox(
            name=unique_name('chk'), x=x, y=y - 2,
            size=13, borderColor=LIGHT_GRAY,
            checked=False
        )
        c.setFont('Helvetica', 10)
        c.setFillColor(GRAY)
        c.drawString(x + 17, y, opt.strip())
        text_w = c.stringWidth(opt.strip(), 'Helvetica', 10)
        x += text_w + 35
        if x > PAGE_W - MARGIN_R - 60:
            y -= 20
            x = MARGIN_L
            y = new_page_if_needed(c, y, 25)
    return y - 18


def draw_yes_no(c, y, form):
    y = new_page_if_needed(c, y, 25)
    x = MARGIN_L
    form.checkbox(
        name=unique_name('yes'), x=x, y=y - 2,
        size=13, borderColor=LIGHT_GRAY
    )
    c.setFont('Helvetica', 10)
    c.setFillColor(GRAY)
    c.drawString(x + 17, y, 'Yes')

    form.checkbox(
        name=unique_name('no'), x=x + 70, y=y - 2,
        size=13, borderColor=LIGHT_GRAY
    )
    c.drawString(x + 87, y, 'No')
    return y - 20


def draw_option_block(c, y, form, label, text, options):
    y = new_page_if_needed(c, y, 120)

    # Option background
    block_h = 14 * len(wrap_text(text, 'Helvetica', 10, CONTENT_W - 30)) + 60
    bg_y = y - block_h + 30

    # Green left bar
    c.setFillColor(GREEN)
    c.rect(MARGIN_L, bg_y, 3, block_h - 10, fill=1, stroke=0)
    c.setFillColor(LIGHT_BG)
    c.rect(MARGIN_L + 3, bg_y, CONTENT_W - 3, block_h - 10, fill=1, stroke=0)

    # Option label
    c.setFont('Helvetica-Bold', 11)
    c.setFillColor(DARK_GREEN)
    c.drawString(MARGIN_L + 12, y, label)
    y -= 16

    # Option text
    c.setFont('Helvetica', 10)
    c.setFillColor(HexColor('#444444'))
    lines = wrap_text(text, 'Helvetica', 10, CONTENT_W - 30)
    for line in lines:
        c.drawString(MARGIN_L + 12, y, line)
        y -= 14
    y -= 4

    # Preference checkboxes
    if options:
        y = draw_checkbox_row(c, y, form, options)

    # Comments
    c.setFont('Helvetica', 9)
    c.setFillColor(GRAY)
    c.drawString(MARGIN_L + 12, y + 2, 'Comments:')
    y -= 4
    form.textfield(
        name=unique_name('comment'), x=MARGIN_L + 12, y=y - 30,
        width=CONTENT_W - 24, height=30, borderWidth=1,
        borderColor=LIGHT_GRAY, fontSize=9,
        fontName='Helvetica', fieldFlags='multiline'
    )
    return y - 45


def draw_divider(c, y):
    y = new_page_if_needed(c, y, 10)
    c.setStrokeColor(HexColor('#e0ddd6'))
    c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
    return y - 15


def draw_modality_content(c, y, sections):
    """Draw the modality description content in a styled block."""
    for label, content in sections:
        y = new_page_if_needed(c, y, 80)

        # Field label
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(DARK_GREEN)
        c.drawString(MARGIN_L + 10, y, label)
        y -= 16

        # Content text
        c.setFont('Helvetica', 9)
        c.setFillColor(HexColor('#444444'))

        if isinstance(content, list):
            for item in content:
                lines = wrap_text(item, 'Helvetica', 9, CONTENT_W - 30)
                for line in lines:
                    y = new_page_if_needed(c, y, 16)
                    c.drawString(MARGIN_L + 10, y, line)
                    y -= 13
                y -= 2
        else:
            lines = wrap_text(content, 'Helvetica', 9, CONTENT_W - 20)
            for line in lines:
                y = new_page_if_needed(c, y, 16)
                c.drawString(MARGIN_L + 10, y, line)
                y -= 13
        y -= 8

    return y


def draw_brain_note(c, y, text):
    y = new_page_if_needed(c, y, 80)

    lines = wrap_text(text, 'Helvetica', 9, CONTENT_W - 30)
    box_h = len(lines) * 13 + 24

    y_start = y
    # Background
    c.setFillColor(ACCENT_BG)
    c.rect(MARGIN_L, y - box_h + 14, CONTENT_W, box_h, fill=1, stroke=0)
    # Left bar
    c.setFillColor(DARK_GREEN)
    c.rect(MARGIN_L, y - box_h + 14, 3, box_h, fill=1, stroke=0)

    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(DARK_GREEN)
    c.drawString(MARGIN_L + 12, y, 'Brain-Based Consideration')
    y -= 16

    c.setFont('Helvetica', 9)
    c.setFillColor(HexColor('#333333'))
    for line in lines:
        c.drawString(MARGIN_L + 12, y, line)
        y -= 13

    return y - 12


def draw_footer(c, y):
    y = new_page_if_needed(c, y, 40)
    c.setStrokeColor(GREEN)
    c.setLineWidth(2)
    c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
    y -= 18
    c.setFont('Helvetica', 11)
    c.setFillColor(HexColor('#777777'))
    c.drawCentredString(PAGE_W / 2, y, 'Thank you for your feedback!')
    return y


def wrap_text(text, font_name, font_size, max_width):
    """Simple word-wrap."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words = text.split()
    lines = []
    current = ''
    for word in words:
        test = current + (' ' if current else '') + word
        if stringWidth(test, font_name, font_size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else ['']


def parse_and_convert(html_path, pdf_path):
    global FIELD_COUNTER
    FIELD_COUNTER = 0

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    c = canvas.Canvas(pdf_path, pagesize=letter)
    form = c.acroForm
    y = PAGE_H - MARGIN_T

    # Extract header
    h1 = soup.find('h1')
    h2 = soup.find('h2')
    title = h1.get_text(strip=True) if h1 else 'Brain-Based Mental Health Community'
    subtitle = h2.get_text(strip=True) if h2 else ''

    y = draw_header(c, y, title, subtitle)
    y = draw_name_date(c, y, form)

    # Website link
    link_div = soup.find('a', href=lambda h: h and 'tcfasd.github.io' in h)
    if link_div:
        url = link_div['href']
        y = draw_website_link(c, y, url)

    # Detect form type by looking at content
    modality_content = soup.find('div', class_='modality-content')
    option_blocks = soup.find_all('div', class_='option-block')
    sections = soup.find_all('div', class_='section')
    question_blocks_all = soup.find_all('div', class_='question-block')

    if modality_content:
        # THERAPY MODALITY FEEDBACK FORM
        # Extract modality meta
        meta = modality_content.find('div', class_='modality-meta')
        if meta:
            c.setFont('Helvetica-Bold', 9)
            c.setFillColor(GREEN)
            c.drawString(MARGIN_L, y, meta.get_text(strip=True))
            y -= 18

        # Draw green left bar background start
        content_start_y = y

        # Extract field sections
        field_labels = modality_content.find_all('div', class_='field-label')
        content_sections = []
        for fl in field_labels:
            label_text = fl.get_text(strip=True)
            # Get content after this label until next label or brain-note
            content_parts = []
            sibling = fl.find_next_sibling()
            while sibling and 'field-label' not in (sibling.get('class') or []) and 'brain-note' not in (sibling.get('class') or []):
                if sibling.name == 'p':
                    content_parts.append(sibling.get_text(strip=True))
                elif sibling.name == 'ul':
                    for li in sibling.find_all('li'):
                        content_parts.append('  \u2022 ' + li.get_text(strip=True))
                sibling = sibling.find_next_sibling()
            content_sections.append((label_text, content_parts))

        # Draw left accent bar
        c.setFillColor(GREEN)
        c.rect(MARGIN_L, MARGIN_B, 3, y - MARGIN_B, fill=1, stroke=0)

        for label_text, parts in content_sections:
            y = new_page_if_needed(c, y, 60)
            c.setFont('Helvetica-Bold', 10)
            c.setFillColor(DARK_GREEN)
            c.drawString(MARGIN_L + 10, y, label_text)
            y -= 16

            c.setFont('Helvetica', 9)
            c.setFillColor(HexColor('#444444'))
            for part in parts:
                lines = wrap_text(part, 'Helvetica', 9, CONTENT_W - 20)
                for line in lines:
                    y = new_page_if_needed(c, y, 16)
                    c.drawString(MARGIN_L + 10, y, line)
                    y -= 13
                y -= 3
            y -= 5

        # Brain note
        brain_note = modality_content.find('div', class_='brain-note')
        if brain_note:
            note_text = brain_note.get_text(strip=True)
            # Remove "Brain-Based Consideration" prefix if present
            note_text = note_text.replace('Brain-Based Consideration', '', 1).strip()
            y = draw_brain_note(c, y, note_text)

        y = draw_divider(c, y)

        # Questions after content
        main_questions = []
        for qb in soup.find_all('div', class_='question-block'):
            # Only get questions outside the modality-content div
            if not qb.find_parent('div', class_='modality-content'):
                main_questions.append(qb)

        for qb in main_questions:
            label = qb.find('label')
            if not label:
                continue
            label_text = label.get_text(strip=True)

            yes_no = qb.find('div', class_='yes-no-row')
            textarea = qb.find('textarea')

            if 'accurate' in label_text.lower():
                y = draw_question_label(c, y, label_text)
                y = draw_yes_no(c, y, form)
                # "If no, please explain" textarea
                explain_label = qb.find_all('label')
                if len(explain_label) > 1:
                    y = draw_question_label(c, y, explain_label[1].get_text(strip=True))
                else:
                    y = draw_question_label(c, y, 'If no, please explain:')
                y = draw_textarea(c, y, form, rows=3)
            elif textarea:
                y = draw_question_label(c, y, label_text)
                y = draw_textarea(c, y, form, rows=3)

    elif option_blocks:
        # HOME PAGE STYLE with option blocks (ranking questions)
        for section in sections:
            sec_num = section.find('div', class_='section-number')
            sec_title = section.find('h3')
            sec_intro = section.find('p', class_='section-intro')

            if sec_num:
                y = draw_section_number(c, y, sec_num.get_text(strip=True))
            if sec_title:
                y = draw_section_title(c, y, sec_title.get_text(strip=True))
            if sec_intro:
                y = draw_section_intro(c, y, sec_intro.get_text(strip=True))

            # Option blocks within this section
            for ob in section.find_all('div', class_='option-block'):
                opt_label = ob.find('div', class_='option-label')
                opt_text = ob.find('div', class_='option-text')
                prefs = ob.find('div', class_='preference-row')

                pref_options = []
                if prefs:
                    for lab in prefs.find_all('label'):
                        pref_options.append(lab.get_text(strip=True))

                if opt_label and opt_text:
                    y = draw_option_block(
                        c, y, form,
                        opt_label.get_text(strip=True),
                        opt_text.get_text(strip=True),
                        pref_options
                    )

            # Other suggestion textareas
            for os_div in section.find_all('div', class_='other-suggestion'):
                os_label = os_div.find('label')
                if os_label:
                    y = draw_question_label(c, y, os_label.get_text(strip=True))
                    y = draw_textarea(c, y, form, rows=2)

            # Regular question blocks
            for qb in section.find_all('div', class_='question-block'):
                label = qb.find('label')
                if label:
                    y = draw_question_label(c, y, label.get_text(strip=True))
                    y = draw_textarea(c, y, form, rows=3)

            y = draw_divider(c, y)

    else:
        # GENERAL FEEDBACK FORM (About Us, Overall Layout, Professionals)
        for section in sections:
            sec_num = section.find('div', class_='section-number')
            sec_title = section.find('h3')
            sec_intro = section.find('p', class_='section-intro')

            if sec_num:
                y = draw_section_number(c, y, sec_num.get_text(strip=True))
            if sec_title:
                y = draw_section_title(c, y, sec_title.get_text(strip=True))
            if sec_intro:
                y = draw_section_intro(c, y, sec_intro.get_text(strip=True))

            # Question blocks
            for qb in section.find_all('div', class_='question-block'):
                label = qb.find('label')
                if label:
                    y = draw_question_label(c, y, label.get_text(strip=True))
                    y = draw_textarea(c, y, form, rows=3)

            # Step headers and their content (Professionals page)
            for sh in section.find_all('div', class_='step-header'):
                y = new_page_if_needed(c, y, 60)
                c.setFillColor(LIGHT_BG)
                c.rect(MARGIN_L, y - 4, CONTENT_W, 20, fill=1, stroke=0)
                c.setFillColor(GREEN)
                c.rect(MARGIN_L, y - 4, 3, 20, fill=1, stroke=0)
                c.setFont('Helvetica-Bold', 10)
                c.setFillColor(DARK_GREEN)
                c.drawString(MARGIN_L + 10, y, sh.get_text(strip=True))
                y -= 24

            # Topic lists
            for tl in section.find_all('ul', class_='topic-list'):
                for li in tl.find_all('li'):
                    y = new_page_if_needed(c, y, 16)
                    c.setFont('Helvetica', 9)
                    c.setFillColor(HexColor('#444444'))
                    text = '\u2022 ' + li.get_text(strip=True)
                    lines = wrap_text(text, 'Helvetica', 9, CONTENT_W - 20)
                    for line in lines:
                        c.drawString(MARGIN_L + 16, y, line)
                        y -= 13
                y -= 4

            # Context notes
            for ctx in section.find_all('div', class_='context'):
                y = new_page_if_needed(c, y, 20)
                c.setFont('Helvetica-Oblique', 9)
                c.setFillColor(GRAY)
                c.drawString(MARGIN_L + 10, y, ctx.get_text(strip=True))
                y -= 16

            y = draw_divider(c, y)

    draw_footer(c, y)
    c.save()


def convert_task_tracker(html_path, pdf_path):
    """Convert the Feedback Task Tracker HTML to a fillable PDF with dropdowns
    and JavaScript-driven color coding by status."""
    import pypdf

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    tmp_path = pdf_path + '.tmp'
    c = canvas.Canvas(tmp_path, pagesize=letter)
    form = c.acroForm
    y = PAGE_H - MARGIN_T

    # Header
    y = draw_header(c, y, 'Brain-Based Mental Health Community', 'Feedback Task Tracker')

    # Divider
    c.setStrokeColor(GREEN)
    c.setLineWidth(2)
    c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
    c.setLineWidth(1)
    y -= 16

    # Column layout for tracker table
    col_widths = [2.0 * inch, 1.5 * inch, 0.95 * inch, 0.95 * inch, 1.1 * inch]
    table_w = sum(col_widths)
    headers = ['Review Document', 'Person(s) Assigned', 'Date Due', 'Date Received', 'Status']
    row_h = 24
    header_h = 28
    status_options = ['--', 'Sent', 'In Progress', 'Received', 'Finalized']

    # Track all row prefixes for JS hookup
    row_prefixes = []

    # Find all section titles and tables
    section_titles = soup.find_all('div', class_='section-title')
    tables = soup.find_all('table')

    for sec_idx, (sec_title, table) in enumerate(zip(section_titles, tables)):
        y = new_page_if_needed(c, y, 80)

        # Section header bar
        sec_h = 26
        c.setFillColor(GREEN)
        c.roundRect(MARGIN_L, y - sec_h, table_w, sec_h, 4, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(MARGIN_L + 10, y - 17, sec_title.get_text(strip=True))
        y -= sec_h

        # Table header row
        c.setFillColor(LIGHT_BG)
        c.rect(MARGIN_L, y - header_h, table_w, header_h, fill=1, stroke=0)
        c.setStrokeColor(LIGHT_GRAY)
        c.rect(MARGIN_L, y - header_h, table_w, header_h, fill=0, stroke=1)

        cx = MARGIN_L
        c.setFont('Helvetica-Bold', 7.5)
        c.setFillColor(DARK_GREEN)
        for i, h in enumerate(headers):
            c.drawString(cx + 4, y - 16, h.upper())
            if i < len(headers) - 1:
                cx += col_widths[i]
                c.line(cx, y, cx, y - header_h)
        y -= header_h

        # Data rows
        rows = table.find_all('tr')[1:]  # skip header row
        for row_idx, tr in enumerate(rows):
            y = new_page_if_needed(c, y, row_h + 5)

            # Alternating background
            if row_idx % 2 == 1:
                c.setFillColor(HexColor('#faf9f7'))
                c.rect(MARGIN_L, y - row_h, table_w, row_h, fill=1, stroke=0)

            # Row border
            c.setStrokeColor(LIGHT_GRAY)
            c.rect(MARGIN_L, y - row_h, table_w, row_h, fill=0, stroke=1)

            # Column dividers
            cx = MARGIN_L
            for i in range(len(col_widths) - 1):
                cx += col_widths[i]
                c.line(cx, y, cx, y - row_h)

            # Document name (static text from first td)
            td = tr.find('td', class_='doc-name')
            doc_name = td.get_text(strip=True) if td else f'Row {row_idx}'
            c.setFillColor(black)
            c.setFont('Helvetica-Bold', 8.5)
            c.drawString(MARGIN_L + 4, y - 15, doc_name)

            # Use predictable field names (no counter) so JS can find them
            prefix = f"s{sec_idx}_r{row_idx}"
            row_prefixes.append(prefix)
            field_y = y - row_h + 4
            field_h = row_h - 8
            cx = MARGIN_L + col_widths[0]

            # Assigned (text field)
            form.textfield(
                name=f'{prefix}_assigned',
                x=cx + 3, y=field_y,
                width=col_widths[1] - 6, height=field_h,
                borderWidth=0,
                fontSize=9, fontName='Helvetica'
            )
            cx += col_widths[1]

            # Date Due (text field)
            form.textfield(
                name=f'{prefix}_due',
                x=cx + 3, y=field_y,
                width=col_widths[2] - 6, height=field_h,
                borderWidth=0,
                fontSize=8, fontName='Helvetica'
            )
            cx += col_widths[2]

            # Date Received (text field)
            form.textfield(
                name=f'{prefix}_recv',
                x=cx + 3, y=field_y,
                width=col_widths[3] - 6, height=field_h,
                borderWidth=0,
                fontSize=8, fontName='Helvetica'
            )
            cx += col_widths[3]

            # Status (dropdown)
            form.choice(
                name=f'{prefix}_status',
                options=status_options,
                value='--',
                x=cx + 3, y=field_y,
                width=col_widths[4] - 6, height=field_h,
                borderWidth=1,
                borderColor=LIGHT_GRAY,
                fillColor=white,
                textColor=black,
                fontSize=8, fontName='Helvetica',
            )

            y -= row_h

        y -= 20

    # Footer
    y -= 10
    c.setStrokeColor(GREEN)
    c.setLineWidth(2)
    c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
    y -= 18
    c.setFont('Helvetica', 10)
    c.setFillColor(HexColor('#777777'))
    c.drawCentredString(PAGE_W / 2, y, 'Brain-Based Mental Health Community - Feedback Task Tracker')

    c.save()

    # --- Phase 2: Inject Acrobat JavaScript for color coding ---
    reader = pypdf.PdfReader(tmp_path)
    writer = pypdf.PdfWriter()
    writer.append_pages_from_reader(reader)

    # Copy the AcroForm from the reader
    if '/AcroForm' in reader.trailer['/Root']:
        from pypdf.generic import NameObject
        writer._root_object[NameObject('/AcroForm')] = reader.trailer['/Root']['/AcroForm']

    # Build JS that hooks each status dropdown to color its row
    js_color_fn = """
function colorRow(prefix, val) {
    var c;
    if (val == "Sent") c = ["RGB", 1.0, 0.973, 0.882];
    else if (val == "In Progress") c = ["RGB", 0.890, 0.949, 0.992];
    else if (val == "Received") c = ["RGB", 0.929, 0.906, 0.965];
    else if (val == "Finalized") c = ["RGB", 0.910, 0.961, 0.914];
    else c = color.white;

    var suffixes = ["_assigned", "_due", "_recv", "_status"];
    for (var i = 0; i < suffixes.length; i++) {
        var f = this.getField(prefix + suffixes[i]);
        if (f) f.fillColor = c;
    }
}
"""

    # On document open, wire up all status dropdowns
    js_setup = js_color_fn + "\n"
    for prefix in row_prefixes:
        field_name = f"{prefix}_status"
        js_setup += (
            f'var f = this.getField("{field_name}");\n'
            f'if (f) f.setAction("Validate", '
            f"'colorRow(\"{prefix}\", event.value);');\n"
        )

    writer.add_js(js_setup)

    with open(pdf_path, 'wb') as out:
        writer.write(out)

    # Clean up temp file
    os.remove(tmp_path)


def main():
    feedback_dir = 'C:/Users/Tamra/Documents/Brain-Based Mental Health Website/Group Feedback'
    html_dir = os.path.join(feedback_dir, 'HTML')
    pdf_dir = os.path.join(feedback_dir, 'PDF')

    # Convert the Task Tracker separately
    tracker_html = os.path.join(html_dir, 'Feedback-Task-Tracker.html')
    tracker_pdf = os.path.join(pdf_dir, 'Feedback-Task-Tracker.pdf')
    if os.path.exists(tracker_html):
        try:
            convert_task_tracker(tracker_html, tracker_pdf)
            print(f'  Created: Feedback-Task-Tracker.pdf (fillable with dropdowns)')
        except Exception as e:
            print(f'  ERROR: Feedback-Task-Tracker.html -> {e}')

    # Convert regular feedback forms
    html_files = [f for f in os.listdir(html_dir)
                  if f.endswith('.html')
                  and f != 'Therapy-Guide-Reviewer-List.html'
                  and f != 'Feedback-Task-Tracker.html']

    for html_file in sorted(html_files):
        pdf_file = html_file.replace('.html', '.pdf')
        html_path = os.path.join(html_dir, html_file)
        pdf_path = os.path.join(pdf_dir, pdf_file)

        try:
            parse_and_convert(html_path, pdf_path)
            print(f'  Created: {pdf_file}')
        except Exception as e:
            print(f'  ERROR: {html_file} -> {e}')


if __name__ == '__main__':
    main()
