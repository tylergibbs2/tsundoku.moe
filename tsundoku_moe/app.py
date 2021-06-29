from quart import Quart, render_template
from quart_cors import cors


CORS_SETTINGS = {
    "allow_headers": ["content-type"],
    "allow_methods": ["POST"],
    "allow_origin": "*"
}


app = Quart("tsundoku_moe")
app = cors(app, **CORS_SETTINGS)


@app.route("/", methods=["GET"])
async def index():
    return await render_template("index.html")

@app.route("/docs", methods=["GET"])
async def docs():
    return await render_template("docs.html")

def run() -> None:
    app.run()
