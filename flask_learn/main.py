from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return "hello world"


def main():
    app.run()


if __name__ == "__main__":
    main()
