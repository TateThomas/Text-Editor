from input.user_input import UserInput
from history.history import Edit
from position.positioning import RegularPositioning, LinePositioning, BackPositioning

class Character(UserInput):

    def __init__(self, text_interface, symbol, cursor_interface=None):
        if cursor_interface is None:
            cursor_interface = RegularPositioning(text_interface)
        super().__init__(text_interface, cursor_interface, symbol, symbol)
    
    def create_edit(self, editor):
        return super().create_edit(editor)
    
class Remover(UserInput):

    def __init__(self, text_interface, symbol, cursor_interface=None):
        if cursor_interface is None:
            cursor_interface = BackPositioning(text_interface)
        super().__init__(text_interface, cursor_interface, symbol, "")
    
    def create_edit(self, editor):
        return super().create_edit(editor)

class Shortcut(UserInput):

    def __init__(self, text_interface, symbol, cursor_interface=None):
        if cursor_interface is None:
            cursor_interface = LinePositioning(text_interface)
        if not symbol in Edit.action_codes:
            raise ValueError("Shortcut symbol must be associated with a defined shortcut action")
        super().__init__(text_interface, cursor_interface, symbol, "", Edit.action_codes[symbol])

    def create_edit(self, editor):
        return super().create_edit(editor)
