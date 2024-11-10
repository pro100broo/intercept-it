import os
import asyncio

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from intercept_it.loggers.base_logger import BaseLogger


def execute_synchronously(function):
    """ Async initializer for the Telegram Bot methods """

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(function(*args, **kwargs))

    return wrapper


class TGLogger(BaseLogger):
    def __init__(self):
        self._get_bot_secrets()
        self._bot = Bot(token=self._token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    def _get_bot_secrets(self) -> None:
        load_dotenv()
        self._chat_id = os.environ.get("INTERCEPT_IT_TG_CHAT_ID")
        self._thread_id = os.environ.get("INTERCEPT_IT_TG_THREAD_ID")
        self._token = os.environ.get("INTERCEPT_IT_TG_BOT_TOKEN")

    @execute_synchronously
    async def save_logs(self, message: str):
        """
        Sends custom exception information to the Telegram Bot

        :param exception: Target exception model
        """

        await self._bot.send_message(
            chat_id=self._chat_id,
            message_thread_id=self._thread_id,
            text=f"Got an error: {message}",
            parse_mode=ParseMode.MARKDOWN_V2
        )
