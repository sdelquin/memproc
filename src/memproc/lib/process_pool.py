import psutil
from rich.console import Console
from rich.table import Table

from memproc.lib.process import Process, ProcNameLevel

PROCESS_FIELDS = {'p': 'pid', 'n': 'name', 'm': 'mem'}


class ProcessPool:
    def __init__(
        self,
        name_level: int,
        sort_by: str,
        sort_reverse: bool,
        show_total: bool,
        units: str,
        num_processes: int,
    ):
        self.name_level = name_level
        self.show_total = show_total
        self.units = f'{units.upper()}B'
        self.processes = self._get_processes()
        sort_by = PROCESS_FIELDS[sort_by]
        reverse = (sort_by in ['pid', 'name'] and sort_reverse) or (
            sort_by == 'mem' and not sort_reverse
        )
        self.processes.sort(key=lambda p: getattr(p, sort_by), reverse=reverse)
        if num_processes > 0:
            self.processes = self.processes[:num_processes]
        self.mem = sum(p.mem for p in self.processes)
        self.mem = int(self.mem) if int(self.mem) == self.mem else round(self.mem, 2)

    def _get_processes(self) -> list:
        processes = []
        for proc in psutil.process_iter():
            try:
                p = Process(proc, self.name_level, self.units)
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
            else:
                processes.append(p)
        return processes

    def mem_display(self):
        return f'{self.mem} {self.units}'

    def show(self):
        table = Table(show_lines=self.name_level == ProcNameLevel.CMDLINE)
        table.add_column('PID')
        table.add_column('Name')
        table.add_column('Mem')
        for proc in self.processes:
            table.add_row(*proc.as_table_row())
        if self.show_total:
            table.add_section()
            table.add_row('', 'TOTAL', self.mem_display(), style='purple')
        console = Console()
        console.print(table)
