import aiohttp
import asyncio
import typing

import asyncpg
from quart import Quart, request, Response
from quart_cors import cors

try:
    import config
except ImportError:
    import heroku_config as config

from . import feedback
from . import metrics


CORS_SETTINGS = {
    "allow_headers": ["Content-Type"],
    "allow_methods": ["POST"],
    "allow_origin": "*"
}


app = Quart("tsundoku_moe")
app = cors(app, **CORS_SETTINGS)


@app.route("/feedback", methods=["POST"])
async def feedback_route() -> typing.Union[Response, dict, tuple]:
    data = await request.get_json()

    type_ = data.get("type")
    feedback_data = data.get("feedback_data")

    if type_ == "general":
        await feedback.send_general(feedback_data)
    elif type_ == "feature":
        await feedback.send_feature(feedback_data)
    elif type_ == "bug":
        await feedback.send_bug(feedback_data)
    else:
        return {}, 400

    return data


@app.route("/metrics/<string:client>", methods=["POST"])
async def metrics_route(client: str) -> dict:
    data = await request.get_json()
    return await metrics.handle(client, data)


@app.before_serving
async def setup_db() -> None:
    loop = asyncio.get_event_loop()

    app.db = await asyncpg.create_pool(loop=loop, dsn=config.PSQL_DSN)

@app.before_serving
async def setup_session() -> None:
    loop = asyncio.get_event_loop()

    app.session = aiohttp.ClientSession(
        loop=loop,
        timeout=aiohttp.ClientTimeout(total=15.0)
    )

@app.after_serving
async def cleanup() -> None:
    try:
        await app.db.close()
        await app.session.close()
    except Exception:
        pass

def run() -> None:
    app.run()
