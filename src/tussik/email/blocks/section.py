import logging
from typing import List, Optional

from tussik.email.blocks.border import BuildBorder
from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.foreach import BuildForeach
from tussik.email.blocks.segment import BuildSegment
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildSection:
    __slots__ = ['border', 'tag', 'ordinal', 'segments', 'hide', 'foreach']

    def __str__(self):
        return f"[section] ordinal:{self.ordinal} segments:{len(self.segments)}"

    def __init__(self, bt: BuildTemplate):
        self.border: BuildBorder = BuildBorder(bt)
        self.tag: str = bt.gettext("tag", "").strip().lower()
        self.ordinal: int = bt.getint('ordinal', 0)
        self.hide: Optional[str] = bt.gettext("hide")
        self.foreach: BuildForeach = BuildForeach(bt)

        segments = bt.getlist('segments')
        self.segments: List[BuildSegment] = []
        if isinstance(segments, list):
            for segment in segments:
                self.segments.append(BuildSegment(segment))

        self.segments = sorted(self.segments, key=lambda d: d.ordinal)
        for idx, segment in enumerate(self.segments, start=1):
            segment.ordinal = idx

    def export(self, preview: bool = False) -> dict:
        payload = {
            'tag': self.tag,
            'ordinal': self.ordinal,
            'segments': [segment.export() for segment in self.segments]
        }
        self.border.merge(payload)
        self.foreach.merge(payload)
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
        html = f"\t<table border=\"{bordersize}\" width=\"{context.width}\"><tr>\n"
        if context.debug:
            return f"\n<!-- SECTION ENTER {self.ordinal} -->\n" + html
        return html

    def render_exit(self, context: BuildContext) -> str:
        html = "\t</tr></table>\n"
        if context.debug:
            return html + f"<!-- SECTION EXIT {self.ordinal} -->\n"
        return html

    def render(self, context: BuildContext) -> str:
        if len(self.segments) == 0:
            return ""

        hide = context.evalbool(self.hide)
        if isinstance(hide, bool) and hide:
            return ""

        if isinstance(self.foreach.iterator, str) and isinstance(self.foreach.alias, str):

            html = ""
            index: int = -1

            while True:
                index += 1
                context.clearData(self.foreach.alias)
                context.setData("_index", index)
                script = f"{self.foreach.iterator}[{index}]"
                value = context.evalany(script)
                if value is None:
                    context.clearData("_index")
                    break
                context.setData(self.foreach.alias, value)

                keep = context.evalbool(self.foreach.filter)
                if isinstance(keep, bool) and not keep:
                    continue

                for segment in self.segments:
                    html += self.render_enter(context)
                    html += segment.render(context)
                    html += self.render_exit(context)

            context.clearData(self.foreach.alias)
            context.clearData("_index")
            return html

        # TODO: calculate column widths and render with adjustments
        html = ""
        for segment in self.segments:
            html += segment.render(context)
        return self.render_enter(context) + html + self.render_exit(context)
