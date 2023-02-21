import logging

from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.render import BuildRender

logger = logging.getLogger("tussik.email")


class BuildRenderWrapper(object):

    @classmethod
    def export(cls, item: BuildRender, preview: bool) -> dict:
        payload = item.export()
        payload['type'] = item.__class__.typename
        payload['tag'] = item.tag
        payload['ordinal'] = item.ordinal
        payload['hide'] = item.hide
        if preview:
            context = BuildContext()
            payload['preview'] = {
                "enter": cls.render_enter(item, context),
                "body": item.render(context),
                "exit": cls.render_exit(item, context)
            }
        return payload

    @classmethod
    def render_enter(self, item: BuildRender, context: BuildContext) -> str:
        html = "\t\t\t<table><tr><td>\n"
        if context.debug:
            return f"\n\t\t<!-- {item.typename.upper()} ENTER {item.ordinal} -->\n" + html
        return html

    @classmethod
    def render_exit(self, item: BuildRender, context: BuildContext) -> str:
        html = "\t\t\t</td></tr></table>\n"
        if context.debug:
            return html + f"\n\t\t<!-- {item.typename.upper()} EXIT {item.ordinal} -->\n"
        return html

    @classmethod
    def render(cls, item: BuildRender, context: BuildContext) -> str:
        hide = context.evalbool(item.hide)
        if isinstance(hide, bool) and hide:
            return ""

        html = "\t\t\t\t" + item.render(context) + "\n"
        return cls.render_enter(item, context) + html + cls.render_exit(item, context)
