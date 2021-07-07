from abc import ABC, abstractmethod


class BaseSource(ABC):
    """Represents a source of IDS data."""

    @abstractmethod
    def get_valid_ids(self, char) -> list[str]:
        """Return all the decompositions of this character which are considered to be valid."""
        pass

    @abstractmethod
    def get_all_ids(self, char) -> list[str]:
        """Return all the decompositions of this character, which may include placeholders and entity references."""
        pass

    @abstractmethod
    def __init__(self, input_file_path):
        """
        :param input_file_path: Path to the raw file (usually a textual file such as JSON, CSV, TSV, etc)
        """
        pass
