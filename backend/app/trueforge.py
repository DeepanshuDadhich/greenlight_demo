from contextlib import AbstractAsyncContextManager

import httpx

from app.config import Settings


class TrueForgeClient:
    def __init__(self, http_client: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http_client
        self._base_url = settings.trueforge_base_url.rstrip("/")
        self._agent_name = settings.trueforge_agent_name

    async def health(self) -> bool:
        try:
            response = await self._http.get(f"{self._base_url}/health", timeout=2.0)
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    def stream_events(self, run_id: str) -> AbstractAsyncContextManager[httpx.Response]:
        url = f"{self._base_url}/agents/{self._agent_name}/runs/{run_id}/events"
        return self._http.stream("GET", url, timeout=httpx.Timeout(None, connect=5.0))
