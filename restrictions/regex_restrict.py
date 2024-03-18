from restrictions.restriction import Restriction
from common_validation import CommonValidation
import re

class RegexRestrict(Restriction):

    def __init__(self, *args):
        self.string_regex = []
        self.line_regex = []
        self.doc_regex = []
        for (list_group, regex) in args:
            self.add_regex(list_group, regex)

    @staticmethod
    def validate(regex, string):
        if isinstance(regex, list):
            if (len(regex) == 0):
                return True
            if (len(regex) == 1):
                return RegexRestrict.validate(regex[0], string)
            return RegexRestrict.validate(regex[-1], string) and RegexRestrict.validate(regex[:-1], string)
        if isinstance(regex, str) or isinstance(regex, re.Pattern):
            return re.fullmatch(regex, string) is not None
        raise TypeError(f"Regex argument must be a string, Pattern, or list containing those types, not {type(regex)}")
    
    def add_regex(self, list_group, regex):
        pattern = regex
        if (isinstance(list_group, str) and (list_group == "string")) or (isinstance(list_group, int) and (int == 0)):
            self.string_regex.append(pattern)
        elif (isinstance(list_group, str) and (list_group == "line")) or (isinstance(list_group, int) and (int == 1)):
            self.line_regex.append(pattern)
        elif (isinstance(list_group, str) and (list_group == "doc")) or (isinstance(list_group, int) and (int == 2)):
            self.doc_regex.append(pattern)
        else:
            if not isinstance(list_group, str) or not isinstance(list_group, int):
                raise TypeError(f"List group must be of type string or int, not {type(list_group)}")
            raise ValueError(f"{list_group} is not a valid list group, must be a string ('string', 'line', or 'doc'), or int (0, 1, 2, correspondingly)")
    
    def delete_regex(self, regex):
        pattern = regex
        self.regex_list[:] = [x for x in self.regex_list if x != pattern]

    def validate_string(self, string):
        return RegexRestrict.validate(self.string_regex, string)
    
    def validate_line(self, line):
        return RegexRestrict.validate(self.line_regex, line)
    
    def validate_document(self, text):
        return RegexRestrict.validate(self.doc_regex, text)
