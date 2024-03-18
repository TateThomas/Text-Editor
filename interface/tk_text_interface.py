from interface.text_interface import TextInterface
from common_validation import CommonValidation
from position.position import Position
from interpreter.ascii_key_interpreter import AsciiKeyInterpreter
import tkinter as tk

class TkTextInterface(TextInterface):

    def __init__(self, root, text_box, denote_unsaved_changes=None, denote_saved_changes=None):
        super().__init__(AsciiKeyInterpreter(self))
        self.root = CommonValidation.validate_type(root, tk.Tk)
        self.text_box = CommonValidation.validate_type(text_box, tk.Text)

        if (denote_unsaved_changes is not None) and not callable(denote_unsaved_changes):
            raise TypeError("denote_unsaved_changes function must be a callable function")
        self.denote_unsaved = denote_unsaved_changes
        if (denote_saved_changes is not None) and not callable(denote_saved_changes):
            raise TypeError("denote_saved_changes function must be a callable function")
        self.denote_saved = denote_saved_changes

        self.text_box.bind("<Key>", TkTextInterface.break_on_input)
        self.text_box.bind("<KeyRelease>", self.event_listener)
    
    @staticmethod
    def event_to_state_bitmap(event):
        return event.state
    
    @staticmethod
    def keysym_num_to_ascii(keysym_num):
        if (keysym_num >= 32) and (keysym_num <= 126):
            return keysym_num
        if keysym_num == 65535:
            return 127
        if keysym_num >= 2**8:
            actual_val = keysym_num & (2**8 - 1)
            if actual_val == 13:
                return 10
            return actual_val

    @staticmethod
    def format_position(position):
        pos = CommonValidation.validate_type(position, Position)
        return f"{pos.line}.{pos.column}"

    @staticmethod
    def string_to_position(string):
        if CommonValidation.validate_type(string, str).replace(".", "").isnumeric():
            pos_list = string.split(".")
            if len(pos_list) == 2:
                return Position(int(pos_list[0]), int(pos_list[1]))
            raise ValueError("Invalid format to convert string to position (must be 'line.column', where line and column are numeric characters)")
        raise ValueError("String contains invalid characters (must be 'line.column', where line and column are numeric characters)")

    @staticmethod
    def break_on_input(event):
        if not event.keysym in ("Left", "Up", "Right", "Down"):
            return "break"
        else:
            return ""
 
    def event_listener(self, event):
        if ((event.keysym_num < 65505) or (event.keysym_num > 65518)) and not (event.keysym in ("Left", "Up", "Right", "Down")):
            super().event_listener(event)

    def event_to_identifier(self, event):
        return (TkTextInterface.keysym_num_to_ascii(event.keysym_num), TkTextInterface.event_to_state_bitmap(event))

    def get_text(self, first, last):
        return self.text_box.get(TkTextInterface.format_position(first), TkTextInterface.format_position(last))

    def get_all_text(self):
        return self.text_box.get(TkTextInterface.format_position(self.get_doc_start_position()), "end-1c")

    def get_line(self, line):
        return self.text_box.get(TkTextInterface.format_position(Position(line, 0)), TkTextInterface.format_position(Position(CommonValidation.validate_type(line, int)+1, 0)))[:-1]

    def get_lines_after_string_insert(self, string, first, last=None):
        return super().get_lines_after_string_insert(string, first, last)

    def get_doc_start_position(self):
        return Position(1, 0)
    
    def get_doc_end_position(self):
        all_text = self.get_all_text().split("\n")
        return Position(len(all_text), len(all_text[-1]))

    def get_cursor_position(self):
        return TkTextInterface.string_to_position(self.text_box.index(tk.INSERT))

    def get_line_start_position(self, line):
        return Position(line, 0)

    def get_line_end_position(self, line):
        return Position(line, len(self.get_line(line)))

    def get_previous_position(self, position):
        return super().get_previous_position(position)

    def get_next_position(self, position):
        return super().get_next_position(position)
    
    def get_position_after_string(self, string, start_pos=None):
        new_text_list = CommonValidation.validate_type(string, str).split("\n")
        added_lines = len(new_text_list) - 1
        if start_pos is not None:
            line_offset = CommonValidation.validate_type(start_pos, Position).line
            column_offset = start_pos.column if (added_lines == 0) else 0
        else:
            line_offset = 1
            column_offset = 0
        return Position(added_lines+line_offset, len(new_text_list[-1])+column_offset)

    def get_selection_positions(self):
        return (TkTextInterface.string_to_position(self.text_box.index(tk.SEL_FIRST)), TkTextInterface.string_to_position(self.text_box.index(tk.SEL_LAST)))

    def set_selection_positions(self, first, last):
        CommonValidation.validate_type(first, Position)
        CommonValidation.validate_type(last, Position)
        if (first >= self.get_doc_start_position()) and (last <= self.get_doc_end_position()):
            self.text_box.tag_add("sel", TkTextInterface.format_position(first), TkTextInterface.format_position(last))
        elif (first < self.get_doc_start_position()) and (last > self.get_doc_end_position()):
            raise IndexError("Both positions are outside document range")
        elif first < self.get_doc_start_position():
            raise IndexError(f"First position {first} is outside of document range (first position cannot be less than {self.get_doc_start_position()})")
        else:
            raise IndexError(f"Last position {last} is outside of document range (last position cannot be greater than {self.get_doc_end_position()})")

    def delete_text(self, first, last):
        self.text_box.delete(TkTextInterface.format_position(first), TkTextInterface.format_position(last))

    def insert_text(self, string, first, last=None):
        if last is not None:
            self.delete_text(first, last)
        self.text_box.insert(TkTextInterface.format_position(first), CommonValidation.validate_type(string, str))

    def denote_unsaved_changes(self):
        if self.denote_unsaved is not None:
            self.denote_unsaved()

    def denote_saved_changes(self):
        if self.denote_saved is not None:
            self.denote_saved()
