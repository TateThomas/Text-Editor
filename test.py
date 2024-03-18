import tkinter as tk
from text_editor import TextEditor
from interface.tk_text_interface import TkTextInterface
from clipboard.tk_clipboard import TkClipboard
from history.edit_history import EditHistory
from restrictions.regex_restrict import RegexRestrict

def main():

    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    label = tk.Label(frame, text="Contents")
    label.pack()
    text = tk.Text(frame)
    text.pack()
    
    text_intrf = TkTextInterface(root, text, lambda: label.config(text="Contents*"), lambda: label.config(text="Contents"))
    clipboard = TkClipboard(root)
    edit_history = EditHistory(50)
    # restriction = RegexRestrict(("line", "^(\+|-)?[0-9]{0,5}$"))
    # text_editor = TextEditor(text_intrf, clipboard, edit_history, restriction)
    text_editor = TextEditor(text_intrf, clipboard, edit_history)

    root.mainloop()

if __name__ == "__main__":
    main()
