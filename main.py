"""Бот для голосования за следующий пост в Telegram канале.

Version: 0.1
"""

import asyncio
from typing import Callable, Awaitable, Any

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, Update, ErrorEvent,
                           SwitchInlineQueryChosenChat)
from loguru import logger

import config


dp = Dispatcher()


## Если вы хотите отключить логгирование в боте
## Закомментируйте необходимые вам декораторы
@dp.message.middleware()
@dp.callback_query.middleware()
async def log_middleware(
    handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: dict[str, Any],
) -> Any:
    """Отслеживает полученные ботом сообщения и callback query."""
    if isinstance(event, CallbackQuery):
        logger.info("[c] {}: {}", event.message.from_user.id, event.data)
    else:
        logger.info("[m] {}: {}", event.chat.id, event.text)

    return await handler(event, data)


# Вспомогательные фкнкции
# =======================

def get_vote_markup(posts: list[dict]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=ic(x["topic"]), callback_data=f"vote:{i}")]
        for i, x in enumerate(posts)
    ])


# Команды для администраторов бота
# ================================

@dp.message(Command("github"))
async def github_commend(message: Message, bot: Bot):
    """Отправляет ссылку на исходный код проекта."""
    await message.answer((
        "🛠️ Ссылка на репозиторий бота: "
        "https://github.com/Microvolna/masterskaya-voiting"
    ))

@dp.message(Command("start"))
async def start_command(message: Message, bot: Bot) -> None:
    """Отправляет сообщение с голосованием в канал."""
    if str(message.from_user.id) == config.admin_id:
        await bot.send_message(config.chanel_id,
            config.message_text,
            reply_markup=get_vote_markup(config.posts)
        )
        await message.answer("✅ Голосование отправлено!")
    else:
        await message.answer("👋😌🌄 Кажется вы не администратор.")

@dp.message(Command("send_post"))
async def send_post_command(message: Message, bot: Bot) -> None:
    """Завершает голосование и отправляет победивший пост."""
    if str(message.from_user.id) == config.admin_id:
        send_post = config.posts[0]

        # Получем пост с наибольшим числом голосов
        for post in config.posts[1:]:
            if len(post['vote']) > len(send_post['vote']):
                send_post = post

        await bot.send_message(config.chanel_id, send_post["text"])
        await message.answer(f"📝 Пост {send_post['topic']} отправлен!")

    else:
        await message.answer("👋😌🌄 Кажется вы не администратор.")


# Команды для обычных пользователей
# =================================

@dp.message(Command("stats"))
async def stats_commend(message: Message) -> None:
    """Отображает статистику голосования."""
    text = "🌟 Статистика голосования:\n"
    total_votes = 0

    for i, x in enumerate(sorted(
        config.posts,
        key=lambda x: len(x["vote"]),
        reverse=True
    )):
        text += f"\n-- {i+1}. {x['topic']} -- {len(x['vote'])}"
        total_votes += len(x["vote"])

    await message.answer(text)


# Обработка голосования
# =====================

class VoteCallback(CallbackData, prefix="vote"):
    post_index: int

@dp.callback_query(VoteCallback.filter())
async def vote_callback(query: CallbackQuery, callback_data: VoteCallback):
    """Обрабатывает все входящие голоса."""
    selected_post = config.posts[callback_data.post_index]

    if query.from_user.id not in selected_post['vote']:
        selected_post['vote'].append(query.from_user.id)
        await query.answer(f"Вы 🌟 за: {selected_post['topic']}")
    else:
        selected_post['vote'].remove(query.from_user.id)
        await query.answer(f"Отмена 🌟 за: {selected_post['topic']}")


@dp.errors()
async def error_handler(exception: ErrorEvent) -> None:
    """Ловит и обрабатывает все исключения."""
    logger.exception(exception.exception)


async def main():
    """Загружает бота и запускает обработку сообщений."""
    bot = Bot(config.token)

    logger.info("Start polling ...")
    await dp.start_polling(bot)


# Запуска бота
# ============

if __name__ == "__main__":
    asyncio.run(main())
