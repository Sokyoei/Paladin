from typing import Union

from fastapi import APIRouter, Path, Query
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@router.get("/")
async def read_root():
    return {"hello": "world"}


@router.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="ID", ge=0, le=1000), q: Union[str, None] = Query(None, max_length=50)
):
    return {"item_id": item_id, "q": q}


@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
