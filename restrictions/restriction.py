from abc import ABC, abstractmethod

class Restriction(ABC):

    @abstractmethod
    def validate_string(self, string):
        pass

    @abstractmethod
    def validate_line(self, line):
        pass

    @abstractmethod
    def validate_document(self, text):
        pass
