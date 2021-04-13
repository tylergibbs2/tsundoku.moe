import aiohttp
import asyncio
import os
import typing

import asyncpg
from quart import Quart, request, Response

import config
from . import feedback
from . import metrics

app = Quart("tsundoku_moe")


@app.route("/feedback", methods=["POST", "OPTIONS"])
async def feedback_route() -> typing.Union[Response, dict, tuple]:
    if request.method == "OPTIONS":
        resp = Response({})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "POST"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

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


@app.route("/metrics/<string:client>", methods=["POST", "OPTIONS"])
async def metrics_route(client: str) -> dict:
    if request.method == "OPTIONS":
        resp = Response({})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "POST"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

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
