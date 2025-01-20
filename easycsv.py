


class Dialect:
    """
        Describe a CSV dialect.
    """
    QUOTE_NONE=0
    QUOTE_ALL=1
    QUOTE_MINIMAL=2
    QUOTE_NONNUMERIC=3
    QUOTE_STRINGS=4
    QUOTE_NOTNULL=5

    def __init__(self, delimiter=',', quotechar='"', escapechar=None, doublequote=True, skipinitialspace=False, lineterminator='\r\n', quoting=QUOTE_MINIMAL):
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.escapechar = escapechar
        self.doublequote = doublequote
        self.skipinitialspace = skipinitialspace
        self.lineterminator = lineterminator
        self.quoting = quoting
        self.header = True  # if true, first data line read/written will be a header
        self.skiplines = 1  # how many lines to skip before starting to process data (ignored for writing)
        #self.skipblanklines = True
        #self.trimfields = True

class unix_dialect(Dialect):
    def __init__(self):
        return super().__init__(lineterminator='\n', quoting=Dialect.QUOTE_ALL)

class excel(Dialect):
    def __init__(self):
        return super().__init__()

class excel_tab(Dialect):
    def __init__(self):
        return super().__init__(delimiter='\t')


class Reader():
    def __init__(self, csvfile, dialect, encoding="utf-8"):
        self._input = None
        self._fieldbuffer = ""
        self._linebuffer = ""
        self._inquote = False
        self._row = []
        if isinstance(csvfile, str):
            self._input = open(csvfile, "r", newline="", encoding=encoding)
        self.dialect = dialect
        self.line_num = 0

    def __next__(self):
        row = []
        self._linebuffer += next(self._input)
        self.line_num += 1
        i = 0
        end = len(self._linebuffer)
        while i < end:
            if self.dialect.quoting == Dialect.QUOTE_NONE:
                if self._linebuffer[i:].startswith(self.dialect.delimiter):
                    i += len(self.dialect.delimiter)
                    self._row.append(self._fieldbuffer)
                    self._fieldbuffer = ""
                elif self._linebuffer[i:].startswith(self.dialect.lineterminator):
                    i += len(self.dialect.lineterminator)
                    self._row.append(self._fieldbuffer)
                    self._fieldbuffer = ""
                    if i < end:
                        self._linebuffer += self._linebuffer[i:]
                    else:
                        self._linebuffer = ""
                    return self._row
                else:
                    self._fieldbuffer += self._linebuffer[i]
                    i += 1
                


class DictReader(Reader):

    def __init__(self):
        pass
