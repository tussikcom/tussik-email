import logging
from typing import Optional

from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildBorder(object):
    __slots__ = ['size', 'color']

    def __str__(self):
        return f"[border] " \
               f"size:{self.size or 'None'} " \
               f"color:{self.color or 'None'}"

    def __init__(self, bt: BuildTemplate):
        self.size: int = bt.getint("border-size", 0)
        self.color: Optional[str] = bt.gettext("border-color")

    def merge(self, data: dict) -> None:
        data['border-size'] = self.size
        data['border-color'] = self.color
