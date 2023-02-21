import logging
from typing import Optional

from tussik.email.blocks.alignment import BuildVAlignEnum, BuildHAlignEnum
from tussik.email.blocks.border import BuildBorder
from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildFooter:

    def __str__(self):
        return f"[footer] width:{self.width or 'None'}"

    def __init__(self, bt: BuildTemplate):
        self.script: Optional[str] = bt.gettext('script')
        self.width: Optional[int] = bt.getint("width")
        self.border: BuildBorder = BuildBorder(bt)
        self.height: Optional[int] = bt.getint("height")
        self.bgcolor: Optional[str] = bt.gettext("bgcolor")
        self.halign: Optional[str] = bt.getenum("halign", BuildHAlignEnum, str(BuildHAlignEnum.center))

    def export(self, preview: bool) -> dict:
        payload = {
            'script': self.script,
            'width': self.width,
            'height': self.height,
            'bgcolor': self.bgcolor,
            'halign': self.halign,
        }
        self.border.merge(payload)
        if preview:
            context = BuildContext()
            payload['preview'] = {
                "enter": self.render_enter(context),
                "body": self.render_body(context),
                "exit": self.render_exit(context),
            }
        return payload

    def render_enter(self, context: BuildContext) -> str:
        bordersize = 1 if context.debug else self.border.size
        width = context.width if self.width is None else self.width
        html = f"<table width=\"{width}\" border=\"{bordersize}\"><tr><td align=\"{self.halign}\">\n"
        if context.debug:
            return f"\n<!-- FOOTER ENTER -->\n" + html
        return html

    def render_exit(self, context: BuildContext) -> str:
        html = "\n</td></tr></table>\n"
        if context.debug:
            return html + f"<!-- FOOTER EXIT -->\n"
        return html

    def render_body(self, context: BuildContext) -> Optional[str]:
        if self.script is None:
            return None
        html = self.script
        return html

    def render(self, context: BuildContext) -> str:
        html = self.render_body(context)
        if html is None:
            return ""
        return self.render_enter(context) + html + self.render_exit(context)
