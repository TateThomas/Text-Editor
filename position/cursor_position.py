from abc import ABC, abstractproperty
from interface.text_interface import TextInterface
from common_validation import CommonValidation

class CursorPosition(ABC):

    def __init__(self, text_interface):
        self.text_intrf = CommonValidation.validate_type(text_interface, TextInterface)

    @abstractproperty
    def first(self):
        try:
            first = self.text_intrf.get_selection_positions()[0]
        except:
            first = self.text_intrf.get_cursor_position()
        return first

    @abstractproperty
    def last(self):
        try:
            last = self.text_intrf.get_selection_positions()[1]
        except:
            last = self.text_intrf.get_cursor_position()
        return last
