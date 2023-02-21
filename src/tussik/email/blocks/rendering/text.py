import logging

from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.font import BuildFont
from tussik.email.blocks.render import BuildRender
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildText(BuildRender):
    typename = "text"

    def __init__(self, bt: BuildTemplate):
        super().__init__(bt)
        self.font: BuildFont = BuildFont(bt)
        self.script: str = bt.gettext("script", "")

    def export(self) -> dict:
        payload = {
            'script': self.script,
            'type': self.typename
        }
        self.font.merge(payload)
        return payload

    def render(self, context: BuildContext) -> str:
        return f"<p>{self.script}</p>"
