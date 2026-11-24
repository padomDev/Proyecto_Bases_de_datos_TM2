from __future__ import annotations

import contextlib
import io
import os
import shutil
import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw, ImageFont, ImageOps
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[2]
TMP = ROOT / "tmp" / "report"
ASSETS = TMP / "assets"
OUTPUT = ROOT / "output"
DOCX_PATH = OUTPUT / "Informe_Proyecto_Ciberseguridad_Pablo_Dominguez.docx"

TMP.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)


def font_path(mono=False, bold=False):
    candidates = []
    if mono:
        candidates = [
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/SFNSMono.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ]
    elif bold:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    return next((p for p in candidates if Path(p).exists()), candidates[-1])


def capture_call(function, answers):
    iterator = iter(answers)

    def fake_input(prompt=""):
        answer = next(iterator)
        print(f"{prompt}{answer}")
        return answer

    buffer = io.StringIO()
    with patch("builtins.input", fake_input), contextlib.redirect_stdout(buffer):
        function()
    return buffer.getvalue()


def console_image(text, path, title):
    lines = []
    for original in text.strip().splitlines():
        if len(original) <= 92:
            lines.append(original)
        else:
            lines.extend(textwrap.wrap(original, 92, subsequent_indent="  "))
    mono = ImageFont.truetype(font_path(mono=True), 21)
    title_font = ImageFont.truetype(font_path(bold=True), 23)
    line_h = 31
    width = 1500
    height = 105 + line_h * max(3, len(lines)) + 45
    image = Image.new("RGB", (width, height), "#111827")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((20, 20, width - 20, height - 20), radius=22, fill="#0b1020", outline="#334155", width=3)
    draw.ellipse((48, 45, 68, 65), fill="#ef4444")
    draw.ellipse((78, 45, 98, 65), fill="#f59e0b")
    draw.ellipse((108, 45, 128, 65), fill="#22c55e")
    draw.text((155, 40), title, font=title_font, fill="#e2e8f0")
    y = 90
    for line in lines:
        draw.text((55, y), line, font=mono, fill="#e5e7eb")
        y += line_h
    image.save(path)


def make_screenshots():
    data_dir = TMP / "demo_data"
    data_dir.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "config" / "app.db", data_dir / "app.db")
    os.environ["PROYECTO_CIBERSEGURIDAD_DATOS"] = str(data_dir)
    sys.path.insert(0, str(ROOT))

    import main
    from controllers.menu_logs import menu_logs
    from controllers.menu_sistema import menu_sistema
    from controllers.menu_vulnerabilidades import menu_vulnerabilidades

    fixed_question = {
        "id": 1,
        "pregunta": "¿Qué es un firewall?",
        "respuestas": [
            {"id": 1, "texto": "Un programa para editar imágenes"},
            {"id": 2, "texto": "Una barrera que filtra tráfico de red"},
            {"id": 3, "texto": "Un virus informático"},
            {"id": 4, "texto": "Un tipo de memoria RAM"},
        ],
    }
    with patch.object(main, "obtener_pregunta_aleatoria_repo", return_value=fixed_question), patch.object(
        main, "menu_sistema", lambda _id: print("Acceso concedido al menú del sistema")
    ):
        login = capture_call(main.menu_ingreso, ["2", "DemoUser1", "ClaveDemo1!", "B", "3"])

    system = capture_call(lambda: menu_sistema(1), ["3"])
    vulnerability = capture_call(lambda: menu_vulnerabilidades(1), ["1", "1", "0", "0"])
    logs = capture_call(menu_logs, ["1", "3650", "2"])

    console_image(login, ASSETS / "captura_login.png", "Inicio de sesión")
    console_image(system, ASSETS / "captura_menu.png", "Menú principal")
    console_image(vulnerability, ASSETS / "captura_vulnerabilidad.png", "Consulta de vulnerabilidades")
    console_image(logs, ASSETS / "captura_logs.png", "Consulta de logs")


