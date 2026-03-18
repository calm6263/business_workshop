# schedule/pdf_utils.py
import io
import os
import sys
import tempfile
import zipfile
import urllib.request
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import FileResponse, HttpResponse
from .models import ScheduleProgram

def download_calendar_pdf(request):
    """تحميل التقويم كملف PDF مطابق لشكل الموقع مع خط Arial"""
    try:
        # محاولة تسجيل خط Arial
        font_name = 'Arial'
        try:
            arial_paths = [
                'C:/Windows/Fonts/arial.ttf',
                'C:/Windows/Fonts/arialbd.ttf',
                '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'fonts', 'arial.ttf'),
            ]
            for font_path in arial_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('Arial', font_path))
                        bold_path = font_path.replace('.ttf', 'bd.ttf')
                        bold_path = bold_path.replace('arial.ttf', 'arialbd.ttf')
                        bold_path = bold_path.replace('Arial.ttf', 'Arial_Bold.ttf')
                        if os.path.exists(bold_path):
                            pdfmetrics.registerFont(TTFont('Arial-Bold', bold_path))
                        else:
                            pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))
                        print(f"تم تسجيل خط Arial من: {font_path}")
                        font_name = 'Arial'
                        break
                    except Exception as e:
                        print(f"خطأ في تسجيل خط Arial من {font_path}: {e}")
                        continue
        except Exception as e:
            print(f"لم يتم العثور على خط Arial، سيتم استخدام Helvetica: {e}")
            font_name = 'Helvetica'

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer,
                              pagesize=landscape(A4),
                              rightMargin=1.5*cm,
                              leftMargin=1.5*cm,
                              topMargin=2*cm,
                              bottomMargin=2*cm,
                              title="Календарь программ")

        elements = []

        selected_date_str = request.GET.get('date', '')
        if selected_date_str:
            try:
                selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
                current_year = selected_date.year
                current_month = selected_date.month
            except:
                current_date = datetime.now()
                current_year = current_date.year
                current_month = current_date.month
        else:
            current_date = datetime.now()
            current_year = current_date.year
            current_month = current_date.month

        month_names_ru = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
        weekday_names = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']

        programs = ScheduleProgram.objects.filter(
            is_active=True,
            start_date__year=current_year,
            start_date__month=current_month
        ).order_by('start_date')

        events_by_day = {}
        for program in programs:
            day = program.start_date.day
            if day not in events_by_day:
                events_by_day[day] = []
            color_map = {
                'professional_retraining': '#052946',
                'qualification_upgrade': '#2E7D32',
                'seminar': '#7F1726',
                'training': '#FF9800',
                'other': '#6A1B9A',
            }
            events_by_day[day].append({
                'title': program.title,
                'type': program.program_type,
                'color': color_map.get(program.program_type, '#052946'),
                'slug': program.slug,
            })

        styles = getSampleStyleSheet()
        regular_font = font_name
        bold_font = f"{font_name}-Bold" if font_name == 'Arial' else f"{font_name}-Bold"

        title_style = ParagraphStyle(
            'MainTitle',
            parent=styles['Title'],
            fontName=bold_font,
            fontSize=36,
            alignment=TA_CENTER,
            spaceAfter=15,
            textColor=colors.HexColor('#052946')
        )
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontName=bold_font,
            fontSize=28,
            alignment=TA_CENTER,
            spaceAfter=40,
            textColor=colors.HexColor('#7F1726')
        )
        weekday_style = ParagraphStyle(
            'WeekdayStyle',
            parent=styles['Normal'],
            fontName=bold_font,
            fontSize=24,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#7F1726'),
            spaceAfter=0
        )
        day_number_style = ParagraphStyle(
            'DayNumberStyle',
            parent=styles['Normal'],
            fontName=regular_font,
            fontSize=20,
            alignment=TA_RIGHT,
            textColor=colors.black,
            rightIndent=5
        )
        weekend_day_style = ParagraphStyle(
            'WeekendDayStyle',
            parent=styles['Normal'],
            fontName=regular_font,
            fontSize=20,
            alignment=TA_RIGHT,
            textColor=colors.HexColor('#7F1726'),
            rightIndent=5
        )
        event_style = ParagraphStyle(
            'EventStyle',
            parent=styles['Normal'],
            fontName=regular_font,
            fontSize=8,
            alignment=TA_LEFT,
            textColor=colors.white,
            leftIndent=2,
            spaceBefore=1,
            spaceAfter=1
        )
        more_events_style = ParagraphStyle(
            'MoreEventsStyle',
            parent=styles['Normal'],
            fontName=bold_font,
            fontSize=7,
            alignment=TA_CENTER,
            textColor=colors.white,
            spaceBefore=1,
            spaceAfter=1
        )

        elements.append(Paragraph("КАЛЕНДАРЬ ПРОГРАММ", title_style))
        month_year_text = f"{month_names_ru[current_month-1].upper()} {current_year}"
        elements.append(Paragraph(month_year_text, subtitle_style))
        elements.append(Spacer(1, 30))

        import calendar
        cal = calendar.monthcalendar(current_year, current_month)

        num_weeks = len(cal)
        cell_width = doc.width / 7
        cell_height = (doc.height - 200) / (num_weeks + 1)

        table_data = []

        header_row = []
        for day_name in weekday_names:
            header_row.append(Paragraph(day_name.upper(), weekday_style))
        table_data.append(header_row)

        for week in cal:
            row = []
            for day_num, day in enumerate(week):
                cell_elements = []
                if day == 0:
                    row.append('')
                else:
                    day_cell = []
                    if day_num >= 5:
                        day_number = Paragraph(str(day), weekend_day_style)
                    else:
                        day_number = Paragraph(str(day), day_number_style)

                    if day in events_by_day:
                        events = events_by_day[day]
                        event_count = len(events)
                        if event_count == 1:
                            event = events[0]
                            event_text = Paragraph(
                                f'<para bgcolor="{event["color"]}">{event["title"][:30]}</para>',
                                event_style
                            )
                            cell_elements.append(event_text)
                        elif event_count == 2:
                            for i, event in enumerate(events[:2]):
                                event_text = Paragraph(
                                    f'<para bgcolor="{event["color"]}">{event["title"][:15]}</para>',
                                    event_style
                                )
                                cell_elements.append(event_text)
                        else:
                            for i, event in enumerate(events[:2]):
                                event_text = Paragraph(
                                    f'<para bgcolor="{event["color"]}">{event["title"][:15]}</para>',
                                    event_style
                                )
                                cell_elements.append(event_text)
                            more_text = Paragraph(
                                f'<para bgcolor="#052946">+{event_count-2} больше</para>',
                                more_events_style
                            )
                            cell_elements.append(more_text)

                    if cell_elements:
                        inner_table_data = [[day_number]]
                        for element in cell_elements:
                            inner_table_data.append([element])
                        inner_table = Table(inner_table_data,
                                          colWidths=[cell_width - 10],
                                          rowHeights=[20] + [15] * len(cell_elements))
                        inner_table.setStyle(TableStyle([
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                            ('TOPPADDING', (0, 0), (-1, -1), 0),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                        ]))
                        row.append(inner_table)
                    else:
                        row.append(day_number)
            table_data.append(row)

        calendar_table = Table(table_data,
                              colWidths=[cell_width] * 7,
                              rowHeights=[40] + [cell_height] * num_weeks)

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (6, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ALIGN', (0, 0), (6, 0), 'CENTER'),
            ('VALIGN', (0, 0), (6, 0), 'MIDDLE'),
            ('BACKGROUND', (5, 1), (6, -1), colors.HexColor('#f9f9f9')),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#052946')),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#7F1726')),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
        ])
        for col in range(7):
            table_style.add('LINEBEFORE', (col, 1), (col, -1), 0.5, colors.HexColor('#eeeeee'))

        calendar_table.setStyle(table_style)
        elements.append(calendar_table)
        elements.append(Spacer(1, 30))

        legend_style = ParagraphStyle(
            'LegendStyle',
            parent=styles['Normal'],
            fontName=regular_font,
            fontSize=10,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=5
        )
        legend_title = Paragraph("<b>Условные обозначения:</b>", legend_style)
        elements.append(legend_title)

        program_colors = [
            ('Профессиональная переподготовка', '#052946'),
            ('Повышение квалификации', '#2E7D32'),
            ('Семинар', '#7F1726'),
            ('Тренинг', '#FF9800'),
            ('Другое', '#6A1B9A'),
        ]

        legend_data = []
        for name, color in program_colors:
            color_cell = Table([[Paragraph('', legend_style)]],
                              colWidths=[20],
                              rowHeights=[15])
            color_cell.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor(color)),
                ('BOX', (0, 0), (0, 0), 1, colors.black),
            ]))
            text_cell = Paragraph(name, legend_style)
            legend_data.append([color_cell, text_cell])

        legend_table = Table(legend_data, colWidths=[25, 200])
        legend_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(legend_table)
        elements.append(Spacer(1, 20))

        if programs.exists():
            programs_title_style = ParagraphStyle(
                'ProgramsTitle',
                parent=styles['Heading2'],
                fontName=bold_font,
                fontSize=16,
                textColor=colors.HexColor('#052946'),
                spaceAfter=10
            )
            elements.append(Paragraph("Список программ на месяц:", programs_title_style))

            programs_data = []
            programs_header = ['Дата', 'Название программы', 'Тип', 'Формат']
            programs_data.append(programs_header)

            for program in programs:
                row = [
                    program.start_date.strftime('%d.%m.%Y'),
                    program.title[:50] + ('...' if len(program.title) > 50 else ''),
                    program.get_program_type_display(),
                    program.get_format_display()
                ]
                programs_data.append(row)

            programs_table = Table(programs_data,
                                 colWidths=[60, 200, 160, 80])
            programs_table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#052946')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), bold_font),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('ALIGN', (3, 1), (3, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('FONTNAME', (0, 1), (-1, -1), regular_font),
            ])
            programs_table.setStyle(programs_table_style)
            elements.append(programs_table)

        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontName=regular_font,
            fontSize=9,
            textColor=colors.gray,
            alignment=TA_CENTER,
            spaceBefore=20
        )
        footer_text = f"Сгенерировано: {datetime.now().strftime('%d.%m.%Y %H:%M')} | Расписание программ"
        elements.append(Paragraph(footer_text, footer_style))

        doc.build(elements)
        buffer.seek(0)
        filename = f"calendar_{month_names_ru[current_month-1].lower()}_{current_year}.pdf"
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        print(f"Ошибка при создании PDF: {e}")
        import traceback
        traceback.print_exc()
        return create_error_pdf(str(e))

