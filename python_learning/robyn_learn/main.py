from robyn import Request, Robyn

app = Robyn(__file__)


@app.get("/")
async def index(request: Request):
    return "Hello, world!"


def main():
    app.start(port=8080)


if __name__ == "__main__":
    main()