def make_der_copy():
    image = Image.new("RGB", (1800, 1200), "white")
    draw = ImageDraw.Draw(image)
    title = ImageFont.truetype(font_path(bold=True), 38)
    head = ImageFont.truetype(font_path(bold=True), 24)
    body = ImageFont.truetype(font_path(), 19)
    relation_font = ImageFont.truetype(font_path(bold=True), 20)
    draw.text((900, 35), "Diagrama Entidad Relación completo", font=title, fill="#111827", anchor="ma")

    entities = {
        "USUARIOS": (55, 210, 400, 425, ["id", "nombre_usuario", "salt", "password_hash"]),
        "LOGS": (690, 205, 1095, 500, ["id", "fecha_hora", "tipo_evento", "id_usuario", "id_vulnerabilidad", "id_mitigacion"]),
        "VULNERABILIDADES": (1360, 185, 1770, 535, ["id", "nombre", "codigo_cve", "descripcion", "puntuacion_cvss", "severidad", "fecha_publicacion", "version_cvss", "id_categoria"]),
        "CATEGORIA": (1360, 780, 1770, 990, ["id", "nombre", "descripcion"]),
        "MITIGACIONES": (760, 790, 1190, 1060, ["id", "descripcion", "tipo_mitigacion", "prioridad", "id_vulnerabilidad"]),
        "PREGUNTAS": (55, 760, 400, 935, ["id", "enunciado"]),
        "RESPUESTAS": (55, 1010, 475, 1170, ["id", "id_pregunta", "texto", "es_correcta"]),
    }

    for name, (x1, y1, x2, y2, fields) in entities.items():
        draw.rounded_rectangle((x1, y1, x2, y2), radius=16, fill="#f8fafc", outline="#334155", width=4)
        draw.rounded_rectangle((x1, y1, x2, y1 + 48), radius=16, fill="#1e3a5f", outline="#1e3a5f")
        draw.rectangle((x1, y1 + 30, x2, y1 + 48), fill="#1e3a5f")
        draw.text(((x1 + x2) / 2, y1 + 24), name, font=head, fill="white", anchor="mm")
        y = y1 + 64
        for index, field in enumerate(fields):
            prefix = "PK " if index == 0 else ("FK " if field.startswith("id_") else "")
            draw.text((x1 + 18, y), prefix + field, font=body, fill="#111827")
            y += 30

    def relation(center, label, connections):
        cx, cy = center
        points = [(cx, cy - 42), (cx + 78, cy), (cx, cy + 42), (cx - 78, cy)]
        draw.polygon(points, fill="#ffffff", outline="#475569")
        wrapped = label.split(" ")
        if len(wrapped) == 1:
            draw.text((cx, cy), label, font=relation_font, fill="#111827", anchor="mm")
        else:
            draw.text((cx, cy - 11), wrapped[0], font=relation_font, fill="#111827", anchor="mm")
            draw.text((cx, cy + 13), " ".join(wrapped[1:]), font=relation_font, fill="#111827", anchor="mm")
        for start, end, cardinality, pos in connections:
            draw.line((start, end), fill="#64748b", width=4)
            draw.text(pos, cardinality, font=relation_font, fill="#111827", anchor="mm", stroke_width=4, stroke_fill="white")

    relation((545, 315), "GENERA", [
        ((400, 315), (467, 315), "1", (425, 292)),
        ((623, 315), (690, 315), "N", (662, 292)),
    ])
    relation((1230, 340), "REGISTRA", [
        ((1095, 340), (1152, 340), "N", (1120, 316)),
        ((1308, 340), (1360, 340), "0..1", (1334, 316)),
    ])
    relation((1515, 655), "CLASIFICA", [
        ((1515, 535), (1515, 613), "N", (1488, 575)),
        ((1515, 697), (1515, 780), "1", (1488, 738)),
    ])
    draw.line(((1020, 790), (1460, 535)), fill="#64748b", width=4)
    draw.text((1220, 645), "TIENE 1 a N", font=relation_font, fill="#111827", anchor="mm", stroke_width=5, stroke_fill="white")

    relation((260, 970), "TIENE", [
        ((260, 935), (260, 928), "1", (230, 944)),
        ((260, 1012), (260, 1010), "N", (230, 998)),
    ])

    # Relación opcional de LOGS con MITIGACIONES.
    draw.line(((905, 500), (975, 790)), fill="#64748b", width=4)
    draw.text((935, 645), "0..N", font=relation_font, fill="#111827", anchor="mm", stroke_width=5, stroke_fill="white")

    # RNE principales del modelo.
    rne_text = [
        "RNE: nombre_usuario y codigo_cve son únicos",
        "CVSS entre 0 y 10 | es_correcta en 0 o 1",
        "severidad, prioridad y tipo_evento usan valores permitidos",
        "cada clave externa debe referir un registro existente",
    ]
    draw.rounded_rectangle((500, 70, 1300, 170), radius=14, fill="#f1f5f9", outline="#94a3b8", width=3)
    for i, line in enumerate(rne_text):
        draw.text((900, 87 + i * 22), line, font=body, fill="#334155", anchor="ma")
    image.save(ASSETS / "der_claro.png")


