import httpx

from app.config import Settings

GITHUB_API_URL = "https://api.github.com"


class GitHubClient:
    def __init__(self, http_client: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http_client
        self._token = settings.github_bot_token
        self._login = settings.github_bot_login

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    async def get_pull_request(self, owner: str, repo: str, number: int) -> dict:
        response = await self._http.get(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{number}",
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()
