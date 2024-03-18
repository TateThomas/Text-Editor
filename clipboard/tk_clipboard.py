from clipboard.clipboard_interface import ClipboardInterface
from common_validation import CommonValidation
import tkinter as tk

class TkClipboard(ClipboardInterface):

    def __init__(self, root):
        self.root = CommonValidation.validate_type(root, tk.Tk)

    def clipboard_get(self):
        return self.root.clipboard_get()

    def clipboard_clear(self):
        self.root.clipboard_clear()

    def clipboard_append(self, string):
        self.root.clipboard_append(string)
