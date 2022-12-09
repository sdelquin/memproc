import psutil


class ProcNameLevel:
    NAME = 1
    EXE = 2
    CMDLINE = 3


class Process:
    def __init__(self, proc: psutil.Process, name_level: int):
        self.pid = proc.pid
        match name_level:
            case ProcNameLevel.NAME:
                self.name = proc.name()
            case ProcNameLevel.EXE:
                self.name = proc.exe()
            case ProcNameLevel.CMDLINE:
                self.name = ' '.join(proc.cmdline())
        self.name = self.name if self.name else proc.name()
        self.mem = proc.memory_info().rss

    @property
    def humanized_mem(self):
        return f'{self.mem / 2 ** 20:.02f} MB'

    def as_table_row(self):
        return str(self.pid), self.name, self.humanized_mem
