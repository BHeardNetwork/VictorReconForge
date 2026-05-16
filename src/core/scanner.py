 """
VictorReconForge — GitHub Scanner Core
"""

import requests
import time
from typing import Dict, List, Any
from rich.console import Console

console = Console()

class GitHubScanner:
    def __init__(self, runtime=None, token: str = None):
        self.runtime = runtime
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})
        self.base_url = "https://api.github.com"

    def _get(self, endpoint: str, params: dict = None) -> Any:
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = self.session.get(url, params=params or {})
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            console.print(f"[red]Scan error: {e}[/red]")
            return {}

    def scan_organization(self, org: str, depth: int = 2) -> Dict:
        console.print(f"[bold cyan]Scanning: {org}[/bold cyan]")
        org_info = self._get(f"orgs/{org}") or self._get(f"users/{org}")
        repos = self._get(f"orgs/{org}/repos", {"per_page": 100}) or self._get(f"users/{org}/repos", {"per_page": 100})
        repo_list = []
        for repo in (repos or [])[:30]:
            repo_list.append({"name": repo.get("name"), "stars": repo.get("stargazers_count", 0), "language": repo.get("language")})
        result = {"org": org, "repos": repo_list, "timestamp": time.time()}
        if self.runtime:
            self.runtime.save_scan_result(org, result)
        return result

    def deep_scan_repos(self, repo_full_names: List[str]) -> List[Dict]:
        return [{"repo": name} for name in repo_full_names[:5]]