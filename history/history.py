from abc import ABC, abstractmethod

class History(ABC):

    @abstractmethod
    def add_edit(self, edit):
        pass

    @abstractmethod
    def commit_edit(self, text_interface):
        pass

    @abstractmethod
    def undo_edit(self, text_interface):
        pass

    @abstractmethod
    def save_edit(self, text_interface):
        pass

class Edit:

    action_codes = {
        "Copy": 0,
        "Save": 1,
        "Paste": 2,
        "Cut": 3,
        "Redo": 4,
        "Undo": 5
    }

    def __init__(self, editor, symbol, first, last, new_text, prev_text, action=None):
        self.editor = editor
        self.symbol = symbol
        self.first = first
        self.last = last
        self.new_text = new_text
        self.prev_text = prev_text
        self.action = action

    def __str__(self):
        return f"<Edit editor={self.editor} symbol={repr(self.symbol)} first={self.first} last={self.last} new_text={repr(self.new_text)} prev_text={repr(self.prev_text)} action={self.action})"
