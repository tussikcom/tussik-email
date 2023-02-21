import logging
from typing import Optional

from tussik.email.blocks.context import BuildContext
from tussik.email.blocks.font import BuildFont
from tussik.email.blocks.render import BuildRender
from tussik.email.blocks.template import BuildTemplate

logger = logging.getLogger("tussik.email")


class BuildButtonStyleEnum:
    boxed = "boxed"
    rounded = "rounded"


class BuildButton(BuildRender):
    typename = "button"

    def __init__(self, bt: BuildTemplate):
        super().__init__(bt)
        self.bgcolor: Optional[str] = bt.gettext("bgcolor", "#1F7F4C")
        self.font: BuildFont = BuildFont(bt)
        self.text: Optional[str] = bt.gettext("text")
        self.url: Optional[str] = bt.gettext("url")
        self.style: str = BuildButtonStyleEnum.boxed

    def export(self) -> dict:
        payload = {
            'text': self.text,
            'url': self.url,
            'bgcolor': self.bgcolor
        }
        self.font.merge(payload)
        return payload

    def render(self, context: BuildContext) -> str:
        color = self.font.color or "#fffff"
        html = f"""
        <a rel="noopener" target="_blank" href="{self.url}"
           style="background-color: {self.bgcolor}; font-size: 18px; font-family: Helvetica, Arial, sans-serif; font-weight: bold; text-decoration: none; padding: 14px 20px; color: {color}; border-radius: 5px; display: inline-block; mso-padding-alt: 0;">
            <!--[if mso]>
            <i style="letter-spacing: 25px; mso-font-width: -100%; mso-text-raise: 30pt;">&nbsp;</i>
            <![endif]-->
            <span style="mso-text-raise: 15pt;">{self.text}</span>
            <!--[if mso]>
            <i style="letter-spacing: 25px; mso-font-width: -100%;">&nbsp;</i>
            <![endif]-->
        </a>
        """
        return html