def install_russian_fonts():
    """تثبيت وتسجيل الخطوط الروسية تلقائياً"""
    try:
        font_paths = [
            'C:/Windows/Fonts/arial.ttf',
            'C:/Windows/Fonts/times.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'fonts', 'DejaVuSans.ttf'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'fonts', 'arial.ttf'),
        ]
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font_name = os.path.basename(font_path).split('.')[0]
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    bold_path = font_path.replace('.ttf', '-Bold.ttf')
                    bold_path = bold_path.replace('arial.ttf', 'arialbd.ttf')
                    bold_path = bold_path.replace('times.ttf', 'timesbd.ttf')
                    if os.path.exists(bold_path):
                        pdfmetrics.registerFont(TTFont(font_name + '-Bold', bold_path))
                    else:
                        pdfmetrics.registerFont(TTFont(font_name + '-Bold', font_path))
                    print(f"تم تسجيل الخط الروسي: {font_name}")
                    return font_name
                except Exception as e:
                    print(f"خطأ في تسجيل الخط {font_path}: {e}")
                    continue
        print("محاولة تنزيل خط DejaVuSans...")
        try:
            return download_dejavu_fonts()
        except Exception as download_error:
            print(f"خطأ في تنزيل الخطوط: {download_error}")
            return 'Helvetica'
    except Exception as e:
        print(f"خطأ عام في تثبيت الخطوط: {e}")
        return 'Helvetica'