def make_schema_diagram():
    image = Image.new("RGB", (1800, 1200), "white")
    draw = ImageDraw.Draw(image)
    title = ImageFont.truetype(font_path(bold=True), 38)
    head = ImageFont.truetype(font_path(bold=True), 26)
    body = ImageFont.truetype(font_path(), 21)
    draw.text((900, 42), "Esquema relacional implementado", font=title, fill="#111827", anchor="ma")

    boxes = {
        "usuarios": (70, 150, 520, 385, ["PK id", "nombre_usuario UNIQUE", "salt", "password_hash"]),
        "logs": (675, 115, 1160, 450, ["PK id", "fecha_hora", "tipo_evento", "FK id_usuario", "FK id_vulnerabilidad", "FK id_mitigacion"]),
        "categoria": (1290, 150, 1730, 350, ["PK id", "nombre UNIQUE", "descripcion"]),
        "preguntas": (70, 700, 520, 900, ["PK id", "enunciado"]),
        "respuestas": (675, 690, 1160, 955, ["PK id", "FK id_pregunta", "texto", "es_correcta"]),
        "vulnerabilidades": (1290, 480, 1730, 805, ["PK id", "nombre", "codigo_cve UNIQUE", "puntuacion_cvss", "severidad", "FK id_categoria"]),
        "mitigaciones": (1290, 900, 1730, 1135, ["PK id", "descripcion", "tipo_mitigacion", "prioridad", "FK id_vulnerabilidad"]),
    }

    def box(name, data):
        x1, y1, x2, y2, fields = data
        draw.rounded_rectangle((x1, y1, x2, y2), radius=18, fill="#f8fafc", outline="#334155", width=4)
        draw.rounded_rectangle((x1, y1, x2, y1 + 55), radius=18, fill="#1e3a5f", outline="#1e3a5f")
        draw.rectangle((x1, y1 + 35, x2, y1 + 55), fill="#1e3a5f")
        draw.text(((x1 + x2) / 2, y1 + 27), name.upper(), font=head, fill="white", anchor="mm")
        y = y1 + 76
        for field in fields:
            draw.text((x1 + 24, y), field, font=body, fill="#111827")
            y += 38

    for name, data in boxes.items():
        box(name, data)

    def arrow(a, b, label):
        draw.line((a, b), fill="#64748b", width=5)
        bx, by = b
        ax, ay = a
        import math
        angle = math.atan2(by - ay, bx - ax)
        size = 18
        p1 = (bx - size * math.cos(angle - 0.5), by - size * math.sin(angle - 0.5))
        p2 = (bx - size * math.cos(angle + 0.5), by - size * math.sin(angle + 0.5))
        draw.polygon([b, p1, p2], fill="#64748b")
        draw.text(((ax + bx) / 2, (ay + by) / 2 - 14), label, font=body, fill="#334155", anchor="mm", stroke_width=5, stroke_fill="white")

    arrow((520, 255), (675, 255), "1 a N")
    arrow((1510, 350), (1510, 480), "1 a N")
    arrow((1510, 805), (1510, 900), "1 a N")
    arrow((520, 800), (675, 800), "1 a N")
    arrow((1290, 610), (1160, 330), "1 a N")
    arrow((1290, 1010), (1160, 390), "1 a N")
    image.save(ASSETS / "esquema_relacional.png")


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color="D9D9D9", size="6"):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = borders.find(qn(f"w:{edge}"))
        if tag is None:
            tag = OxmlElement(f"w:{edge}")
            borders.append(tag)
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), size)
        tag.set(qn("w:color"), color)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def add_table(doc, headers, rows, widths=None, font_size=10.5):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    header = table.rows[0]
    set_repeat_table_header(header)
    for i, label in enumerate(headers):
        cell = header.cells[i]
        cell.text = str(label)
        set_cell_shading(cell, "1E3A5F")
        set_cell_margins(cell)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for run in cell.paragraphs[0].runs:
            run.font.name = "Times New Roman"
            run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
            run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
            run.font.size = Pt(font_size)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
        if widths:
            cell.width = Inches(widths[i])
    for r_idx, values in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(values):
            cell = cells[i]
            cell.text = str(value)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if r_idx % 2:
                set_cell_shading(cell, "F1F5F9")
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.paragraph_format.line_spacing = 1.05
                for run in paragraph.runs:
                    run.font.name = "Times New Roman"
                    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
                    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
                    run.font.size = Pt(font_size)
            if widths:
                cell.width = Inches(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def set_run_font(run, name="Times New Roman", size=12, bold=False, italic=False, color="000000"):
    run.font.name = name
    run._element.get_or_add_rPr()
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)


