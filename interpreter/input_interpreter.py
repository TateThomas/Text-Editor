from abc import ABC, abstractmethod

class InputInterpreter(ABC):

    @abstractmethod
    def interpret(self, identifier):
        pass
