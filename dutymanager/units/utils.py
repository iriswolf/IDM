"""

Tools for vk-bot

"""

from module import Blueprint
from typing import Optional

bp = Blueprint()

__all__ = (
    "get_chat", "send_msg",
    "get_msg_id", "get_msg_ids",
    "get_history", "edit_msg",
    "get_attachments",
    "bp"
)


async def get_attachments(message_id: int) -> Optional[str]:
    attachments = []
    data = (await bp.api.request("messages.getById", {
        "message_ids": message_id
    }))["items"][0]
    if not data["attachments"]:
        return
    for x in data["attachments"]:
        kind = x["type"]
        if kind != "link":
            attachments.append(
                f"{kind}{x[kind]['owner_id']}_{x[kind]['id']}"
            )
    return ",".join(attachments)


async def get_history(peer_id: int, count: int = 200) -> dict:
    history = (await bp.api.request("messages.getHistory", {
        "peer_id": peer_id, "count": count
    }))["items"]
    return history


async def get_msg_ids(peer_id: int, local_ids: list) -> list:
    data = await bp.api.messages.get_by_conversation_message_id(
        peer_id=peer_id,
        conversation_message_ids=local_ids
    )
    return [str(i['id']) for i in data.items if "action" not in i]


async def get_msg_id(peer_id: int, local_id: int) -> int:
    data = await bp.api.messages.get_by_conversation_message_id(
        peer_id=peer_id,
        conversation_message_ids=local_id
    )
    return data.items[0]['id']


async def send_msg(
    peer_id: int,
    message: str,
    attachment: str = None,
    disable_mentions: bool = True,
    **kwargs
):
    await bp.api.messages.send(
        peer_id=peer_id,
        message=message,
        attachment=attachment,
        disable_mentions=disable_mentions,
        random_id=0,
        **kwargs
    )


async def edit_msg(
    peer_id: int,
    message_id: int,
    message: str,
    attachment: int = None
):
    await bp.api.messages.edit(
        **locals(), keep_forward_messages=True
    )


async def get_chat(date: int, text: str = "!связать") -> int:
    data = (await bp.api.request("messages.search", {
        "q": text, "count": 5
    }))["items"]
    for i in data:
        if i["date"] == date:
            return i["peer_id"]


