import abc
import logging

from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildRender(object):
    typename: str = ""

    def __str__(self):
        return f"[{self.typename}] ordinal:{self.ordinal}"

    def __init__(self, bt: BuildTemplate):
        self.tag: str = bt.gettext("tag", "").strip().lower()
        self.ordinal: int = bt.getint("ordinal", 0)

    @abc.abstractmethod
    def export(self) -> dict:
        raise Exception(f"{self.__class__.__name__}.export() MUST be implemented")

    @abc.abstractmethod
    def render(self, context: BuildContext) -> str:
        raise Exception(f"{self.__class__.__name__}.render() MUST be implemented")
