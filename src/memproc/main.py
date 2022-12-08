import typer
from rich import print

from memproc import core, utils

app = typer.Typer(
    add_completion=False,
    help='✨ Fancy display of memory usage.',
)


@app.command()
def run(
    version: bool = typer.Option(
        False,
        '--version',
        show_default=False,
        help='Show installed version.',
    ),
    update: bool = typer.Option(
        False,
        '--update',
        show_default=False,
        help='Update memproc to last version.',
    ),
):
    if version:
        print(utils.get_memproc_version())
        return
    if update:
        utils.update_memproc()
        return
    core.display_memproc()


if __name__ == "__main__":
    app()
