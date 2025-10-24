import json
import time

from fastapi import APIRouter, Path, Query
from fastapi.responses import StreamingResponse

# from fastapi_learn.schema import Item

router = APIRouter()


@router.get("/")
async def read_root():
    return {"hello": "world"}


@router.get("/items/{item_id}")
async def read_item(item_id: int = Path(..., title="ID", ge=0, le=1000), q: str | None = Query(None, max_length=50)):
    return {"item_id": item_id, "q": q}


# @router.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


@router.get("/stream")
async def stream():
    async def generate():
        n = 1
        while True:
            data = {"value": n}
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)
            print(f"send data: {data}")
            n += 1

    return StreamingResponse(generate(), media_type="text/event-stream")
