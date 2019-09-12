import io
import re
import zipfile

from django.conf import settings
from django.core.files.storage import default_storage
from django.template import Context
from django.template.context import make_context
from django.template.exceptions import TemplateDoesNotExist
from pathlib import Path

from . import NEW_LINE_TAG, BOLD_START_TAG, BOLD_STOP_TAG
from .abstract import AbstractEngine, AbstractTemplate
from .utils import modify_libreoffice_doc, add_image_in_docx_template


class DocxTemplate(AbstractTemplate):
    """
    Handles docx templates.
    """

    def __init__(self, template, template_path=None):
        """
        :param template: the template to fill.
        :type template: django.template.Template

        :param template_path: path to the template.
        :type template_path: str
        """
        super().__init__(template)
        self.template_path = template_path

    def clean_bold_tag(self, data):
        nb_bold_tag = len(re.findall(BOLD_START_TAG, data))
        if nb_bold_tag > 0:
            for _ in range(nb_bold_tag):
                data = re.sub(
                    (
                        '<w:r><w:rPr>((<w:[^>]+>)*)</w:rPr><w:t>([^<]*){0}([^<]*){1}'
                        .format(BOLD_START_TAG, BOLD_STOP_TAG)),
                    (
                        '<w:r>'
                        + '<w:rPr>'
                        + '\\g<1>'
                        + '</w:rPr>'
                        + '<w:t>'
                        + '\\g<3>'
                        + '</w:t>'
                        + '</w:r>'
                        + '<w:r>'
                        + '<w:rPr>'
                        + '\\g<1>'
                        + '<w:b w:val="true"/>'
                        + '</w:rPr>'
                        + '<w:t>'
                        + '&#xA0;'
                        + '\\g<4>'
                        + '&#xA0;'
                        + '</w:t>'
                        + '</w:r>'
                        + '<w:r>'
                        + '<w:rPr>'
                        + '\\g<1>'
                        + '</w:rPr>'
                        + '<w:t>'
                    ),
                    data,
                )
        return data

    def clean_new_lines(self, data):
        nb_nl = len(re.findall(NEW_LINE_TAG, data))
        for _ in range(nb_nl):
            data = re.sub(
                '<w:t>([^<{0}]*){0}'.format(NEW_LINE_TAG),
                '<w:t>\\g<1></w:t><w:br/><w:t>',
                data,
            )
        return data

    def render(self, context=None, request=None):
        """
        Fills a docx template with the context obtained by combining the `context` and` request`
        parameters and returns a docx file as a byte object.
        """
        context = make_context(context, request)
        rendered = self.template.render(Context(context))
        rendered = self.clean(rendered)
        docx_content = modify_libreoffice_doc(self.template_path, 'word/document.xml', rendered)
        for _, image in context.get('images', {}).items():
            docx_content = add_image_in_docx_template(docx_content, image)
        return docx_content


class DocxEngine(AbstractEngine):
    """
    Docx template engine.

    ``app_dirname`` is equal to 'templates' but you can change this value by adding
    an ``DOCX_ENGINE_APP_DIRNAME`` setting in your settings.
    By default, ``sub_dirname`` is equal to 'docx' but you can change this value by adding
    an ``DOCX_ENGINE_SUB_DIRNAME`` setting in your settings.
    By default, ``DocxTemplate`` is used as template_class.
    """
    sub_dirname = getattr(settings, 'DOCX_ENGINE_SUB_DIRNAME', 'docx')
    app_dirname = getattr(settings, 'DOCX_ENGINE_APP_DIRNAME', 'templates')
    template_class = DocxTemplate
    mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    def get_template_content(self, filename):
        """
        Returns the contents of a template before modification, as a string.
        """
        template_buffer = io.BytesIO(
            default_storage.open(filename, 'rb').read())
        with zipfile.ZipFile(template_buffer, 'r') as zip_file:
            b_content = zip_file.read('word/document.xml')
        return b_content.decode()

    def get_template(self, template_name):
        template_path = self.get_template_path(template_name)
        content = self.get_template_content(template_path)
        return self.from_string(content, template_path=template_path)

    def check_mime_type(self, path):
        fmime_type = self.get_mimetype(path)
        suffix = Path(path).suffix

        if (fmime_type != self.mime_type) and (suffix not in [".docx", ".DOCX"] or fmime_type != "application/zip"):
            raise TemplateDoesNotExist('Bad template ({} != {}).'.format(fmime_type,
                                                                         self.mime_type))
