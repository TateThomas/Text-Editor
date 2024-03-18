from position.cursor_position import CursorPosition

class RegularPositioning(CursorPosition):

    def __init__(self, text_interface):
        super().__init__(text_interface)
    
    @property
    def first(self):
        return super().first

    @property
    def last(self):
        return super().last

class BackPositioning(CursorPosition):

    def __init__(self, text_interface):
        super().__init__(text_interface)
    
    @property
    def first(self):
        try:
            first = self.text_intrf.get_selection_positions()[0]
        except:
            current_pos = self.text_intrf.get_cursor_position()
            first = self.text_intrf.get_previous_position(current_pos)
        return first

    @property
    def last(self):
        return super().last

class NextPositioning(CursorPosition):

    def __init__(self, text_interface):
        super().__init__(text_interface)
    
    @property
    def first(self):
        return super().first

    @property
    def last(self):
        try:
            last = self.text_intrf.get_selection_positions()[1]
        except:
            current_pos = self.text_intrf.get_cursor_position()
            last = self.text_intrf.get_next_position(current_pos)
        return last

class LinePositioning(CursorPosition):

    def __init__(self, text_interface):
        super().__init__(text_interface)
    
    @property
    def first(self):
        try:
            first = self.text_intrf.get_selection_positions()[0]
        except:
            current_pos = self.text_intrf.get_cursor_position()
            first = self.text_intrf.get_line_start_position(current_pos.line)
        return first

    @property
    def last(self):
        try:
            last = self.text_intrf.get_selection_positions()[1]
        except:
            current_pos = self.text_intrf.get_cursor_position()
            last = self.text_intrf.get_line_end_position(current_pos.line)
        return last
