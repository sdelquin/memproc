import psutil

from . import utils


class ProcDesc:
    NAME = 'n'
    EXE = 'e'
    CMDLINE = 'c'


PROCESS_FIELDS = {'p': 'pid', 'd': 'description', 'm': 'mem'}


class Process:
    def __init__(self, pid: int, description: str, mem: float):
        self.pid = pid
        self.description = description
        self.mem = mem

    def __str__(self):
        return f'[{self.pid}] {self.description}: {self.mem}'

    @classmethod
    def from_psutil(cls, proc: psutil.Process, description: str):
        pid = proc.pid
        match description:
            case ProcDesc.NAME:
                description = proc.name()
            case ProcDesc.EXE:
                description = proc.exe()
            case ProcDesc.CMDLINE:
                description = ' '.join(proc.cmdline())
        if not description:
            description = proc.name()
        mem = proc.memory_info().rss
        return cls(pid, description, mem)

    def mem_display(self, units: str):
        return utils.mem_display(self.mem, units)

    def as_table_row(self, units: str):
        return str(self.pid), self.description, self.mem_display(units)
