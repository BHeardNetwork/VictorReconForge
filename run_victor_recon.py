#!/usr/bin/env python3
"""
VictorReconForge — Main Runtime Launcher
Full-stack GitHub recon with workers, runtime, and hacker GUI.
"""

import typer
from rich.console import Console
from rich.panel import Panel
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from core.scanner import GitHubScanner
from core.mapper import EmpireMapper
from core.runtime import ReconRuntime
from gui.hacker_tui import launch_hacker_tui
from workers.parallel_scanner import ParallelWorkerPool

app = typer.Typer(help="VictorReconForge — The ultimate GitHub empire recon toolkit")
console = Console()

@app.command()
def scan(target: str = typer.Argument(..., help="GitHub org or user to scan (e.g. MASSIVEMAGNETICS)"), depth: int = typer.Option(2, help="Scan depth"), workers: int = typer.Option(8, help="Number of parallel workers"), gui: bool = typer.Option(False, "--gui", help="Launch interactive hacker GUI after scan")):
    """Launch full recon scan on target empire."""
    console.print(Panel.fit("[bold red]🚀 VICTORRECONFORGE — DEPLOYING SCAN[/bold red]", border_style="red"))
    runtime = ReconRuntime()
    scanner = GitHubScanner(runtime=runtime)
    mapper = EmpireMapper(runtime=runtime)
    worker_pool = ParallelWorkerPool(num_workers=workers)
    # Demo scan
    org_data = scanner.scan_organization(target, depth=depth)
    graph = mapper.build_dependency_graph(org_data)
    if gui:
        launch_hacker_tui(runtime, target, graph)
    console.print("[green]✓ Mission complete.[/green]")

@app.command()
def interactive():
    """Launch interactive hacker TUI."""
    runtime = ReconRuntime()
    launch_hacker_tui(runtime)

if __name__ == "__main__":
    app()