def download_dejavu_fonts():
    """تنزيل خط DejaVuSans من الإنترنت"""
    try:
        fonts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'fonts')
        os.makedirs(fonts_dir, exist_ok=True)
        dejavu_url = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
        temp_zip = os.path.join(tempfile.gettempdir(), 'dejavu_fonts.zip')
        print(f"جارٍ تنزيل DejaVuSans من {dejavu_url}...")
        urllib.request.urlretrieve(dejavu_url, temp_zip)
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith('.ttf'):
                    font_data = zip_ref.read(file_info.filename)
                    font_filename = os.path.basename(file_info.filename)
                    font_path = os.path.join(fonts_dir, font_filename)
                    with open(font_path, 'wb') as f:
                        f.write(font_data)
                    print(f"تم حفظ الخط: {font_filename}")
        os.remove(temp_zip)
        regular_path = os.path.join(fonts_dir, 'DejaVuSans.ttf')
        bold_path = os.path.join(fonts_dir, 'DejaVuSans-Bold.ttf')
        if os.path.exists(regular_path):
            pdfmetrics.registerFont(TTFont('DejaVuSans', regular_path))
            if os.path.exists(bold_path):
                pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', bold_path))
            else:
                pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', regular_path))
            print("تم تسجيل خط DejaVuSans بنجاح")
            return 'DejaVuSans'
        else:
            raise Exception("لم يتم العثور على ملفات الخط بعد التنزيل")
    except Exception as e:
        print(f"فشل تنزيل الخطوط: {e}")
        raise

