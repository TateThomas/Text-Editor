from abc import ABC, abstractmethod, abstractstaticmethod
from common_validation import CommonValidation
from position.position import Position

class TextInterface(ABC):

    def __init__(self, key_interpreter):
        self.key_interpreter = key_interpreter
        self.event_handler = None

    @staticmethod
    def get_state(state_bitmap, state):
        states = ("Shift", "Caps", "Control", "Alt")
        if CommonValidation.validate_type(state, str).capitalize() in states:
            return state_bitmap & 2**(states.index(state.capitalize()))
        raise ValueError(f"State '{state}' is not a valid state (must be one of the following: 'Shift', 'Caps', 'Control', 'Alt')")

    @abstractstaticmethod
    def event_to_state_bitmap(state):
        pass

    @abstractstaticmethod
    def format_position(position):
        pass

    @abstractmethod
    def event_listener(self, event):
        if self.event_handler is None:
            raise AttributeError("Text editor has not set up event handler with text interface yet")
        try:
            user_input = self.key_interpreter.interpret(self.event_to_identifier(event))
            self.event_handler(user_input.create_edit("user"))
        except NotImplementedError:
            pass

    @abstractmethod
    def event_to_identifier(self, event):
        pass

    @abstractmethod
    def get_text(self, first, last):
        pass

    @abstractmethod
    def get_all_text(self):
        pass

    @abstractmethod
    def get_line(self, line):
        pass

    @abstractmethod
    def get_lines_after_string_insert(self, string, first, last=None):
        insert_text = CommonValidation.validate_type(string, str)
        first_pos = CommonValidation.validate_type(first, Position)
        if last is not None:
            last_pos = CommonValidation.validate_type(last, Position)
        else:
            last_pos = first_pos
        start_line = self.get_text(self.get_line_start_position(first.line), first)
        end_line = self.get_text(last_pos, self.get_line_end_position(last_pos.line))
        if len(insert_text) > 0:
            lines = insert_text.split("\n")
            lines[0] = start_line + lines[0]
            lines[-1] += end_line
        else:
            lines = [start_line + end_line]
        return lines
    
    @abstractmethod
    def get_doc_start_position(self):
        pass

    @abstractmethod
    def get_doc_end_position(self):
        pass

    @abstractmethod
    def get_cursor_position(self):
        pass

    @abstractmethod
    def get_line_start_position(self, line):
        pass

    @abstractmethod
    def get_line_end_position(self, line):
        pass

    @abstractmethod
    def get_previous_position(self, position):
        if CommonValidation.validate_type(position, Position) > self.get_line_start_position(position.line):
            return Position(position.line, position.column-1)
        if position.line > self.get_first_line():
            return self.get_line_end_position(position.line-1)
        return position

    @abstractmethod
    def get_next_position(self, position):
        if CommonValidation.validate_type(position, Position) < self.get_line_end_position(position.line):
            return Position(position.line, position.column+1)
        return self.get_line_start_position(position.line+1)
    
    @abstractmethod
    def get_position_after_string(self, string, start_pos=None):
        pass

    @abstractmethod
    def get_selection_positions(self):
        pass

    @abstractmethod
    def set_selection_positions(self, first, last):
        pass

    @abstractmethod
    def insert_text(self, string, first, last=None):
        pass

    @abstractmethod
    def delete_text(self, first, last):
        pass

    @abstractmethod
    def denote_unsaved_changes(self):
        pass

    @abstractmethod
    def denote_saved_changes(self):
        pass

    def set_event_handler(self, event_handler):
        if (event_handler is not None) and not callable(event_handler):
            raise TypeError("denote_unsaved_changes function must be a callable function")
        self.event_handler = event_handler
