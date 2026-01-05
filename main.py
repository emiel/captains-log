#!/usr/bin/env -S uv run --script

import datetime as dt
import getpass
import random
import string
from collections.abc import Iterable
from pathlib import Path
from typing import Annotated

import typer


def _get_weekdays_for(date: dt.date) -> Iterable[dt.date]:
    year, week, _ = date.isocalendar()
    first_week_day = dt.date.fromisocalendar(year=year, week=week, day=1)

    for n in range(5):
        yield first_week_day + dt.timedelta(days=n)


def _get_captain() -> str:
    return getpass.getuser()


def _get_starship_registry() -> str:
    return f"NCC-{random.randrange(100, 10000)}"


def _get_self_destruct_code() -> str:
    # JANEWAY PI 1-1
    captain = _get_captain().upper()
    a = random.choice(string.digits)
    b = random.choice(string.digits)
    return f"{captain} PI {a}-{b}"


def _get_template(date: dt.date) -> str:
    year, week, _ = date.isocalendar()
    captain = _get_captain()
    starship_registry = _get_starship_registry()
    self_destruct_code = _get_self_destruct_code()

    buf = f"# LOG ENTRIES: {year}-W{week:02d}\n"
    buf += "\n"
    buf += f"    Captain: {captain}\n"
    buf += f"    Starship: {starship_registry}\n"
    buf += f"    Self-destruct code authorization: {self_destruct_code}\n"
    buf += "\n"

    for day in _get_weekdays_for(date=date):
        buf += f"## Captain's log, {day.isoformat()} ({day.strftime('%a')})\n"
        buf += "\n"
        buf += "- [ ] Task...\n"
        buf += "\n"

    buf += "## Backlog\n"
    buf += "\n"
    buf += "- [ ] Task...\n"

    return buf


def _get_log_path(date: dt.date) -> Path:
    year, week, _ = date.isocalendar()
    return Path(f"{year}-W{week:02d}.md")


def _init_log(path: Path, buf: str) -> None:
    with open(path, "w") as file:
        file.write(buf)


def main(log_dir: Annotated[Path, typer.Argument()]) -> None:
    if not log_dir.is_dir():
        print(f"Directory {log_dir} does not exist")
        raise typer.Abort()

    today = dt.date.today()
    template = _get_template(date=today)

    path = log_dir / _get_log_path(date=today)

    if not path.exists():
        _init_log(path=path, buf=template)

    print(path.resolve())


if __name__ == "__main__":
    typer.run(main)
