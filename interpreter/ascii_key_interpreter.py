from interpreter.input_interpreter import InputInterpreter
from input.inputs import Character, Remover, Shortcut
from position.positioning import RegularPositioning, BackPositioning, NextPositioning
from interface.text_interface import TextInterface
from common_validation import CommonValidation

class AsciiKeyInterpreter(InputInterpreter):

    def __init__(self, text_interface):
        self.txt_intrf = CommonValidation.validate_type(text_interface, TextInterface)

    def interpret(self, identifier):
        ascii_code = CommonValidation.validate_type(identifier[0], int)
        state_bitmap = CommonValidation.validate_type(identifier[1], int)
        if (ascii_code < 0) or (ascii_code > 255):
            raise ValueError(f"Identifier not in range of possible ASCII codes 0-255 ({identifier} was given)")
        match ascii_code:
            case 8:     # backspace
                return Remover(self.txt_intrf, "Backspace")
            case 9:     # tab
                return Character(self.txt_intrf, "\t")
            case 10:    # line feed
                return Character(self.txt_intrf, "\n")
            case 12:    # form feed
                return Character(self.txt_intrf, "\f")
            case 13:    # carriage return
                return Character(self.txt_intrf, "\r")
            case _ if TextInterface.get_state(state_bitmap, "Control") and (ascii_code == 99):  # Ctrl + c / copy
                return Shortcut(self.txt_intrf, "Copy")
            case _ if TextInterface.get_state(state_bitmap, "Control") and (ascii_code == 115):  # Ctrl + s / save
                return Shortcut(self.txt_intrf, "Save")
            case _ if TextInterface.get_state(state_bitmap, "Control") and (ascii_code == 118):  # Ctrl + v / paste
                return Shortcut(self.txt_intrf, "Paste", RegularPositioning(self.txt_intrf))
            case _ if TextInterface.get_state(state_bitmap, "Control") and (ascii_code == 120):  # Ctrl + x / cut
                return Shortcut(self.txt_intrf, "Cut")
            case _ if TextInterface.get_state(state_bitmap, "Control") and (ascii_code == 121):  # Ctrl + y / redo
                return Shortcut(self.txt_intrf, "Redo")
            case _ if TextInterface.get_state(state_bitmap, "Control") and (ascii_code == 122):  # Ctrl + z / undo
                return Shortcut(self.txt_intrf, "Undo")
            case _ if ascii_code in range(32, 126):
                return Character(self.txt_intrf, chr(ascii_code))
            case 127:   # delete
                return Remover(self.txt_intrf, "Delete", NextPositioning(self.txt_intrf))
        raise NotImplementedError(f"ASCII code {ascii_code} not currently supported as a valid input")
    