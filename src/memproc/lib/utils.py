import subprocess
import sys

import pkg_resources


def update_memproc():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', 'memproc'])


def get_memproc_version():
    return pkg_resources.get_distribution('memproc').version


def convert_mem(mem_in_bytes: int, to_unit: str):
    MEM_FACTOR = {'B': 1, 'KB': 2**10, 'MB': 2**20, 'GB': 2**30}

    mem_factor = MEM_FACTOR[to_unit]
    return mem_in_bytes / mem_factor


def mem_display(mem_in_bytes: int, units: str):
    mem = convert_mem(mem_in_bytes, units)
    mem = int(mem) if int(mem) == mem else round(mem, 2)
    return f'{mem} {units}'
