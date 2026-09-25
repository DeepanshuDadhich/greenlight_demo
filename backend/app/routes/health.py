from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(request: Request) -> dict:
    trueforge_client = request.app.state.trueforge_client
    trueforge_reachable = await trueforge_client.health()
    return {"ok": True, "trueforge_reachable": trueforge_reachable}
