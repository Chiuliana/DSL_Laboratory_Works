# CONSTANTS
DIGITS = '0123456789'
KEYWORDS = {'if', 'while', 'return'}

# ERRORS
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start  # Start position of the error
        self.pos_end = pos_end  # End position of the error
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'  # Formatting error message
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'  # Adding file and line information
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
