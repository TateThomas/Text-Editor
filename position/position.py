from common_validation import CommonValidation

class Position:

    def __init__(self, line, column):
        self.line = CommonValidation.validate_type(line, int)
        self.column = CommonValidation.validate_type(column, int)
    
    def __eq__(self, other):
        try:
            position2 = CommonValidation.validate_type(other, Position)
            return (self.line == position2.line) and (self.column == position2.column)
        except TypeError:
            raise NotImplementedError(f"Comparison between Position and {type(other)} is not currently supported")
    
    def __lt__(self, other):
        try:
            position2 = CommonValidation.validate_type(other, Position)
            return (self.line < position2.line) or ((self.line == position2.line) and (self.column < position2.column))
        except TypeError:
            raise NotImplementedError(f"Comparison between Position and {type(other)} is not currently supported")
    
    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)
    
    def __gt__(self, other):
        return not self.__le__(other)
    
    def __ge__(self, other):
        return not self.__lt__(other)
    
    def __str__(self):
        return f"({self.line}, {self.column})"
