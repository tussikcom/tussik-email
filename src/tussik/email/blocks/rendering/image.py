import logging
from typing import Optional

from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.render import BuildRender
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildImage(BuildRender):
    typename = "image"

    def __init__(self, bt: BuildTemplate):
        super().__init__(bt)
        self.url: str = bt.gettext("url", "#")
        self.alt: Optional[str] = bt.gettext("alt")
        self.embedded: bool = bt.getbool("embedded", False)  # base64 include the image

    def export(self) -> dict:
        payload = {
            'url': self.url,
            'alt': self.alt,
            'embedded': self.embedded,
        }
        return payload

    def render(self, context: BuildContext) -> str:
        return "<image/>"
