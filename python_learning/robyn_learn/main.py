from robyn import Robyn

app = Robyn(__file__)


@app.get("/")
async def h(request):
    return "Hello, world!"


def main():
    app.start(port=8080)


if __name__ == "__main__":
    main()
