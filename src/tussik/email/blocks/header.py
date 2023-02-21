import logging
from typing import Optional

from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildHeader:

    def __str__(self):
        return f"[header] {self.name}: {self.script or 'None'}"

    def __init__(self, bt: BuildTemplate):
        self.name: str = bt.gettext('name', "").strip().upper()
        self.script: Optional[str] = bt.gettext("script")

    def export(self) -> dict:
        return {'name': self.name, 'script': self.script}

    def render(self) -> Optional[str]:
        return self.script
