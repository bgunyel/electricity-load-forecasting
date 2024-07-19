import uvicorn
from fastapi import FastAPI

from source.config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/")
def read_item(item_id: int):
    package = f'item {item_id}: Fenerbahçe'
    print(package)
    return package


if __name__ == "__main__":
    uvicorn.run("server:app", port=settings.BACKEND_PORT, host=settings.HOST, reload=settings.ENABLE_RELOAD)
