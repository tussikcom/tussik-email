import logging
from typing import List, Optional

from tussik.email.blocks.border import BuildBorder
from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.registrar import BuildRenderRegistrar
from tussik.email.blocks.render import BuildRender
from tussik.email.blocks.renderwrapper import BuildRenderWrapper
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildSegment:

    __slots__ = ['border', 'tag', 'ordinal', 'hide', 'renders']

    def __str__(self):
        return f"[segment] ordinal:{self.ordinal} renders:{len(self.renders)}"

    def __init__(self, bt: BuildTemplate):
        self.border: BuildBorder = BuildBorder(bt)
        self.tag: str = str(bt.get('tag') or "").strip().lower()
        self.ordinal: int = bt.getint('ordinal', 0)
        self.hide: Optional[str] = bt.gettext("hide")

        renders = bt.getlist('renders')
        self.renders: List[BuildRender] = []
        if isinstance(renders, list):
            for render in renders:
                item = BuildRenderRegistrar.create(render)
                if isinstance(item, BuildRender):
                    self.renders.append(item)

        self.renders = sorted(self.renders, key=lambda d: d.ordinal)
        for idx, render in enumerate(self.renders, start=1):
            render.ordinal = idx

    def export(self, preview: bool = False) -> dict:
        payload = {
            'tag': self.tag,
            'ordinal': self.ordinal,
            'renders': [BuildRenderWrapper.export(render, preview) for render in self.renders]
        }
        self.border.merge(payload)
        if preview:
            context = BuildContext()
            payload['preview'] = {
                "enter": self.render_enter(context),
                "body": None,
                "exit": self.render_exit(context),
            }
        return payload

    def render_enter(self, context: BuildContext) -> str:
        bordersize = 1 if context.debug else self.border.size
        html = f"\t\t<td><table border=\"{bordersize}\"><tr><td>\n"
        if context.debug:
            return f"\n\t<!-- SEGMENT ENTER {self.ordinal} -->\n" + html
        return html

    def render_exit(self, context: BuildContext) -> str:
        html = "\t\t</td></tr></table></td>\n"
        if context.debug:
            return html + f"\t<!-- SEGMENT EXIT {self.ordinal} -->\n"
        return html

    def render(self, context: BuildContext) -> str:
        html = ""

        hide = context.evalbool(self.hide)
        if isinstance(hide, bool) and hide:
            return ""

        # TODO: calculate column widths and render with adjustments
        for render in self.renders:
            html += BuildRenderWrapper.render(render, context)
        return self.render_enter(context) + html + self.render_exit(context)
