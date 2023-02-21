from typing import Dict, Union, Optional


class BuildContext:
    __slots__ = ['_values', 'debug', 'width']

    def __init__(self):
        self.debug: bool = False
        self.width: Optional[int] = None
        self._values: Dict[str, Union[str, int, float, bool]] = {}

    def getValue(self, key: str, defval: Union[str, int, float, bool] = None) -> Union[str, int, float, bool]:
        value = self._values.get(key)
        if value is None:
            return defval
        return value

    def setValue(self, key: str, value: Union[str, int, float, bool]):
        self._values[key] = value
