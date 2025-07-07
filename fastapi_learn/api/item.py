from fastapi import APIRouter, Path, Query

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
