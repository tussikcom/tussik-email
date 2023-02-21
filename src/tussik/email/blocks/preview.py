import logging
from typing import Optional

from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildPreview:
    __slots__ = ['script']

    def __str__(self):
        return f"[preview] script:{self.script or 'None'}"

    def __init__(self, bt: BuildTemplate):
        self.script: Optional[str] = bt.gettext("script")

    def export(self) -> dict:
        return {'script': self.script}

    def render(self) -> str:
        if self.script is None:
            return ""
        html = f"""
        <div style="display:none; max-height: 0px; overflow: hidden">{self.script}</div>
        <div style="display: none; max-height: 0px; overflow: hidden;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
            &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
        </div>
        """
        return html
