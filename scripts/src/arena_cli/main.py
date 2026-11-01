"""The arena command-line tool."""

import pathlib

import typer
from arena_core.db import get_engine
from arena_core.seed import SeedError, load_seed, verify_seed
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
seed_app = typer.Typer(no_args_is_help=True, help="Load and verify the curated seed.")
app.add_typer(seed_app, name="seed")
console = Console()


@seed_app.command("load")
def seed_load(
    seed: pathlib.Path = typer.Option(pathlib.Path("seed/SEED-v4.json")),
    slice_: pathlib.Path = typer.Option(pathlib.Path("seed/SLICE-1-LANDMARKS.json"), "--slice"),
) -> None:
    """Load niches and landmarks. Re-running with the same files changes nothing."""
    try:
        result = load_seed(get_engine(), seed, slice_)
    except SeedError as error:
        console.print(f"[red]Seed files are inconsistent, nothing written:[/red] {error}")
        raise typer.Exit(1) from error
    if result.skipped:
        console.print("Already loaded: these exact files were loaded before.")
    else:
        console.print(f"Loaded: {result.created} created, {result.updated} updated.")


@seed_app.command("verify")
def seed_verify() -> None:
    """Check the loaded seed against gate G0.3. Exits non-zero on any mismatch."""
    results = verify_seed(get_engine())
    table = Table("check", "expected", "actual", "")
    for name, expected, actual in results:
        table.add_row(name, str(expected), str(actual), "ok" if expected == actual else "MISMATCH")
    console.print(table)
    if any(expected != actual for _, expected, actual in results):
        raise typer.Exit(1)
