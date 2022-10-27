from typing import Union
from fastapi import FastAPI, Query
from enum import Enum
from fastapi.testclient import TestClient

from pydantic import BaseModel

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
    


app = FastAPI()

client = TestClient(app)

@app.get('/')
async def root():
  return {
        'data': {' message' : 'salut tout le monde'} 
  }
  
@app.get('/username/{name}')
async def read_name(name: str):
  return {"name" : name}


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json({
        'data': {' message' : 'salut tout le monde'} 
  })

@app.get("/user/me")
async def read_user_me():
    return {"user_id": "utilisateur courant"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
 if model_name is ModelName.alexnet:
   return {"model_name": model_name, "message": "Deep Learning FTW!"}
 
 if model_name.value == "lenet":
   return {"model_name": model_name, "message": "LeCNN all the images"}
 
 return {"model_name": model_name, "message": "Have some residuals"}

#query parameters

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip+limit]
  
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
  
# required query
@app.get("/queryneed/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

#request body 
@app.post("/items/")
async def create_item(item: Item):
    return item


@app.put("/putitems/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
  
@app.get("/show/")
async def show(item: Item):
  return { **item.dict()}

#query parameters and string validations 
@app.get("/items/")
async def read_items(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
