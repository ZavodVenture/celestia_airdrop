class Error:
    name = ''
    message = ''
    exception = None
    filename = ''
    line = 0

    def __init__(self, name, message, exception=None, filename=None, line=None):
        self.name = name
        self.message = message
        self.exception = exception
        self.filename = filename
        self.line = line

    def get_dict(self):
        return {
            'name': self.name,
            'message': self.message
        }

    def __str__(self):
        exc_msg = f' - {self.filename}[{self.line}] - {type(self.exception)}'
        return f'({self.name}) {self.message}{exc_msg if self.exception else ""}'