def create_error_pdf(error_message):
    """إنشاء ملف PDF بسيط مع رسالة خطأ"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, "Ошибка при создании календаря PDF")
    p.setFont("Helvetica", 10)
    error_lines = []
    for i in range(0, len(error_message), 80):
        error_lines.append(error_message[i:i+80])
    y_position = 720
    for line in error_lines[:10]:
        p.drawString(100, y_position, line)
        y_position -= 15
    p.drawString(100, 650, "Попробуйте следующие решения:")
    p.drawString(120, 630, "1. Установите шрифт DejaVuSans в папку static/fonts/")
    p.drawString(120, 615, "2. Проверьте права доступа к файлам")
    p.drawString(120, 600, "3. Обратитесь к администратору системы")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="calendar_error.pdf")

def download_calendar_pdf_simple(request):
    """نسخة مبسطة من PDF للتقويم"""
    try:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=landscape(A4))
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        month_names = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
        width, height = landscape(A4)
        p.setFont("Helvetica-Bold", 24)
        p.setFillColor(colors.HexColor('#052946'))
        p.drawCentredString(width/2, height - 50, "Календарь программ")
        p.setFont("Helvetica-Bold", 20)
        p.setFillColor(colors.HexColor('#7F1726'))
        p.drawCentredString(width/2, height - 90, f"{month_names[current_month-1]} {current_year}")

        import calendar
        cal = calendar.monthcalendar(current_year, current_month)

        table_top = height - 150
        row_height = 50
        col_width = width / 7

        weekdays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']

        p.setFillColor(colors.HexColor('#f8f9fa'))
        p.rect(0, table_top - row_height, width, row_height, fill=1, stroke=0)
        p.setFillColor(colors.HexColor('#7F1726'))
        p.setFont("Helvetica-Bold", 16)
        for i, day in enumerate(weekdays):
            x = i * col_width + col_width/2
            p.drawCentredString(x, table_top - row_height + 20, day)

        programs = ScheduleProgram.objects.filter(
            is_active=True,
            start_date__year=current_year,
            start_date__month=current_month
        ).order_by('start_date')

        events_map = {}
        for program in programs:
            day = program.start_date.day
            if day not in events_map:
                events_map[day] = []
            events_map[day].append(program)

        p.setFont("Helvetica", 14)
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    x = day_num * col_width + col_width/2
                    y = table_top - (week_num + 1) * row_height + 25
                    if day_num >= 5:
                        p.setFillColor(colors.HexColor('#7F1726'))
                    else:
                        p.setFillColor(colors.black)
                    p.drawCentredString(x, y, str(day))
                    if day in events_map:
                        event_count = len(events_map[day])
                        p.setFont("Helvetica", 10)
                        p.setFillColor(colors.red)
                        p.drawCentredString(x, y - 15, f"({event_count})")
                        p.setFont("Helvetica", 14)

        p.setStrokeColor(colors.gray)
        p.setLineWidth(0.5)
        for i in range(8):
            y = table_top - i * row_height
            p.line(0, y, width, y)
        for i in range(8):
            x = i * col_width
            p.line(x, table_top - 7 * row_height, x, table_top)

        if programs.exists():
            list_top = table_top - 7 * row_height - 50
            p.setFont("Helvetica-Bold", 14)
            p.setFillColor(colors.HexColor('#052946'))
            p.drawString(50, list_top, "Список программ:")
            p.setFont("Helvetica", 10)
            p.setFillColor(colors.black)
            y_pos = list_top - 20
            for program in programs[:10]:
                if y_pos < 50:
                    break
                program_text = f"{program.start_date.strftime('%d.%m.%Y')} - {program.title[:40]}..."
                p.drawString(70, y_pos, program_text)
                y_pos -= 15

        p.setFont("Helvetica", 8)
        p.setFillColor(colors.gray)
        p.drawString(50, 30, f"Сгенерировано: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                           filename=f"calendar_{current_month}_{current_year}.pdf")
    except Exception as e:
        print(f"Ошибка в простой версии PDF: {e}")
        return create_error_pdf(str(e))