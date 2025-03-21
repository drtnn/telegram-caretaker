from re import Match

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters.command import CommandStart
from aiogram.types import CallbackQuery, Message, ChatInviteLink

from app.database.models import UserChatSubscription, User
from app.loader import user_chat_subscription_repository, bot, user_repository
from app.utils.constants import ChatAction
from app.utils.markups import ChatActionCallbackData, user_subscribe_chat_markup
from app.utils.patterns import ADMIN_SUBSCRIBED_CHAT_PATTERN, ADMIN_UNSUBSCRIBED_CHAT_PATTERN, START_MESSAGE_PATTERN

router = Router()
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.message(CommandStart())
async def user_start_command(message: Message):
    await user_repository.get_or_create(
        User(id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name),
        filter_kwargs={"id": message.from_user.id}
    )
    await message.answer(START_MESSAGE_PATTERN)


# @router.message(F.text.regexp(r"t\.me/(joinchat/)?([^/]+)").as_("invite_link"))
# async def user_link(message: Message, invite_link: Match[str]):
#     invite = ChatInviteLink(invite_link=str(invite_link), )
#     await bot.get_chat()


@router.callback_query(ChatActionCallbackData.filter(F.action == ChatAction.subscribe))
async def admin_subscribe_chat(query: CallbackQuery, callback_data: ChatActionCallbackData):
    await user_chat_subscription_repository.create(
        UserChatSubscription(chat_id=callback_data.chat_id, user_id=query.from_user.id)
    )
    chat = await bot.get_chat(callback_data.chat_id)
    await query.message.edit_text(
        text=ADMIN_SUBSCRIBED_CHAT_PATTERN.format(channel_title=chat.title),
        reply_markup=user_subscribe_chat_markup(chat, ChatAction.unsubscribe)
    )


@router.callback_query(ChatActionCallbackData.filter(F.action == ChatAction.unsubscribe))
async def admin_unsubscribe_chat(query: CallbackQuery, callback_data: ChatActionCallbackData):
    await user_chat_subscription_repository.delete(chat_id=callback_data.chat_id, user_id=query.from_user.id)
    chat = await bot.get_chat(callback_data.chat_id)
    await query.message.edit_text(
        text=ADMIN_UNSUBSCRIBED_CHAT_PATTERN.format(channel_title=chat.title),
        reply_markup=user_subscribe_chat_markup(chat, ChatAction.subscribe)
    )