def add_field(paragraph, instruction, placeholder=""):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, text, end])
    return run


def add_body(doc, text, bold_lead=None):
    p = doc.add_paragraph(style="Body Text")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_lead and text.startswith(bold_lead):
        first = p.add_run(bold_lead)
        set_run_font(first, bold=True)
        rest = p.add_run(text[len(bold_lead):])
        set_run_font(rest)
    else:
        run = p.add_run(text)
        set_run_font(run)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.left_indent = Inches(0.28)
        p.paragraph_format.first_line_indent = Inches(-0.14)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(item)
        set_run_font(run)


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(text)
    set_run_font(run, size=10, italic=True, color="334155")


def add_picture(doc, path, width=6.2):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(path), width=Inches(width))


def add_code(doc, text, title=None, font_size=8.5):
    if title:
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        set_run_font(r, size=10, bold=True)
    for line in text.splitlines() or [""]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.18)
        p.paragraph_format.right_indent = Inches(0.08)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.keep_together = False
        r = p.add_run(line if line else " ")
        set_run_font(r, name="Courier New", size=font_size, color="1F2937")


def add_cached_toc(doc, entries):
    paragraphs = []
    for label, page, level in entries:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.22 * (level - 1))
        p.paragraph_format.space_after = Pt(5 if level == 1 else 3)
        p.paragraph_format.tab_stops.add_tab_stop(
            Inches(6.15), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
        )
        r = p.add_run(f"{label}\t{page}")
        set_run_font(r, size=11 if level == 1 else 10.5, bold=(level == 1))
        paragraphs.append(p)

    first_run = paragraphs[0].runs[0]
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = 'TOC \\o "1-3" \\h \\z \\u'
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    first_run._r.insert(0, separate)
    first_run._r.insert(0, instr)
    first_run._r.insert(0, begin)

    last_run = paragraphs[-1].runs[0]
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    last_run._r.append(end)


def page_break(doc):
    doc.add_page_break()


def configure_styles(doc):
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_after = Pt(7)
    normal.paragraph_format.line_spacing = 1.15

    body = styles["Body Text"]
    body.font.name = "Times New Roman"
    body._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    body._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    body.font.size = Pt(12)
    body.font.color.rgb = RGBColor(0, 0, 0)
    body.paragraph_format.space_after = Pt(8)
    body.paragraph_format.line_spacing = 1.15

    title = styles["Title"]
    title.font.name = "Times New Roman"
    title._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    title._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    title.font.size = Pt(18)
    title.font.bold = True
    title.font.color.rgb = RGBColor(0, 0, 0)
    title_ppr = title._element.get_or_add_pPr()
    title_border = title_ppr.find(qn("w:pBdr"))
    if title_border is not None:
        title_ppr.remove(title_border)

    for name, size in (("Heading 1", 18), ("Heading 2", 14), ("Heading 3", 12)):
        style = styles[name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(14 if name == "Heading 1" else 10)
        style.paragraph_format.space_after = Pt(7)
        style.paragraph_format.keep_with_next = True


def configure_document(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.78)
    section.bottom_margin = Inches(0.72)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)
    section.header_distance = Inches(0.35)
    section.footer_distance = Inches(0.35)

    footer = section.footer
    table = footer.add_table(rows=1, cols=2, width=Inches(6.8))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(5.5)
    table.columns[1].width = Inches(1.3)
    left = table.cell(0, 0).paragraphs[0]
    left.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = left.add_run("Proyecto final de Bases de Datos - Pablo Dominguez")
    set_run_font(r, size=9, color="475569")
    right = table.cell(0, 1).paragraphs[0]
    right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = right.add_run("Página ")
    set_run_font(r, size=9, color="475569")
    field_run = add_field(right, "PAGE", "1")
    set_run_font(field_run, size=9, color="475569")

    settings = doc.settings._element
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    settings.append(update)


