from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient
from xiaogpt.config import (
    Config,
)
import asyncio


class SlackClient(AsyncWebClient):
    CHANNEL_ID = None

    async def open_channel(self):
        if not self.CHANNEL_ID:
            response = await self.conversations_open(users=Config.slack_claude_bot_id)
            self.CHANNEL_ID = response["channel"]["id"]

    async def chat(self, text):
        if not self.CHANNEL_ID:
            raise Exception("Channel not found.")

        resp = await self.chat_postMessage(channel=self.CHANNEL_ID, text=text)
        self.LAST_TS = resp["ts"]

    async def get_slack_messages(self):
        try:
            # TODO：暂时不支持历史消息，因为在同一个频道里存在多人使用时历史消息渗透问题
            resp = await self.conversations_history(channel=self.CHANNEL_ID, oldest=self.LAST_TS, limit=1)
            msg = [msg for msg in resp["messages"]
                   if msg.get("user") == Config.slack_claude_bot_id]
            return msg
        except (SlackApiError, KeyError) as e:
            raise RuntimeError(f"获取Slack消息失败。")

    async def get_reply(self):
        while True:
            slack_msgs = await self.get_slack_messages()
            if len(slack_msgs) == 0:
                await asyncio.sleep(0.5)
                continue

            msg = slack_msgs[-1]
            if msg["text"].endswith("Typing…_"):
                yield False, msg["text"]
            else:
                yield True, msg["text"]
                break
