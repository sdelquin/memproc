from collections import defaultdict

import psutil
from rich.console import Console
from rich.table import Table

from memproc.lib.process import PROCESS_FIELDS, ProcDesc, Process

from . import utils
from .utils import convert_mem


class ProcessPool:
    def __init__(
        self,
        description: str,
        sort_by: str,
        sort_reverse: bool,
        show_total: bool,
        units: str,
        num_processes: int,
        group: bool,
        gt_mem: float,
        lt_mem: float,
        find_description: str,
        color_output: bool,
    ):
        self.description = description
        self.show_total = show_total
        self.sort_by = PROCESS_FIELDS[sort_by]
        self.sort_reverse = sort_reverse
        self.units = f'{units.upper()}B'
        self.color_output = color_output
        self._get_processes()
        if group:
            self._group_processes()
        self._sort_processes()
        self._filter_processes_by_memsize(gt_mem, lt_mem)
        self._filter_processes_by_description(find_description)
        if num_processes > 0:
            self.processes = self.processes[:num_processes]
        self.mem = self._get_total_mem()
        self._grade_processes(self._get_grade_interval())

    def _get_processes(self):
        self.processes = []
        for proc in psutil.process_iter():
            try:
                p = Process.from_psutil(proc, self.description)
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
            else:
                self.processes.append(p)

    def _sort_processes(self):
        reverse = (self.sort_by in ['pid', 'description'] and self.sort_reverse) or (
            self.sort_by == 'mem' and not self.sort_reverse
        )
        self.processes.sort(key=lambda p: getattr(p, self.sort_by), reverse=reverse)

    def _group_processes(self):
        groups = defaultdict(int)
        for proc in self.processes:
            groups[proc.description] += proc.mem
        self.processes = []
        for desc, mem in groups.items():
            proc = Process('', desc, mem)
            self.processes.append(proc)

    def _filter_processes_by_memsize(self, lower_limit, upper_limit):
        self.processes = [
            p
            for p in self.processes
            if lower_limit <= convert_mem(p.mem, self.units) <= upper_limit
        ]

    def _filter_processes_by_description(self, find):
        self.processes = [
            p for p in self.processes if find.upper() in p.description.upper()
        ]

    def _get_grade_interval(self, num_slots=4):
        min_mem = min(p.mem for p in self.processes)
        max_mem = max(p.mem for p in self.processes)
        interval_size = (max_mem - min_mem) / num_slots
        return [min_mem + i * interval_size for i in range(1, num_slots + 1)]

    def _grade_processes(self, grade_interval: list):
        for proc in self.processes:
            proc.grade(grade_interval)

    def _get_total_mem(self):
        return sum(p.mem for p in self.processes)

    def mem_display(self, units):
        return utils.mem_display(self.mem, units)

    def show(self):
        table = Table(show_lines=self.description == ProcDesc.CMDLINE)
        table.add_column('PID')
        table.add_column('DESCRIPTION')
        table.add_column('MEMORY')
        for proc in self.processes:
            style = proc.grade_color if self.color_output else ''
            table.add_row(*proc.as_table_row(self.units), style=style)
        style = 'purple' if self.color_output else ''
        if self.show_total:
            table.add_section()
            table.add_row('', 'TOTAL', self.mem_display(self.units), style=style)
        console = Console()
        console.print(table)
