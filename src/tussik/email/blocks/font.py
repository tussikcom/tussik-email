import logging
from typing import Optional

from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildFont(object):

    def __str__(self):
        return f"[font] name:{self.name or 'None'} size:{self.size or 'None'}"

    def __init__(self, bt: BuildTemplate):
        self.size: Optional[int] = bt.getint("font-size")
        self.name: str = bt.gettext("font-name", "")
        self.color: Optional[str] = bt.gettext("font-color")
        self.italics: Optional[bool] = bt.getbool("font-italics")
        self.bold: Optional[bool] = bt.getbool("font-bold")
        self.smallcap: Optional[bool] = bt.getbool("font-smallcap")

    def merge(self, data: dict) -> None:
        data['font-size'] = self.size
        data['font-name'] = self.name
