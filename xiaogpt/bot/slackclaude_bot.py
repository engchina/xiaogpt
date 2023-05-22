from __future__ import annotations

from rich import print

from xiaogpt.bot.base_bot import BaseBot
from xiaogpt.slackclient import SlackClient
from xiaogpt.utils import split_sentences

import re

_reference_link_re = re.compile(r"\[\d+\]: .+?\n+")


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

    @staticmethod
    def clean_text(s):
        s = s.replace("_Typing…_", "")
        # s = s.replace("**", "")
        # s = _reference_link_re.sub("", s)
        # s = re.sub(r"\[[\^\d]+\]", "", s)
        return s.strip()

    async def ask(self, query, **options):
        await self.client.open_channel()
        await self.client.chat(query)

        async for text in self.client.get_reply():
            if text[0]:
                print(text[1])
                return text[1]

    async def ask_stream(self, query, **options):
        await self.client.open_channel()
        await self.client.chat(query)

        completion = self.client.get_reply()

        async def text_gen():
            current = ""
            async for final, resp in completion:
                text = self.clean_text(resp)
                if text == "":
                    continue
                if text == current:
                    continue
                diff = text[len(current):]
                current = text
                is_a_sentence = False
                for x in (",", "。", "，", "？", "！", "；", "、", ".", "?", "!", ";"):
                    pos = diff.rfind(x)
                    if pos == -1:
                        is_a_sentence = True
                        break
                if is_a_sentence:
                    yield diff
                if final:
                    break

        try:
            async for sentence in split_sentences(text_gen()):
                print(sentence)
                yield sentence
        finally:
            print()
