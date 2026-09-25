import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app


@pytest.mark.asyncio
async def test_health_reports_ok_when_trueforge_unreachable(monkeypatch):
    monkeypatch.setenv("GREENLIGHT_API_KEY", "test-key")
    monkeypatch.setenv("FRONTEND_ORIGIN", "http://localhost:5173")
    monkeypatch.setenv("GITHUB_BOT_TOKEN", "test-token")
    monkeypatch.setenv("LEDGER_PATH", ":memory:")
    monkeypatch.setenv("TRUEFORGE_BASE_URL", "http://localhost:1")

    app = create_app()
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        async with app.router.lifespan_context(app):
            response = await client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["trueforge_reachable"] is False
