import asyncio

import uvicorn
from flask import Flask, Response, jsonify, stream_with_context

from flask_learn.api import all_blueprints

app = Flask(__name__)


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
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
    # app.run(debug=True, host="0.0.0.0", port=12920)  # WSGI
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=12920)


if __name__ == "__main__":
    main()
