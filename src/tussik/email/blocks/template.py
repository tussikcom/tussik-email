from enum import StrEnum
from typing import Optional, List


class BuildTemplate:
    __slots__ = ['template']

    def __init__(self, template: Optional[dict] = None):
        if isinstance(template, dict):
            self.template: dict = template
        else:
            self.template: dict = {}

    def __str__(self):
        if len(self.template) == 0:
            return "empty"
        return ", ".join(self.template.keys())

    def gettext(self, key: str, defval: Optional[str] = None) -> Optional[str]:
        data = self.template.get(key)
        if isinstance(data, str):
            return data
        return defval

    def getenum(self, key: str, options: StrEnum, defval: Optional[str] = None) -> Optional[str]:
        data = self.template.get(key)
        if isinstance(data, str):
            limited = [str(x) for x in options]
            if data in limited:
                return data
        return defval

    def getint(self, key: str, defval: Optional[int] = None) -> Optional[int]:
        data = self.template.get(key)
        if isinstance(data, int):
            return data
        return defval

    def getbool(self, key: str, defval: Optional[bool] = None) -> Optional[bool]:
        data = self.template.get(key)
        if isinstance(data, bool):
            return data
        return defval

    def getfloat(self, key: str, defval: Optional[float] = None) -> Optional[float]:
        data = self.template.get(key)
        if isinstance(data, float):
            return data
        return defval

    def get(self, key: str) -> "BuildTemplate":
        data = self.template.get(key)
        if isinstance(data, dict):
            return BuildTemplate(data)
        return BuildTemplate()

    def getlist(self, key: str) -> List["BuildTemplate"]:
        data = self.template.get(key)
        if isinstance(data, list):
            return [BuildTemplate(item) for item in data]
        return []
