import asyncio
import atexit

from flask import Flask, Response, render_template, stream_with_context

from flask_learn.api import all_blueprints
from flask_learn.config import db_instance, settings
from flask_learn.utils import ORJSONProvider, register_error_handlers


########################################################################################################################
# app
########################################################################################################################
def create_app() -> Flask:
    app = Flask(__name__)

    # config
    app.config.from_object(settings)
    app.json = ORJSONProvider(app)  # use `orjson` instead of `json`
    app.json.ensure_ascii = False  # CJK ascii for `DefaultJSONProvider` or `UJSONProvider`

    # database
    db_instance.init_app(app)
    db_instance.init_db(app)

    # blueprints
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    # error handlers
    register_error_handlers(app)

    atexit.register(lambda: db_instance.close_db(app))

    return app


app = create_app()


########################################################################################################################
# routes
########################################################################################################################
@app.get("/")
async def index():
    return render_template("index.html")


@app.route('/sse')
async def sse():
    async def generate():
        count = 0
        while True:
            yield f"data: {count}\n\n"
            count += 1
            await asyncio.sleep(1)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


def main():
    app.run(host="0.0.0.0", port=12920)  # WSGI
    # uvicorn.run("main:app", reload=True, host="0.0.0.0", port=12920)  # ASGI


if __name__ == "__main__":
    main()
