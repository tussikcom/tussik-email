import logging
from typing import Optional, Dict

from tussik.email.blocks.render import BuildRender
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildRenderRegistrar:
    def __init__(self):
        raise Exception()

    __registry: Dict[str, type] = {}

    @classmethod
    def add(cls, classtype: type):
        if issubclass(classtype, BuildRender):
            typename = str(classtype.typename).strip().lower()
            cls.__registry[typename] = classtype

    @classmethod
    def create(cls, bt: BuildTemplate) -> Optional[BuildRender]:
        typename = bt.gettext("type", "").strip().lower()
        if typename not in cls.__registry:
            return None
        classtype = cls.__registry[typename]
        return classtype(bt)
