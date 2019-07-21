from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
import io
from django.http import FileResponse, HttpResponse
import docx
from docx import Document
from docx import RT
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.dml import MSO_THEME_COLOR_INDEX
from datetime import datetime

from .models import Article
from .forms import AddingForm
from .themes import THEME_CHOICES


class AddArticle(CreateView):
    model = Article
    template_name = 'article/add_article.html'
    form_class = AddingForm
    success_url = 'add_article'

    def get_success_url(self):
        return reverse(self.success_url)


class GetArticles(ListView):
    model = Article
    template_name = 'article/get_article.html'
    success_url = 'get_article'

    def get_success_url(self):
        return reverse(self.success_url)


def add_head(paragraph, article):
    add_hyperlink(paragraph, article.article_url, 'Link', '0000FF', True)
    r = paragraph.add_run(" {0}".format(article.description))


def add_hyperlink(paragraph, url, text, color, underline):
    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
    hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )

    # Create a w:r element
    new_run = docx.oxml.shared.OxmlElement('w:r')

    # Create a new w:rPr element
    rPr = docx.oxml.shared.OxmlElement('w:rPr')

    # Add color if it is given
    if not color is None:
      c = docx.oxml.shared.OxmlElement('w:color')
      c.set(docx.oxml.shared.qn('w:val'), color)
      rPr.append(c)

    # Remove underlining if it is requested
    if not underline:
      u = docx.oxml.shared.OxmlElement('w:u')
      u.set(docx.oxml.shared.qn('w:val'), 'none')
      rPr.append(u)

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    paragraph._p.append(hyperlink)

    return hyperlink


def add_toc(paragraph):
    run = paragraph.add_run()
    fldChar = OxmlElement('w:fldChar')  # creates a new element
    fldChar.set(qn('w:fldCharType'), 'begin')  # sets attribute on element
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')  # sets attribute on element
    instrText.text = 'TOC \\o "1-2" \\h \\z \\u'  # change 123 depending on heading levels you need

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:t')
    fldChar3.text = "Right-click to update field."
    fldChar2.append(fldChar3)

    fldChar4 = OxmlElement('w:fldChar')
    fldChar4.set(qn('w:fldCharType'), 'end')

    r_element = run._r
    run._r.append(fldChar)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar4)
    p_element = paragraph._p


def get_docx(request):
    document = Document()
    start_date = datetime.strptime(str(request.GET.get("start")), "%Y-%m-%d")
    end_date = datetime.strptime(str(request.GET.get("end")), "%Y-%m-%d")

    all_articles = Article.objects.all().filter(created_at__range=(start_date, end_date))
    articles = dict()
    for theme_choice in THEME_CHOICES:
        articles[theme_choice[1]] = all_articles.all().filter(theme=theme_choice[0])

    document.add_paragraph('Table of Contents', style='TOCHeading')
    paragraph = document.add_paragraph()
    add_toc(paragraph)

    document.add_page_break()

    for theme in articles.keys():
        document.add_heading(theme, level=1)
        for article in articles[theme]:
            document.add_heading(article.title, level=2)

            p = document.add_paragraph()
            add_head(p, article)

            p = document.add_paragraph(article.abstract)

            if (article.keywords):
                p = document.add_paragraph(article.keywords)

            document.add_page_break()

    # document.add_heading('Document Title', 0)
    #
    # p = document.add_paragraph('A plain paragraph having some ')
    # p.add_run('bold').bold = True
    # p.add_run(' and some ')
    # p.add_run('italic.').italic = True
    #
    # document.add_heading('Heading, level 1', level=1)
    #
    # document.add_paragraph(
    #     'first item in unordered list', style='ListBullet'
    # )
    # document.add_paragraph(
    #     'first item in ordered list', style='ListNumber'
    # )
    #
    # # document.add_picture('monty-truth.png', width=Inches(1.25))
    #
    # table = document.add_table(rows=1, cols=3)
    # hdr_cells = table.rows[0].cells
    # hdr_cells[0].text = 'Qty'
    # hdr_cells[1].text = 'Id'
    # hdr_cells[2].text = 'Desc'
    # for item in [0,1]:
    #     row_cells = table.add_row().cells
    #     row_cells[0].text = "lol"
    #     row_cells[1].text = "kek"
    #     row_cells[2].text = "cheburek"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    document.save(response)

    return response
