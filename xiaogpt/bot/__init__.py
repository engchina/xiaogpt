from __future__ import annotations

from xiaogpt.bot.base_bot import BaseBot
from xiaogpt.bot.chatgptapi_bot import ChatGPTBot
from xiaogpt.bot.gpt3_bot import GPT3Bot
from xiaogpt.bot.newbing_bot import NewBingBot
from xiaogpt.bot.slackclaude_bot import SlackClaudeBot
from xiaogpt.config import Config

BOTS: dict[str, type[BaseBot]] = {
    "gpt3": GPT3Bot,
    "newbing": NewBingBot,
    "chatgptapi": ChatGPTBot,
    "slackclaude": SlackClaudeBot,
}


def get_bot(config: Config) -> BaseBot:
    try:
        return BOTS[config.bot].from_config(config)
    except KeyError:
        raise ValueError(f"Unsupported bot {config.bot}, must be one of {list(BOTS)}")


__all__ = ["GPT3Bot", "ChatGPTBot", "NewBingBot", "SlackClaudeBot", "get_bot"]
