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
        if preview:
            payload['preview'] = {
                "enter": cls.render_enter(),
                "body": item.render(),
                "exit": cls.render_exit()
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
        html = "\t\t\t\t" + item.render(context) + "\n"
        return cls.render_enter(item, context) + html + cls.render_exit(item, context)
