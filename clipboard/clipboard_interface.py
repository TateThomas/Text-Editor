from abc import ABC, abstractmethod

class ClipboardInterface(ABC):

    @abstractmethod
    def clipboard_get(self):
        pass

    @abstractmethod
    def clipboard_clear(self):
        pass

    @abstractmethod
    def clipboard_append(self, string):
        pass

    def clipboard_set(self, string):
        self.clipboard_clear()
        self.clipboard_append(string)
