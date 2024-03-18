from interface.text_interface import TextInterface
from clipboard.clipboard_interface import ClipboardInterface
from history.history import History, Edit
from restrictions.restriction import Restriction
from common_validation import CommonValidation

class TextEditor:

    def __init__(self, text_interface, clipboard_interface, edit_history, *restrictions):

        self.txt_intrf = CommonValidation.validate_type(text_interface, TextInterface)
        self.txt_intrf.set_event_handler(self.event_handler)
        self.clipboard = CommonValidation.validate_type(clipboard_interface, ClipboardInterface)
        self.edit_hist = CommonValidation.validate_type(edit_history, History)
        self.restrictions = []
        for restriction in restrictions:
            self.add_restriction(restriction)

    def add_restriction(self, restriction):
        self.restrictions.append(CommonValidation.validate_type(restriction, Restriction))

    def get_restriction(self, arg):
        if isinstance(arg, int):
            if (arg >= 0) and (arg < len(self.restrictions)):
                return self.restrictions[arg]
            raise IndexError("Index is out of range")
        elif isinstance(arg, Restriction):
            if arg in self.restrictions:
                return self.restrictions[self.restrictions.index(arg)]
            raise ValueError("Given restriction is not currently apart of text editor restrictions")
        raise NotImplementedError("Other methods of retrieving a restriction from text editor restrictions have not been implemented")

    def delete_restriction(self, arg):
        try:
            self.get_restriction(arg)
            if isinstance(arg, int):
                del self.restrictions[arg]
            elif isinstance(arg, Restriction):
                self.restrictions.remove(arg)
        except:
            pass

    def event_handler(self, edit):
        CommonValidation.validate_type(edit, Edit)
        if edit.action is not None:
            match edit.action:
                case 0:     # copy
                    self.clipboard.clipboard_set(edit.prev_text)
                    return
                case 1:     # save
                    self.edit_hist.save_edit(self.txt_intrf)
                    return
                case 2:     # paste
                    edit.new_text = self.clipboard.clipboard_get()
                case 3:     # cut
                    self.clipboard.clipboard_set(edit.prev_text)
                case 4:     # redo
                    self.edit_hist.commit_edit(self.txt_intrf)
                    return
                case 5:     # undo
                    self.edit_hist.undo_edit(self.txt_intrf)
                    return
                case _:
                    raise ValueError("Invalid edit action")
        for restriction in self.restrictions:
            if not restriction.validate_string(edit.new_text):
                return
            new_lines = self.txt_intrf.get_lines_after_string_insert(edit.new_text, edit.first, edit.last)
            for line in new_lines:
                if not restriction.validate_line(line):
                    return
            if not restriction.validate_document(self.txt_intrf.get_all_text()):
                return
        self.edit_hist.add_edit(edit)
        self.edit_hist.commit_edit(self.txt_intrf)
        
