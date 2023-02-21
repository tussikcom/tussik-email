import logging
from typing import Optional

from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildForeach(object):
    __slots__ = ['alias', 'iterator', 'filter']

    def __str__(self):
        return f"[foreach] alias:{self.alias or 'None'} " \
               f"iterator:{self.iterator or 'None'}, " \
               f"filter:{self.filter or 'None'}"

    def __init__(self, bt: BuildTemplate):
        self.alias: Optional[str] = bt.gettext("foreach-alias")
        self.iterator: Optional[str] = bt.gettext("foreach-iterator")
        self.filter: Optional[str] = bt.gettext("foreach-filter")

    def merge(self, data: dict) -> None:
        data['foreach-alias'] = self.alias
        data['foreach-iterator'] = self.iterator
        data['foreach-filter'] = self.filter
