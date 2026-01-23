from aiohttp import web

app = web.Application()


def index(request: web.Request):
    return web.Response(text="Hello, world")


app.add_routes([web.get('/', index)])

if __name__ == '__main__':
    web.run_app(app)
