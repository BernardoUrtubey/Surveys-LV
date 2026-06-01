```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import math
import io
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_COLOR = os.path.join(BASE_DIR, 'logo_color_transp.png')
LOGO_WM    = os.path.join(BASE_DIR, 'logo_wm_final.png')

W, H = A4

DARK_RED   = colors.Color(0.482353, 0.113725, 0.07451)
RED_LINE   = colors.Color(0.752941, 0.223529, 0.168627)
RED_STRIPE = colors.Color(0.909804, 0.270588, 0.235294)
DARK_NAV   = colors.Color(0.066667, 0.094118, 0.152941)
KPI_RED    = colors.Color(0.752941, 0.223529, 0.168627)
LIGHT_PINK = colors.Color(0.996078, 0.964706, 0.964706)
ROW_GRAY   = colors.Color(0.952941, 0.956863, 0.964706)
LABEL_GRAY = colors.Color(0.611765, 0.639216, 0.686275)
TEXT_DARK  = colors.Color(0.066667, 0.094118, 0.152941)
SEP_GRAY   = colors.Color(0.898039, 0.905882, 0.921569)
WHITE      = colors.white
NOTES_BG   = colors.Color(1.0, 0.984314, 0.921569)

LABELS = {
    'es': {
        'subtitle':       'Mudanzas & Relocation Internacional',
        'report_title':   'INFORME DE SURVEY',
        'client':         'CLIENTE',
        'destination':    'DESTINO',
        'est_volume':     'VOLUMEN EST.',
        'kpi_volume':     'VOLUMEN ESTIMADO',
        'kpi_container':  'CONTENEDOR',
        'kpi_packing':    'FECHA EMBALAJE',
        'kpi_rooms':      'AMBIENTES',
        'row_destination':'DESTINO',
        'row_nationality':'NACIONALIDAD',
        'row_survey_date':'FECHA RELEVAMIENTO',
        'row_packing':    'FECHA EMBALAJE',
        'row_allowance':  'FRANQUICIA',
        'row_background': 'ANTECEDENTE',
        'inventory':      'INVENTARIO POR AMBIENTE',
        'crates':         'ESQUELETOS / EMBALAJES ESPECIALES',
        'notes':          'NOTAS OPERATIVAS',
        'page':           'Pág.',
    },
    'en': {
        'subtitle':       'International Moving & Relocation',
        'report_title':   'SURVEY REPORT',
        'client':         'CLIENT',
        'destination':    'DESTINATION',
        'est_volume':     'EST. VOLUME',
        'kpi_volume':     'EST. VOLUME',
        'kpi_container':  'CONTAINER',
        'kpi_packing':    'PACKING DATE',
        'kpi_rooms':      'ROOMS',
        'row_destination':'DESTINATION',
        'row_nationality':'NATIONALITY',
        'row_survey_date':'SURVEY DATE',
        'row_packing':    'PACKING DATE',
        'row_allowance':  'CUSTOMS ALLOWANCE',
        'row_background': 'BACKGROUND',
        'inventory':      'INVENTORY BY ROOM',
        'crates':         'CRATES / SPECIAL PACKAGING',
        'notes':          'OPERATIONAL NOTES',
        'page':           'Page',
    }
}


def draw_page_bg(c):
    c.setFillColor(LIGHT_PINK)
    c.rect(0, 25.49, W, 703.0, fill=1, stroke=0)


def draw_watermark(c):
    tile_w = 206
    tile_h = 178
    x_step = 226
    y_step = 106
    stagger = 113
    for row in range(-1, 10):
        for col in range(-1, 5):
            offset = stagger if row % 2 == 1 else 0
            x = col * x_step + offset - 30
            y = H - (row * y_step + tile_h + 30)
            c.drawImage(LOGO_WM, x, y, width=tile_w, height=tile_h,
                        mask='auto', preserveAspectRatio=True)


def draw_header(c, data, lbl):
    c.setFillColor(DARK_RED)
    c.rect(0, H - 113.4, W, 113.4, fill=1, stroke=0)
    c.setFillColor(RED_LINE)
    c.rect(0, H - 116.2, W, 2.8, fill=1, stroke=0)
    c.setFillColor(RED_STRIPE)
    p = c.beginPath()
    p.moveTo(238.1, H - 113.4)
    p.lineTo(297.6, H)
    p.lineTo(315.5, H)
    p.lineTo(256.0, H - 113.4)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.drawImage(LOGO_COLOR, 45.35, 778.21, width=164.4, height=36.65,
                mask='auto', preserveAspectRatio=True)
    c.setFillColor(colors.Color(0.75, 0.75, 0.75))
    c.setFont("Helvetica", 7.5)
    c.drawString(45.4, H - 89, lbl['subtitle'])
    c.setStrokeColor(colors.Color(0.55, 0.55, 0.55))
    c.setLineWidth(0.8)
    c.line(45.4, H - 94, 201.3, H - 94)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(45.4, H - 108, lbl['report_title'])
    rx = 549.9
    volume_str = f"{data.get('volume', '')}  \u00b7  {data.get('container', '')}"
    c.setFillColor(colors.Color(0.7, 0.7, 0.7))
    c.setFont("Helvetica", 6)
    c.drawRightString(rx, H - 21, lbl['client'])
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(rx, H - 34, data.get('client', ''))
    c.setFillColor(colors.Color(0.7, 0.7, 0.7))
    c.setFont("Helvetica", 6)
    c.drawRightString(rx, H - 55, lbl['destination'])
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(rx, H - 67, data.get('destination', ''))
    c.setFillColor(colors.Color(0.7, 0.7, 0.7))
    c.setFont("Helvetica", 6)
    c.drawRightString(rx, H - 86, lbl['est_volume'])
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(rx, H - 98, volume_str)


def draw_footer(c, lbl, page_num):
    c.setFillColor(DARK_NAV)
    c.rect(0, 0, W, 25.5, fill=1, stroke=0)
    c.setFillColor(RED_LINE)
    c.rect(0, 0, 8.5, 25.5, fill=1, stroke=0)
    c.setFillColor(colors.Color(0.65, 0.65, 0.65))
    c.setFont("Helvetica", 7.5)
    c.drawString(16, 9, "Lift Van International  \u00b7  sales@liftvan.com  \u00b7  liftvan.com  \u00b7  +54 11 4016-1100")
    c.drawRightString(W - 10, 9, f"{lbl['page']} {page_num}")


def draw_kpis(c, data, lbl):
    top = H - 133.6
    bot = H - 174.6
    kpi_h = top - bot
    cols = [62.4, 180.0, 297.6, 415.3, 532.9]
    kpis = [
        (data.get('volume', '\u2014'), lbl['kpi_volume']),
        (data.get('container', '\u2014'), lbl['kpi_container']),
        (data.get('packing_date', '\u2014'), lbl['kpi_packing']),
        (str(len(data.get('rooms', []))), lbl['kpi_rooms']),
    ]
    for i, (val, label) in enumerate(kpis):
        x0, x1 = cols[i], cols[i+1]
        cx = (x0 + x1) / 2
        c.setFillColor(ROW_GRAY)
        c.rect(x0, bot, x1-x0, kpi_h, fill=1, stroke=0)
        c.setFillColor(KPI_RED)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(cx, bot + kpi_h - 24, val)
        c.setFillColor(LABEL_GRAY)
        c.setFont("Helvetica", 5.5)
        c.drawCentredString(cx, bot + 6, label)
    c.setStrokeColor(RED_LINE)
    c.setLineWidth(2)
    for i in range(4):
        c.line(cols[i], top, cols[i+1], top)
    return bot


def draw_general_table(c, data, lbl, start_y):
    rows = [
        (lbl['row_destination'], data.get('destination_detail', data.get('destination', '')), True),
        (lbl['row_nationality'], data.get('nationality', ''), False),
        (lbl['row_survey_date'], data.get('survey_date', ''), True),
        (lbl['row_packing'], data.get('packing_date', '') + ' \u00b7 ' + data.get('packing_days', ''), False),
        (lbl['row_allowance'], data.get('allowance', ''), True),
        (lbl['row_background'], data.get('background', ''), False),
    ]
    row_h = 20
    y = start_y
    for label, value, is_white in rows:
        c.setFillColor(WHITE if is_white else ROW_GRAY)
        c.rect(45.4, y-row_h, 504.5, row_h, fill=1, stroke=0)
        c.setStrokeColor(SEP_GRAY)
        c.setLineWidth(0.3)
        c.line(45.4, y-row_h, 549.9, y-row_h)
        c.setFillColor(LABEL_GRAY)
        c.setFont("Helvetica", 6)
        c.drawString(50.4, y-13, label)
        c.setFillColor(TEXT_DARK)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(158.1, y-13, value)
        y -= row_h
    c.setStrokeColor(RED_LINE)
    c.setLineWidth(2)
    c.line(153.07, y, 153.07, start_y)
    return y


def draw_section_header(c, y, title):
    hdr_h = 17
    c.setFillColor(DARK_NAV)
    c.rect(45.4, y-hdr_h, 504.5, hdr_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(53.4, y-12, title)
    return y - hdr_h


def draw_room(c, y, room_name, items):
    name_h = 18
    c.setFillColor(ROW_GRAY)
    c.rect(45.4, y-name_h, 504.5, name_h, fill=1, stroke=0)
    c.setStrokeColor(RED_LINE)
    c.setLineWidth(3)
    c.line(45.4, y, 45.4, y-name_h)
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(51.4, y-13, room_name)
    y -= name_h
    row_count = math.ceil(len(items) / 3)
    item_h = 16
    col_w = 504.5 / 3
    for row in range(row_count):
        bg = WHITE if row % 2 == 0 else ROW_GRAY
        c.setFillColor(bg)
        c.rect(45.4, y-item_h, 504.5, item_h, fill=1, stroke=0)
        c.setStrokeColor(SEP_GRAY)
        c.setLineWidth(0.2)
        c.line(45.4, y-item_h, 549.9, y-item_h)
        c.setStrokeColor(RED_LINE)
        c.setLineWidth(3)
        c.line(45.4, y, 45.4, y-item_h)
        for col in range(3):
            idx = row*3 + col
            if idx < len(items):
                ix = 45.4 + col*col_w + 6
                c.setFillColor(TEXT_DARK)
                c.setFont("Helvetica", 7.5)
                c.drawString(ix, y-11, f"\u2013 {items[idx]}")
        y -= item_h
    c.setStrokeColor(SEP_GRAY)
    c.setLineWidth(0.3)
    c.line(45.4, y, 549.9, y)
    return y - 6


def draw_crates(c, y, crates, lbl):
    hdr_h = 17
    c.setFillColor(DARK_NAV)
    c.rect(45.4, y-hdr_h, 504.5, hdr_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(53.4, y-12, lbl['crates'])
    y -= hdr_h + 10
    col_w = 504.5 / 2
    row_h = 20
    rows = [crates[i:i+2] for i in range(0, len(crates), 2)]
    for r in rows:
        for j, item in enumerate(r):
            xb = 45.4 + j*col_w
            c.setFillColor(RED_LINE)
            c.rect(xb+5, y-12, 7, 7, fill=1, stroke=0)
            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica", 8)
            c.drawString(xb+16, y-7, item.get('name', ''))
            c.setFillColor(KPI_RED)
            c.setFont("Helvetica-Bold", 8)
            c.drawRightString(xb+col_w-5, y-7, item.get('status', ''))
        y -= row_h
    return y - 6


def draw_notes(c, y, notes, lbl):
    note_h = 18
    hdr_h = 17
    total_h = hdr_h + len(notes)*note_h + 8
    c.setFillColor(NOTES_BG)
    c.rect(45.4, y-total_h, 504.5, total_h, fill=1, stroke=0)
    c.setFillColor(DARK_NAV)
    c.rect(45.4, y-hdr_h, 504.5, hdr_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(53.4, y-12, lbl['notes'])
    ny = y - hdr_h - 6
    for note in notes:
        c.setFillColor(colors.Color(0.9, 0.65, 0.1))
        c.circle(55, ny-2, 2.5, fill=1, stroke=0)
        c.setFillColor(TEXT_DARK)
        c.setFont("Helvetica", 7.5)
        c.drawString(62, ny-5, note)
        ny -= note_h
    return y - total_h


def room_height(items):
    return 18 + math.ceil(len(items) / 3) * 16 + 6


def generate_survey_pdf(data, lang='es'):
    lbl = LABELS[lang]
    buf = io.BytesIO()
    cv = canvas.Canvas(buf, pagesize=A4)
    rooms = data.get('rooms', [])
    crates = data.get('crates', [])
    notes = data.get('notes', [])

    def new_page(page_num):
        draw_page_bg(cv)
        draw_watermark(cv)
        draw_header(cv, data, lbl)
        draw_footer(cv, lbl, page_num)

    page_num = 1
    new_page(page_num)
    kpi_bot = draw_kpis(cv, data, lbl)
    table_bot = draw_general_table(cv, data, lbl, kpi_bot - 8)
    y = table_bot - 8
    y = draw_section_header(cv, y, lbl['inventory'])
    y -= 6
    BOTTOM_LIMIT = 45

    for room in rooms:
        rh = room_height(room.get('items', []))
        if y - rh < BOTTOM_LIMIT:
            cv.showPage()
            page_num += 1
            new_page(page_num)
            y = H - 133.6 - 6
        y = draw_room(cv, y, room.get('name', ''), room.get('items', []))

    if crates:
        crate_h = 17 + math.ceil(len(crates)/2) * 20 + 16
        if y - crate_h < BOTTOM_LIMIT:
            cv.showPage()
            page_num += 1
            new_page(page_num)
            y = H - 133.6 - 6
        y -= 6
        y = draw_crates(cv, y, crates, lbl)

    if notes:
        notes_h = 17 + len(notes)*18 + 8 + 14
        if y - notes_h < BOTTOM_LIMIT:
            cv.showPage()
            page_num += 1
            new_page(page_num)
            y = H - 133.6 - 6
        y -= 6
        draw_notes(cv, y, notes, lbl)

    cv.save()
    buf.seek(0)
    return buf.read()
```

Click **"Commit changes"** y avisame. ¡Ya casi está!
