from history.history import History, Edit
from interface.text_interface import TextInterface
from common_validation import CommonValidation

class EditHistory(History):

    def __init__(self, max_history=None, save_function=None):
        self.history = []
        self.current_edit = -1
        if max_history is not None:
            CommonValidation.validate_type(max_history, int)
        self.max_history = max_history
        if (save_function is not None) and not callable(save_function):
            raise TypeError("Save function must be a callable function")
        self.save = save_function
        self.last_save = self.current_edit
    
    def add_edit(self, edit):
        new_edit = CommonValidation.validate_type(edit, Edit)
        if len(self.history) > 0:
            del self.history[self.current_edit+1:]
        self.history.append(new_edit)
        if (self.max_history is not None) and (len(self.history) > self.max_history):
            amount_to_remove = len(self.history[:-self.max_history])
            del self.history[:amount_to_remove]
            self.current_edit -= amount_to_remove
            self.last_save -= amount_to_remove

    def commit_edit(self, text_interface):
        txt_intrf = CommonValidation.validate_type(text_interface, TextInterface)
        if self.current_edit < (len(self.history)-1):
            this_edit = self.history[self.current_edit+1]
            txt_intrf.insert_text(this_edit.new_text, this_edit.first, this_edit.last)
            self.current_edit += 1
            if self.current_edit == self.last_save:
                txt_intrf.denote_saved_changes()
            else:
                txt_intrf.denote_unsaved_changes()

    def undo_edit(self, text_interface):
        txt_intrf = CommonValidation.validate_type(text_interface, TextInterface)
        if self.current_edit > -1:
            this_edit = self.history[self.current_edit]
            txt_intrf.insert_text(this_edit.prev_text, this_edit.first, txt_intrf.get_position_after_string(this_edit.new_text, this_edit.first))
            txt_intrf.set_selection_positions(this_edit.first, this_edit.last)
            self.current_edit -= 1
            if self.current_edit == self.last_save:
                txt_intrf.denote_saved_changes()
            else:
                txt_intrf.denote_unsaved_changes()

    def save_edit(self, text_interface):
        if self.save is not None:
            self.save()
        self.last_save = self.current_edit
        CommonValidation.validate_type(text_interface, TextInterface).denote_saved_changes()
