import psutil

from . import utils


class ProcNameLevel:
    NAME = 1
    EXE = 2
    CMDLINE = 3


PROCESS_FIELDS = {'p': 'pid', 'n': 'name', 'm': 'mem'}


class Process:
    def __init__(self, pid: int, name: str, mem: float):
        self.pid = pid
        self.name = name
        self.mem = mem

    def __str__(self):
        return f'[{self.pid}] {self.name}: {self.mem}'

    @classmethod
    def from_psutil(cls, proc: psutil.Process, name_level: int):
        pid = proc.pid
        match name_level:
            case ProcNameLevel.NAME:
                name = proc.name()
            case ProcNameLevel.EXE:
                name = proc.exe()
            case ProcNameLevel.CMDLINE:
                name = ' '.join(proc.cmdline())
        if not name:
            name = proc.name()
        mem = proc.memory_info().rss
        return cls(pid, name, mem)

    def mem_display(self, units: str):
        return utils.mem_display(self.mem, units)

    def as_table_row(self, units: str):
        return str(self.pid), self.name, self.mem_display(units)
