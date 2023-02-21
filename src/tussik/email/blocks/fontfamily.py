import logging

from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildFontFamily:

    def __str__(self):
        return f"[fontfamily] name:{self.name or 'None'}"

    def __init__(self, bt: BuildTemplate):
        # TODO: is this a download? embedded? referenced?
        self.name: str = bt.gettext("name", "")

    def export(self) -> dict:
        return {'name': self.name}

    def render(self) -> str:
        if len(self.name) == 0:
            return ""
        return f"font-family: {self.name}; "
