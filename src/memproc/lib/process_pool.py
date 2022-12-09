import psutil
from rich.console import Console
from rich.table import Table

from memproc.lib.process import Process, ProcNameLevel


class ProcessPool:
    def __init__(
        self,
        name_level: int,
        sort_by: str,
        sort_reverse: bool,
        show_total: bool,
        units: str,
    ):
        self.name_level = name_level
        self.show_total = show_total
        self.units = f'{units.upper()}B'
        self.processes = self._get_processes()
        self.mem = sum(p.mem for p in self.processes)
        self.mem = int(self.mem) if int(self.mem) == self.mem else round(self.mem, 2)
        self.processes.sort(key=lambda p: getattr(p, sort_by), reverse=sort_reverse)

    def _get_processes(self) -> list:
        processes = []
        for proc in psutil.process_iter():
            try:
                p = Process(proc, self.name_level, self.units)
            except psutil.AccessDenied:
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
