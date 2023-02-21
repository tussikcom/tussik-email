import logging
from typing import Optional

from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildSubject(object):
    __slots__ = ['script']

    def __str__(self):
        return f"[subject] {self.script or 'None'}"

    def __init__(self, bt: BuildTemplate):
        self.script: Optional[str] = bt.gettext("script")

    def export(self) -> dict:
        return {'script': self.script}

    def render(self, context: BuildContext) -> str:
        return self.script or ""
