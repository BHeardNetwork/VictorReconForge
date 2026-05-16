"""
VictorReconForge — Hacker TUI
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import time

console = Console()

def launch_hacker_tui(runtime=None, last_target=None, graph=None):
    console.clear()
    console.print(Panel.fit("[bold red]🧠 VICTORRECONFORGE HACKER TUI[/bold red]"))
    while True:
        console.print("\n[bold yellow]Commands:[/bold yellow] 1=Scan  2=Results  3=Workers  4=Map  q=Quit")
        choice = Prompt.ask("Action", choices=["1","2","3","4","q"], default="1")
        if choice == "1":
            target = Prompt.ask("Target")
            console.print(f"[green]Scanning {target}...[/green]")
        elif choice == "q":
            break
        time.sleep(0.5)
    console.print("[red]Session ended.[/red]")