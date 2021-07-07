from abc import ABC, abstractmethod
from typing import Union


class EntityResolver(ABC):
    """Represents a source of entity resolution data. Refer to https://glyphwiki.org/wiki/Group:CDP%e5%a4%96%e5%ad%97 as an example of what constitutes an entity."""

    @abstractmethod
    def resolve(self, entity_reference: str) -> Union[str, None]:
        """Returns the string (usually 1 char) that this entity refers to, None if unresolvable."""
        pass

    @abstractmethod
    def __init__(self, input_file_path):
        """
        :param input_file_path: Path to the raw file (usually a textful file such as JSON, CSV, TSV, etc)
        """
        pass
