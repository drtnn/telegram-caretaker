from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, User, Chat

from app.loader import bot
from app.utils.constants import ChatAction, chat_action_names


class ChatActionCallbackData(CallbackData, prefix="chat-action"):
    action: ChatAction
    chat_id: int


async def user_join_chat_markup(user: User, chat: Chat) -> InlineKeyboardMarkup:
    chat_invite_link = f"https://t.me/{chat.username}" if chat.username else await bot.export_chat_invite_link(chat.id)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👤 " + user.full_name, url=f"tg://user?id={user.id}"),
                InlineKeyboardButton(text="💬 " + chat.title, url=chat_invite_link)
            ]
        ]
    )


def user_subscribe_chat_markup(chat: Chat, action: ChatAction) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=chat_action_names[action],
                    callback_data=ChatActionCallbackData(action=action, chat_id=chat.id).pack()
                )
            ]
        ]
    )