def build_doc():
    doc = Document()
    configure_styles(doc)
    configure_document(doc)

    # Carátula
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(40)
    r = p.add_run("ITI - DGETP")
    set_run_font(r, size=14, bold=True)

    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(86)
    p.paragraph_format.space_after = Pt(20)
    p.add_run("Sistema de consulta de vulnerabilidades y auditoría de seguridad")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Informe del proyecto final")
    set_run_font(r, size=14, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(85)
    for label, value in [
        ("Asignatura", "Introducción a las Bases de Datos"),
        ("Carrera", "Tecnólogo en Ciberseguridad"),
        ("Docente", "Andrés Álvarez"),
        ("Integrante", "Pablo Dominguez"),
        ("Año", "2026"),
    ]:
        line = p.add_run(f"{label}: ")
        set_run_font(line, bold=True)
        line = p.add_run(value + "\n")
        set_run_font(line)

    page_break(doc)

    # Índice automático
    p = doc.add_paragraph(style="Title")
    p.add_run("Índice")
    add_cached_toc(doc, [
        ("1 Realidad planteada", 3, 1),
        ("2 Documento de requerimientos", 3, 1),
        ("3 Diseño y código fuente", 4, 1),
        ("4 Manual del programa", 5, 1),
        ("5 Diagrama Entidad Relación y RNE", 8, 1),
        ("6 Esquema relacional en tercera forma normal", 10, 1),
        ("7 Sentencias SQL", 11, 1),
        ("7 1 DDL", 11, 2),
        ("7 2 DML y datos iniciales", 13, 2),
        ("7 3 Consultas y operaciones CRUD", 13, 2),
        ("8 Verificación del proyecto", 15, 1),
        ("9 Conclusión", 16, 1),
        ("Anexo A Código fuente completo", 17, 1),
        ("Anexo B Datos iniciales", 31, 1),
    ])
    page_break(doc)

    doc.add_heading("1 Realidad planteada", level=1)
    add_body(doc, "Las organizaciones y los usuarios necesitan conocer las vulnerabilidades que afectan a sus sistemas, comprender su gravedad y consultar medidas de mitigación. Cuando esta información se encuentra dispersa, resulta difícil relacionar una vulnerabilidad con su categoría, sus datos CVE y las acciones recomendadas.")
    add_body(doc, "El proyecto resuelve esa necesidad mediante una aplicación de consola que administra un catálogo de vulnerabilidades. El usuario debe registrarse o iniciar sesión, responder una pregunta de seguridad y luego puede consultar vulnerabilidades, mitigaciones y registros de actividad. La información se conserva en una base de datos relacional SQLite.")
    add_body(doc, "La solución también registra eventos de auditoría. Cada registro identifica al usuario y distingue entre registro, inicio de sesión, consulta de vulnerabilidad y consulta de mitigación. Esto permite revisar qué acciones se realizaron y cuándo ocurrieron.")

    doc.add_heading("2 Documento de requerimientos", level=1)
    doc.add_heading("2 1 Requerimientos funcionales", level=2)
    requirements = [
        ("RF01", "Registrar usuarios", "El sistema debe validar el nombre, la contraseña y la respuesta de seguridad antes de guardar un usuario."),
        ("RF02", "Iniciar sesión", "El sistema debe comprobar usuario, contraseña y respuesta de seguridad."),
        ("RF03", "Proteger contraseñas", "El sistema debe almacenar un hash y un salt en lugar de la contraseña en texto claro."),
        ("RF04", "Consultar vulnerabilidades", "El sistema debe listar las vulnerabilidades disponibles y mostrar sus datos principales."),
        ("RF05", "Consultar mitigaciones", "El sistema debe mostrar las mitigaciones relacionadas con una vulnerabilidad."),
        ("RF06", "Registrar actividad", "El sistema debe crear logs para registros, ingresos y consultas."),
        ("RF07", "Consultar logs", "El usuario debe poder consultar los eventos de los últimos N días."),
        ("RF08", "Inicializar la base", "La aplicación debe crear las tablas y cargar los datos iniciales de forma idempotente."),
    ]
    add_table(doc, ["Código", "Nombre", "Descripción"], requirements, widths=[0.8, 1.45, 4.35])

    doc.add_heading("2 2 Requerimientos no funcionales", level=2)
    add_bullets(doc, [
        "La aplicación debe ejecutarse desde consola y controlar entradas numéricas inválidas.",
        "La base debe aplicar claves externas mediante PRAGMA foreign_keys = ON.",
        "La inicialización debe poder repetirse sin duplicar los datos de demostración.",
        "Las consultas deben utilizar parámetros para los valores ingresados por el usuario.",
        "El ejecutable de Windows debe incluir los scripts SQL necesarios para crear e inicializar la base.",
    ])

    doc.add_heading("3 Diseño y código fuente", level=1)
    doc.add_heading("3 1 Arquitectura del programa", level=2)
    add_body(doc, "El programa separa la interacción con el usuario, la lógica de autenticación y el acceso a datos. Esta organización reduce la duplicación y permite modificar una parte sin reescribir todo el sistema.")
    structure = [
        ("main.py", "Inicia la base y presenta el menú de registro e ingreso."),
        ("controllers", "Controla los menús de preguntas, vulnerabilidades, logs y sesión."),
        ("services", "Aplica las validaciones de registro e inicio de sesión."),
        ("repositories", "Ejecuta consultas parametrizadas contra SQLite."),
        ("config", "Define las rutas, conexión, claves externas e inicialización."),
        ("domines", "Genera el salt y el hash utilizados por la autenticación."),
        ("sql", "Contiene DDL, datos iniciales y consultas requeridas."),
    ]
    add_table(doc, ["Componente", "Responsabilidad"], structure, widths=[1.35, 5.25])

    doc.add_heading("3 2 Flujo principal", level=2)
    add_bullets(doc, [
        "Al comenzar, inicializar_db ejecuta crear_tablas.sql e insertar_datos.sql.",
        "El menú de ingreso permite registrarse, iniciar sesión o salir.",
        "Una pregunta aleatoria funciona como desafío adicional de acceso.",
        "Después del ingreso, el usuario consulta vulnerabilidades, mitigaciones o logs.",
        "Los repositorios registran los eventos asociados al usuario autenticado.",
    ])

    doc.add_heading("3 3 Consideración de seguridad", level=2)
    add_body(doc, "El proyecto implementa un hash educativo de 16 bytes con salt. Este mecanismo demuestra que una contraseña no debe guardarse en texto claro y permite validar el ingreso con el mismo salt. Para un sistema de producción correspondería usar una función especializada y resistente, como Argon2, bcrypt o PBKDF2.")
    add_body(doc, "El código fuente completo, con los comentarios incluidos en el proyecto, se presenta en el Anexo A.")

    doc.add_heading("4 Manual del programa", level=1)
    doc.add_heading("4 1 Inicio", level=2)
    add_body(doc, "Durante el desarrollo se ejecuta python main.py desde la carpeta del proyecto. En Windows también puede generarse ProyectoCiberseguridad.exe con compilar_windows.bat. Al iniciar, la aplicación crea o actualiza la base y carga los datos que falten.")

    doc.add_heading("4 2 Inicio de sesión", level=2)
    add_body(doc, "Para ingresar se selecciona la opción 2, se escribe el usuario y la contraseña, y se responde la pregunta de seguridad. Las credenciales de demostración incluyen DemoUser1 con contraseña ClaveDemo1!.")
    add_picture(doc, ASSETS / "captura_login.png", 6.25)
    add_caption(doc, "Figura 1 Inicio de sesión con un usuario de demostración")

    doc.add_heading("4 3 Menú principal", level=2)
    add_body(doc, "Después de autenticar al usuario, el menú principal permite consultar vulnerabilidades, revisar logs o cerrar la sesión.")
    add_picture(doc, ASSETS / "captura_menu.png", 6.25)
    add_caption(doc, "Figura 2 Menú principal del sistema")

    doc.add_heading("4 4 Consulta de vulnerabilidades", level=2)
    add_body(doc, "La opción de vulnerabilidades muestra el catálogo. Al elegir una entrada se presentan el código CVE, la severidad, la descripción y las mitigaciones relacionadas. La consulta queda registrada en logs.")
    add_picture(doc, ASSETS / "captura_vulnerabilidad.png", 6.25)
    add_caption(doc, "Figura 3 Consulta de una vulnerabilidad y su mitigación")

    doc.add_heading("4 5 Consulta de logs", level=2)
    add_body(doc, "El usuario indica la cantidad de días que desea consultar. El sistema devuelve los eventos en orden descendente e incluye la vulnerabilidad o mitigación cuando corresponde.")
    add_picture(doc, ASSETS / "captura_logs.png", 6.25)
    add_caption(doc, "Figura 4 Consulta de eventos de auditoría")

    doc.add_heading("4 6 Credenciales de demostración", level=2)
    creds = [(f"DemoUser{i}", f"ClaveDemo{i}!") for i in range(1, 6)]
    add_table(doc, ["Usuario", "Contraseña"], creds, widths=[3.0, 3.0])

    doc.add_heading("5 Diagrama Entidad Relación y RNE", level=1)
    add_body(doc, "El diagrama representa las siete entidades implementadas: usuarios, logs, vulnerabilidades, mitigaciones, categorías, preguntas y respuestas. Las cardinalidades muestran las relaciones uno a muchos y las asociaciones opcionales de los eventos de auditoría.")
    add_picture(doc, ASSETS / "der_claro.png", 6.2)
    add_caption(doc, "Figura 5 Diagrama Entidad Relación completo")

    doc.add_heading("5 1 Restricciones no estructurales", level=2)
    rne = [
        ("RNE01", "El nombre de usuario debe ser único y no puede ser nulo."),
        ("RNE02", "El código CVE debe identificar una única vulnerabilidad."),
        ("RNE03", "La puntuación CVSS debe estar entre 0 y 10."),
        ("RNE04", "La severidad solo puede ser Baja, Media, Alta o Critica."),
        ("RNE05", "La prioridad de una mitigación solo puede ser Baja, Media o Alta."),
        ("RNE06", "Una respuesta solo puede marcarse como incorrecta 0 o correcta 1."),
        ("RNE07", "Cada mitigación debe pertenecer a una vulnerabilidad existente."),
        ("RNE08", "Cada vulnerabilidad debe pertenecer a una categoría existente."),
        ("RNE09", "Un log de REGISTRO o LOGIN no puede referir vulnerabilidad ni mitigación."),
        ("RNE10", "Un log de VULNERABILIDAD debe tener vulnerabilidad y no mitigación."),
        ("RNE11", "Un log de MITIGACION debe tener mitigación y no vulnerabilidad."),
    ]
    add_table(doc, ["Código", "Regla"], rne, widths=[0.85, 5.75])

    doc.add_heading("6 Esquema relacional en tercera forma normal", level=1)
    add_picture(doc, ASSETS / "esquema_relacional.png", 6.3)
    add_caption(doc, "Figura 6 Esquema relacional implementado con claves externas")
    schema = [
        ("usuarios", "id", "-", "nombre_usuario, salt, password_hash"),
        ("preguntas", "id", "-", "enunciado"),
        ("respuestas", "id", "id_pregunta -> preguntas.id", "texto, es_correcta"),
        ("categoria", "id", "-", "nombre, descripcion"),
        ("vulnerabilidades", "id", "id_categoria -> categoria.id", "nombre, codigo_cve, descripcion, puntuacion_cvss, severidad, fecha_publicacion, version_cvss"),
        ("mitigaciones", "id", "id_vulnerabilidad -> vulnerabilidades.id", "descripcion, tipo_mitigacion, prioridad"),
        ("logs", "id", "id_usuario -> usuarios.id; id_vulnerabilidad -> vulnerabilidades.id; id_mitigacion -> mitigaciones.id", "fecha_hora, tipo_evento"),
    ]
    add_table(doc, ["Relación", "PK", "FK", "Atributos"], schema, widths=[1.1, 0.55, 2.4, 2.55], font_size=9.5)
    add_body(doc, "Las relaciones se encuentran en tercera forma normal porque cada atributo contiene un valor atómico, todos los atributos no clave dependen de la clave primaria completa y no se almacenan dependencias transitivas entre atributos no clave. Las categorías y mitigaciones se separan de las vulnerabilidades, mientras que las respuestas se separan de las preguntas.")

    doc.add_heading("7 Sentencias SQL", level=1)
    doc.add_heading("7 1 DDL", level=2)
    add_body(doc, "crear_tablas.sql define siete tablas, por lo que supera el mínimo de cinco. Las claves externas relacionan respuestas, vulnerabilidades, mitigaciones y logs. Las restricciones UNIQUE y CHECK controlan nombres, códigos CVE, puntuaciones, severidades, prioridades y tipos de evento.")
    ddl_excerpt = (ROOT / "sql" / "crear_tablas.sql").read_text(encoding="utf-8")
    add_code(doc, ddl_excerpt, "Listado 1 Definición completa de tablas")

    doc.add_heading("7 2 DML y datos iniciales", level=2)
    counts = [
        ("usuarios", 5), ("categoria", 5), ("vulnerabilidades", 5),
        ("mitigaciones", 10), ("preguntas", 5), ("respuestas", 20), ("logs", 9),
    ]
    add_table(doc, ["Tabla", "Registros verificados"], counts, widths=[3.2, 2.8])
    add_body(doc, "insertar_datos.sql utiliza INSERT OR IGNORE. Para los logs, que no poseen una clave única adecuada para identificar un evento de demostración, también utiliza NOT EXISTS. Esto permite ejecutar la inicialización varias veces sin duplicar ni sobrescribir información.")

    doc.add_heading("7 3 Consultas y operaciones CRUD", level=2)
    add_body(doc, "consultas.sql incluye consultas de una tabla, INNER JOIN y LEFT JOIN, además de los cuatro informes requeridos. Los ejemplos de INSERT, UPDATE y DELETE se ejecutan dentro de una transacción que termina con ROLLBACK, por lo que no alteran permanentemente la base real.")
    dml_text = (ROOT / "sql" / "consultas.sql").read_text(encoding="utf-8")
    add_code(doc, dml_text, "Listado 2 Consultas e informes requeridos")

    doc.add_heading("7 4 Resultados de los informes", level=2)
    reports = [
        ("Tabular", "Lista las cinco vulnerabilidades con código CVE, severidad y puntuación."),
        ("Resumen", "Muestra cuatro vulnerabilidades de ejecución remota y una de denegación de servicio."),
        ("Detalle", "Relaciona cada vulnerabilidad con su categoría y sus mitigaciones."),
        ("Comparativo", "Compara 2 vulnerabilidades críticas con promedio 9,90 y 3 altas con promedio 8,37."),
    ]
    add_table(doc, ["Informe", "Resultado"], reports, widths=[1.25, 5.35])

    doc.add_heading("8 Verificación del proyecto", level=1)
    checks = [
        ("Compilación de módulos Python", "Correcta", "compileall no informó errores."),
        ("Cantidad mínima por tabla", "Correcta", "Todas las tablas poseen al menos cinco registros."),
        ("Claves externas", "Correcta", "PRAGMA foreign_key_check no devolvió filas."),
        ("Integridad", "Correcta", "PRAGMA integrity_check devolvió ok."),
        ("Inicio de sesión", "Correcta", "DemoUser1 pudo autenticarse con ClaveDemo1!."),
        ("Consultas SQL", "Correcta", "Las sentencias se ejecutaron sin errores y ROLLBACK conservó los datos."),
    ]
    add_table(doc, ["Prueba", "Estado", "Evidencia"], checks, widths=[2.1, 1.0, 3.5], font_size=10)

    doc.add_heading("9 Conclusión", level=1)
    add_body(doc, "El proyecto implementa una aplicación funcional para consultar vulnerabilidades y mitigaciones sobre una base relacional. La solución dispone de autenticación, preguntas de seguridad, auditoría de eventos, siete tablas relacionadas, datos de demostración y consultas que cubren operaciones CRUD e informes.")
    add_body(doc, "Las verificaciones confirman que el esquema mantiene su integridad, las claves externas son válidas y la inicialización puede repetirse. Como mejora futura, el hash educativo debería reemplazarse por un algoritmo de contraseñas diseñado para producción.")

    page_break(doc)
    doc.add_heading("Anexo A Código fuente completo", level=1)
    add_body(doc, "Este anexo reúne el código Python entregado. Los comentarios existentes explican las validaciones, conexiones y operaciones principales.")
    source_files = [
        "main.py",
        "config/conexion.py",
        "domines/security.py",
        "services/auth_service.py",
        "repositories/usuarios_repo.py",
        "repositories/preguntas_repo.py",
        "repositories/vulnerabilidades_repo.py",
        "repositories/logs_repo.py",
        "controllers/menu_pregunta.py",
        "controllers/menu_sistema.py",
        "controllers/menu_vulnerabilidades.py",
        "controllers/menu_logs.py",
    ]
    for file_name in source_files:
        doc.add_heading(file_name.replace("_", " "), level=2)
        add_code(doc, (ROOT / file_name).read_text(encoding="utf-8"))

    page_break(doc)
    doc.add_heading("Anexo B Datos iniciales", level=1)
    add_body(doc, "El siguiente script carga categorías, vulnerabilidades, mitigaciones, preguntas, respuestas, usuarios y logs de demostración.")
    add_code(doc, (ROOT / "sql" / "insertar_datos.sql").read_text(encoding="utf-8"), font_size=8.0)

    doc.core_properties.title = "Sistema de consulta de vulnerabilidades y auditoría de seguridad"
    doc.core_properties.subject = "Proyecto final de Introducción a las Bases de Datos"
    doc.core_properties.author = "Pablo Dominguez"
    doc.core_properties.keywords = "bases de datos, ciberseguridad, SQLite, vulnerabilidades"
    doc.save(DOCX_PATH)
    return DOCX_PATH


if __name__ == "__main__":
    make_screenshots()
    make_der_copy()
    make_schema_diagram()
    print(build_doc())
