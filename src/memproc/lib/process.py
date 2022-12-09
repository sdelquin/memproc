import psutil

from . import utils


class ProcNameLevel:
    NAME = 1
    EXE = 2
    CMDLINE = 3


class Process:
    def __init__(self, proc: psutil.Process, name_level: int, units: str):
        self.pid = proc.pid
        self.units = units.upper()
        match name_level:
            case ProcNameLevel.NAME:
                self.name = proc.name()
            case ProcNameLevel.EXE:
                self.name = proc.exe()
            case ProcNameLevel.CMDLINE:
                self.name = ' '.join(proc.cmdline())
        self.name = self.name if self.name else proc.name()
        self.mem = proc.memory_info().rss
        self.mem = utils.convert_mem(self.mem, self.units)
        self.mem = int(self.mem) if int(self.mem) == self.mem else round(self.mem, 2)

    def mem_display(self):
        return f'{self.mem} {self.units}'

    def as_table_row(self):
        return str(self.pid), self.name, self.mem_display()
