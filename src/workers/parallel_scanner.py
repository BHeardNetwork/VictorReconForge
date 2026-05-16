"""
VictorReconForge — Parallel Worker Pool
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress

console = Console()

class ParallelWorkerPool:
    def __init__(self, num_workers: int = 8):
        self.num_workers = num_workers
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        console.print(f"[cyan]Worker pool: {num_workers} threads online[/cyan]")

    def submit_batch(self, func, items):
        results = []
        with Progress() as progress:
            task = progress.add_task("[green]Workers executing...", total=len(items))
            futures = {self.executor.submit(func, item): item for item in items}
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    console.print(f"[red]Worker error: {e}[/red]")
                progress.update(task, advance=1)
        return results

    def shutdown(self):
        self.executor.shutdown()