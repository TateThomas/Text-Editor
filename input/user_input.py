from abc import ABC, abstractmethod
from common_validation import CommonValidation
from position.cursor_position import CursorPosition
from interface.text_interface import TextInterface
from history.history import Edit

class UserInput(ABC):

    def __init__(self, text_interface, cursor_interface, symbol, new_text, action=None):
        self.text_intrf = CommonValidation.validate_type(text_interface, TextInterface)
        self.cursor_intrf = CommonValidation.validate_type(cursor_interface, CursorPosition)
        self.symbol = CommonValidation.validate_type(symbol, str)
        self.new_text = CommonValidation.validate_type(new_text, str)
        if action is not None:
            CommonValidation.validate_type(action, int)
        self.action = action

    @property
    def first(self):
        return self.cursor_intrf.first
    
    @property
    def last(self):
        return self.cursor_intrf.last

    @abstractmethod
    def create_edit(self, editor):
        return Edit(editor, self.symbol, self.first, self.last, self.new_text, self.text_intrf.get_text(self.first, self.last), self.action)
