from quart import current_app as app

from config import WEBHOOK_URLS


async def send_general(data):
    embed = {
        "title": "General Feedback",
        "description": data["feedback"],
        "color": 3315932
    }
    await app.session.post(
        WEBHOOK_URLS["general"],
        headers={
            "Content-Type": "application/json"
        },
        json={
            "embeds": [embed]
        }
    )

async def send_feature(data):
    embed = {
        "title": "Feature Request",
        "description": data["feedback"],
        "color": 3306460
    }
    await app.session.post(
        WEBHOOK_URLS["feature"],
        headers={
            "Content-Type": "application/json"
        },
        json={
            "embeds": [embed]
        }
    )

async def send_bug(data):
    embed = {
        "title": "Bug Report",
        "description": f"Bug Type: {data['bugType']}",
        "color": 15812200,
        "fields": [
            { "name": "Description", "value": data["issue"] },
            { "name": "Expected", "value": data["expected"] }
        ]
    }
    await app.session.post(
        WEBHOOK_URLS["bug"],
        headers={
            "Content-Type": "application/json"
        },
        json={
            "embeds": [embed]
        }
    )

