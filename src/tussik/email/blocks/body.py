import logging
from typing import List, Optional

from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.fontfamily import BuildFontFamily
from tussik.email.blocks.footer import BuildFooter
from tussik.email.blocks.header import BuildHeader
from tussik.email.blocks.page import BuildPage
from tussik.email.blocks.preview import BuildPreview
from tussik.email.blocks.registrar import BuildRenderRegistrar
from tussik.email.blocks.rendering.button import BuildButton
from tussik.email.blocks.rendering.image import BuildImage
from tussik.email.blocks.rendering.text import BuildText
from tussik.email.blocks.section import BuildSection
from tussik.email.blocks.subject import BuildSubject
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")

#
# self register all the included render classes
#
BuildRenderRegistrar.add(BuildText)
BuildRenderRegistrar.add(BuildButton)
BuildRenderRegistrar.add(BuildImage)


class BuildBody(object):
    __slots__ = ['page', 'preview', 'subject', 'headers', 'sections', 'fonts', 'footer']

    def __str__(self):
        return f"headers({len(self.headers)}), " \
               f"sections({len(self.sections)}), " \
               f"fonts({len(self.fonts)})"

    def __init__(self, template: Optional[dict] = None):
        bt = BuildTemplate(template)
        self.page: BuildPage = BuildPage(bt.get("page"))
        self.preview: BuildPreview = BuildPreview(bt.get("preview"))
        self.subject: BuildSubject = BuildSubject(bt.get("subject"))
        self.footer: BuildFooter = BuildFooter(bt.get("footer"))

        headers = bt.getlist('headers')
        self.headers: List[BuildHeader] = []
        if isinstance(headers, list):
            for header in headers:
                self.headers.append(BuildHeader(header))

        fonts = bt.getlist('fonts')
        self.fonts: List[BuildFontFamily] = []
        if isinstance(fonts, list):
            for font in fonts:
                self.fonts.append(BuildFontFamily(font))

        sections = bt.getlist('sections')
        self.sections: List[BuildSection] = []
        if isinstance(sections, list):
            for section in sections:
                self.sections.append(BuildSection(section))

        self.sections = sorted(self.sections, key=lambda d: d.ordinal)
        for idx, section in enumerate(self.sections, start=1):
            section.ordinal = idx

    def export(self, preview: bool) -> dict:
        payload = {
            'page': self.page.export(),
            'footer': self.footer.export(preview),
            'preview': self.page.export(),
            'fonts': [font.export() for font in self.fonts],
            'sections': [section.export(preview) for section in self.sections],
        }
        if preview:
            context = BuildContext()
            payload['preview'] = {
                "enter": self.render_enter(context) + self.page.render_enter(context),
                "body": None,
                "exit": self.page.render_exit(context) + self.render_exit(context),
            }
        return payload

    def render_enter(self, context: BuildContext) -> str:
        html = ""
        if len(self.fonts) > 0:
            fonts = " ".join([f.render() for f in self.fonts])
            html = f"<head><style>body {{  {fonts}  }}</style></head>\n"

        if len(self.page.bgcolor) > 0:
            html += "<body bgcolor=\"#D3D3D3\" style=\"background-color: #D3D3D3;\">\n"
        else:
            html += "<body>\n"
        return html

    def render_exit(self, context: BuildContext) -> str:
        return "</body></html>\n"

    def render(self, context: BuildContext) -> str:
        context.width = self.page.width
        html = ""
        for section in self.sections:
            html += section.render(context)
        footer = self.footer.render(context)
        html_enter = self.render_enter(context) + self.page.render_enter(context)
        html_exit = self.page.render_exit(context) + footer + self.render_exit(context)
        return html_enter + html + html_exit
