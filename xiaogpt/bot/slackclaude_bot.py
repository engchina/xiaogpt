from __future__ import annotations

from rich import print

from xiaogpt.bot.base_bot import BaseBot
from xiaogpt.slackclient import SlackClient
from xiaogpt.utils import split_sentences

import asyncio

class SlackClaudeBot(BaseBot):
    CHANNEL_ID = None
    LAST_TS = None
    def __init__(
        self,
        slack_claude_user_token,
    ):
        self.history = []
        self.client = SlackClient(token=slack_claude_user_token)


    @classmethod
    def from_config(cls, config):
        return cls(
            slack_claude_user_token=config.slack_claude_user_token,
        )

    async def ask(self, query, **options):
        await self.client.open_channel()
        await self.client.chat(query)

        async for text in self.client.get_reply():
            if text[0]:
                print(text[1])
                return text[1]

    async def ask_stream(self, query, **options):
        print('ToDo') 
