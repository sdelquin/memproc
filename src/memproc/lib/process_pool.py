import psutil
from rich.console import Console
from rich.table import Table

from memproc.lib.process import Process, ProcNameLevel


class ProcessPool:
    def __init__(self, name_level: int, sort_by: str, sort_reverse: bool):
        self.name_level = name_level
        self.processes = self._get_processes(name_level)
        self.processes.sort(key=lambda p: getattr(p, sort_by), reverse=sort_reverse)

    def _get_processes(self, name_level: int) -> list:
        processes = []
        for proc in psutil.process_iter():
            try:
                # just to trigger AccessDenied if proceed
                proc.memory_info()
            except psutil.AccessDenied:
                pass
            else:
                p = Process(proc, name_level)
                processes.append(p)
        return processes

    def show(self):
        table = Table(show_lines=self.name_level == ProcNameLevel.CMDLINE)
        table.add_column('PID')
        table.add_column('Name')
        table.add_column('Mem')
        for proc in self.processes:
            table.add_row(*proc.as_table_row())
        console = Console()
        console.print(table)
