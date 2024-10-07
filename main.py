from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"
    
class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category
    
items = {
    0: Item(name="Drill Machine", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES)
}

# FastAPI handles JSON serialization and deserialization
@app.get("/")
def index() -> dict[str, dict[int, dict]]:
    # Convert Item objects to dict
    return {"Requested item(s)": {k: v.dict() for k, v in items.items()}}


@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> dict:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")
    return items[item_id].dict()


# Function parameters that are not path parameters can be specified as query parameters 
@app.get("/items/")
def query_item_by_parameters(
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None,
    ) -> dict:
    
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category == category,
            )
        )
    
    # Convert Item objects to dicts for serialization
    selection = {item.id: item.dict() for item in items.values() if check_item(item)}
    
    if not selection:
        raise HTTPException(status_code=404, detail="No items match the query parameters.")
    
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection
    }
    
@app.post("/")
def add_item(item: Item) -> dict[str, Item]:
    
    if item.id in items:
        HTTPException(status_code=400, detail=f"Item with {item.id=} already exists.")
        
    items[item.id] = item
    return {"added": item}


@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
) -> dict[str, Item]:
    
    if item_id not in items:
        HTTPException(status_code=404, detail=f"item with {item_id} does not exist.")
        
    if all(info is None for info in (name, price, count)):
        raise HTTPException(status_code=400, detail="No parameters provided for update.")
    
    item = items[item_id]
    
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count
        
    return {"Updated item": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"item with {item_id} does not exist")

    item = items.pop(item_id)
    return {"Deleted item": item}