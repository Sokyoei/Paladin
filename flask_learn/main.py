import asyncio

from flask import Flask, Response, jsonify, stream_with_context

from flask_learn.api import all_blueprints
from flask_learn.config import db_instance, settings
from flask_learn.utils import register_error_handlers

########################################################################################################################
# app
########################################################################################################################
app = Flask(__name__)

# config
app.config["SECRET_KEY"] = settings.SECRET_KEY
app.json.ensure_ascii = False  # CJK ascii

# database
db_instance.init_app(app)

# blueprints
for blueprint in all_blueprints:
    app.register_blueprint(blueprint)

# error handlers
register_error_handlers(app)

if settings.DEBUG:
    app.debug = True


########################################################################################################################
# routes
########################################################################################################################
@app.get("/")
async def index():
    return jsonify({"hello": "world"})


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
