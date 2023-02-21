import ast
import logging
from typing import Dict, Union, Optional, Any

from jinja2.sandbox import SandboxedEnvironment

logger = logging.getLogger("tussik.email")


class BuildContext:
    __slots__ = ['_values', 'debug', 'width', '_data', '_env']

    def __init__(self, **kwargs):
        self.debug: bool = False
        self.width: Optional[int] = None
        self._values: Dict[str, Union[str, int, float, bool]] = {}
        self._data: Dict[str, Any] = {}
        for k, v in kwargs.items():
            self._data[k] = v
        self._env = SandboxedEnvironment()

    def getData(self, key: str, defval: Any) -> Any:
        value = self._data.get(key)
        if value is None:
            return defval
        return value

    def setData(self, key: str, value: Any):
        self._data[key] = value

    def getValue(self, key: str, defval: Union[str, int, float, bool] = None) -> Union[str, int, float, bool]:
        value = self._values.get(key)
        if value is None:
            return defval
        return value

    def setValue(self, key: str, value: Union[str, int, float, bool]):
        self._values[key] = value

    def eval(self, template: Optional[str] = None) -> str:
        try:
            if not isinstance(template, str):
                return ""
            tmp = self._env.from_string(template)
            value = str(tmp.render(**self._data)).strip()
            return value
        except Exception as e:
            logger.error(f"failed to process script")
        return ""

    def evalbool(self, template: Optional[str] = None) -> Optional[bool]:
        try:
            if not isinstance(template, str):
                return None
            tmp = self._env.from_string(template)
            value = str(tmp.render(**self._data)).strip()
            result = ast.literal_eval(value)
            if isinstance(result, bool):
                return result
            return None
        except Exception as e:
            logger.error(f"failed to process script")
        return None

    def evalint(self, template: Optional[str] = None) -> Optional[int]:
        try:
            if not isinstance(template, str):
                return None
            tmp = self._env.from_string(template)
            value = str(tmp.render(**self._data)).strip()
            result = ast.literal_eval(value)
            if isinstance(result, int):
                return result
            return None
        except Exception as e:
            logger.error(f"failed to process script")
        return None
