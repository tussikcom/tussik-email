import logging

from tussik.email.blocks.border import BuildBorder
from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.font import BuildFont
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildPage:

    def __str__(self):
        return f"[page] width:{self.width or 'None'}"

    def __init__(self, bt: BuildTemplate):
        self.width: int = bt.getint("width", 600)
        self.bgcolor: str = bt.gettext("bgcolor", "#FFFFFF")
        self.border: BuildBorder = BuildBorder(bt)
        self.font: BuildFont = BuildFont(bt)

    def export(self) -> dict:
        payload = {
            'width': self.width,
            'bgcolor': self.bgcolor,
        }
        self.border.merge(payload)
        self.font.merge(payload)
        return payload

    def render_enter(self, context: BuildContext) -> str:
        html = f"""
        <table width="{self.width}" cellspacing="0" cellpadding="2" align="center" bgcolor="{self.bgcolor}" style="background-color: {self.bgcolor}">
        <tr><td align=\"center\">\n
        """
        if context.debug:
            return f"\n<!-- PAGE ENTER -->\n" + html
        return html

    def render_exit(self, context: BuildContext) -> str:
        html = "</td></tr></table>\n"
        if context.debug:
            return html + f"<!-- PAGE EXIT -->\n"
        return html
