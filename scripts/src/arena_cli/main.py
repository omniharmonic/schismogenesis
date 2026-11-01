"""The arena command-line tool."""

import pathlib

import typer
from arena_core.config import load_settings
from arena_core.db import get_engine
from arena_core.seed import SeedError, load_seed, verify_seed
from arena_core.storage import FileSourceStore
from arena_extract.written import chunk_source, extract_source, gate_source
from arena_harness import gold, report
from arena_ingest.written import WrittenWork, ingest_written
from arena_llm import AnthropicApi, BackendDisabled, ClaudeCodeBatch
from rich.console import Console
from rich.table import Table

from arena_cli import redline as redline_checks

app = typer.Typer(no_args_is_help=True)
seed_app = typer.Typer(no_args_is_help=True, help="Load and verify the curated seed.")
app.add_typer(seed_app, name="seed")
eval_app = typer.Typer(no_args_is_help=True, help="Score extraction runs against gold.")
app.add_typer(eval_app, name="eval")
written_app = typer.Typer(no_args_is_help=True, help="Run a written work through the pipeline.")
app.add_typer(written_app, name="written")
llm_app = typer.Typer(no_args_is_help=True, help="LLM backend checks.")
app.add_typer(llm_app, name="llm")
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


@eval_app.command("run")
def eval_run(
    gold_version: pathlib.Path = typer.Option(..., "--gold", help="evals/gold/v<k> directory"),
    predictions: pathlib.Path = typer.Option(..., help="JSONL of predicted claims"),
    report_path: pathlib.Path = typer.Option(..., "--report"),
    split: str = typer.Option("dev"),
    purpose: str | None = typer.Option(None, help="Required for the sealed test split; logged."),
    reference_m1: float | None = typer.Option(None, help="The Claude pipeline's own M1."),
) -> None:
    """Score predictions and write a Markdown report."""
    if split not in ("dev", "test"):
        raise typer.BadParameter("split must be dev or test")
    chunks = gold.load_split(gold_version, split, purpose)  # type: ignore[arg-type]
    claims = [
        gold.PredictedClaim.model_validate_json(line)
        for line in predictions.read_text().splitlines()
        if line.strip()
    ]
    sheet = report.load_sheet()
    lines = report.evaluate(report.score(chunks, claims), sheet, reference_m1)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report.render(f"Eval: {predictions.name} ({split})", lines, sheet))
    console.print(f"Wrote {report_path}")


@app.command()
def redline(root: pathlib.Path = typer.Option(pathlib.Path("."))) -> None:
    """Fail if a red line is crossed in the repository or public output."""
    problems = redline_checks.check(root)
    for problem in problems:
        console.print(f"[red]{problem}[/red]")
    if problems:
        raise typer.Exit(1)
    console.print("Red-line checks passed.")


@written_app.command("ingest")
def written_ingest(
    file: pathlib.Path,
    url: str = typer.Option(...),
    title: str = typer.Option(...),
    author: str = typer.Option(..., help="landmark_id"),
    published: str = typer.Option(..., help="YYYY-MM-DD"),
    channel: str = typer.Option(...),
    format_: str = typer.Option("essay", "--format"),
    authorship: str = typer.Option("own_name"),
) -> None:
    """Store a cleaned text file (paragraphs separated by blank lines) and split it up."""
    work = WrittenWork(url, title, author, published, channel, format=format_,
                       authorship=authorship)  # fmt: skip
    episode_id = ingest_written(
        get_engine(), FileSourceStore(load_settings().source_dir), work, file
    )
    console.print(f"Episode {episode_id}; {chunk_source(get_engine(), episode_id)} chunks.")


@written_app.command("extract")
def written_extract(episode_id: str, batch: str = typer.Option(...)) -> None:
    """Queue extraction, or collect and anchor results once a Claude session has answered."""
    console.print(extract_source(get_engine(), ClaudeCodeBatch(batch, "gold"), episode_id))


@written_app.command("gate")
def written_gate(episode_id: str) -> None:
    """Run the entailment gate locally. Needs: uv sync --all-packages --extra nli."""
    from arena_extract.nli import NLIGate

    nli = NLIGate()
    console.print(gate_source(get_engine(), nli.score, nli.MODEL, episode_id))


@llm_app.command("smoke")
def llm_smoke(backend: str = typer.Option("anthropic_api")) -> None:
    """Check that the paid backend refuses to run (G0.6)."""
    if backend != "anthropic_api":
        raise typer.BadParameter("only anthropic_api is checked here")
    try:
        AnthropicApi().complete_json()
    except BackendDisabled as error:
        console.print(str(error))
