import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps import item_router


app = FastAPI()
app.include_router(item_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def main():
    uvicorn.run(app="main:app", reload=True)


if __name__ == '__main__':
    main()
