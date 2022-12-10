import typer
from rich import print

from memproc.lib import utils
from memproc.lib.process_pool import ProcessPool

app = typer.Typer(
    add_completion=False,
    pretty_exceptions_enable=False,
    help='✨ Fancy display of memory usage (RSS).',
)


@app.command()
def run(
    version: bool = typer.Option(
        False,
        '--version',
        help='Show installed version.',
    ),
    update: bool = typer.Option(
        False,
        '--update',
        help='Update memproc to last version.',
    ),
    sort_by: str = typer.Option(
        'm',
        '--sort',
        '-s',
        help='Sort results by criteria (m:mem, p:pid, d:description).',
    ),
    sort_reverse: bool = typer.Option(
        False,
        '--sort-reverse',
        '-r',
        help='Sort reverse by current criteria.',
    ),
    description: str = typer.Option(
        'n',
        '--description',
        '-d',
        help='Process description (n:name, e:executable, c:command line).',
    ),
    show_total: bool = typer.Option(
        False,
        '--show-total',
        '-t',
        help='Show total used memory.',
    ),
    units: str = typer.Option(
        'm',
        '--units',
        '-u',
        help='Memory units (k:KB, m:MB, g:GB).',
    ),
    num_processes: int = typer.Option(
        0,
        '--num-processes',
        '-n',
        help='Limit the number of processes shown.',
    ),
    group: bool = typer.Option(
        False,
        '--group',
        help='Group process by description.',
    ),
):
    if version:
        print(utils.get_memproc_version())
        return
    if update:
        utils.update_memproc()
        return

    pool = ProcessPool(
        description, sort_by, sort_reverse, show_total, units, num_processes, group
    )
    pool.show()


if __name__ == "__main__":
    app()
