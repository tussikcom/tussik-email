import json
import logging
from enum import Enum
from typing import Union, Optional

from tussik.email import Emailer
from tussik.email.blocks.body import BuildBody
from tussik.email.blocks.context import BuildContext

logger = logging.getLogger("tussik.email")

try:
    import yaml
except:
    yaml = None


class EmailTemplateFormatEnum(Enum):
    json = "json"
    yaml = "yaml"
    dict = "dict"


class EmailBuilder:
    def __init__(self):
        self._body: Optional[BuildBody] = None

    @property
    def body(self) -> Optional[BuildBody]:
        return self._body

    def load(self, template: Union[str, dict], format: EmailTemplateFormatEnum = EmailTemplateFormatEnum.dict) -> bool:
        try:
            if format == EmailTemplateFormatEnum.json:
                value = json.loads(template)
                self._body = BuildBody(value)
                return True
            elif format == EmailTemplateFormatEnum.yaml:
                value = yaml.safe_load(template)
                self._body = BuildBody(value)
                return True
            elif format == EmailTemplateFormatEnum.dict:
                self._body = BuildBody(template)
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"failed to load {format.value}: {str(e.args)}")
            return False

    def export(self, format: EmailTemplateFormatEnum = EmailTemplateFormatEnum.dict) -> Union[str, dict, None]:
        if self._body is None:
            return None
        template = self._body.export(False)
        if format == EmailTemplateFormatEnum.json:
            return json.dumps(template, indent=4)
        elif format == EmailTemplateFormatEnum.yaml:
            return yaml.safe_dump(template)
        else:
            return template

    def preview(self) -> Optional[dict]:
        if self._body is None:
            return None
        return self._body.export(True)

    def render(self, debug: bool = False) -> Optional[str]:
        if self._body is None:
            return None
        context = BuildContext()
        context.debug = debug
        return self._body.render(context)

    def update(self, msg: Emailer) -> bool:
        if self._body is None:
            return False
        context = BuildContext()
        msg.subject = self._body.subject.render(context)
        msg.html = self._body.render(context)

        for header in self._body.headers:
            name = header.name
            value = header.render()
            if isinstance(value, str) and len(value) > 0 and len(name) > 0:
                msg.header(header.name, value)

        return False
