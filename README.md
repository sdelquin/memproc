# memproc

✨ Fancy display of memory usage.

## Installation

```console
$ pip install memproc
```

## Usage

```console
Usage: memproc [OPTIONS]

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version                            Show installed version.                                                                               │
│ --update                             Update memproc to last version.                                                                       │
│ --sort              -s      TEXT     Sort results by criteria (m:mem, p:pid, d:description). [default: m]                                  │
│ --sort-reverse      -r               Sort reverse by current criteria.                                                                     │
│ --description       -d      TEXT     Process description (n:name, e:executable, c:command line). [default: n]                              │
│ --show-total        -t               Show total used memory.                                                                               │
│ --units             -u      TEXT     Memory units (k:KB, m:MB, g:GB). [default: m]                                                         │
│ --num-processes     -n      INTEGER  Limit the number of processes shown. [default: 0]                                                     │
│ --group                              Group process by description.                                                                         │
│ --greater-than      -g      FLOAT    Show processes with used memory greater than this value. [default: 0]                                 │
│ --lower-than        -l      FLOAT    Show processes with used memory lower than this value. [default: 17179869184]                         │
│ --find-description  -f      TEXT     Find processes with text by the chosen description criteria.                                          │
│ --no-color                           Omit row coloring.                                                                                    │
│ --help                               Show this message and exit.                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
