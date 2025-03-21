from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.types import ChatMemberUpdated

from app.database.models import UserChatSubscription, User
from app.utils.constants import ChatAction
from app.utils.markups import user_join_chat_markup, user_subscribe_chat_markup
from app.loader import user_chat_subscription_repository, bot, user_repository
from app.utils.patterns import USER_JOIN_CHAT_PATTERN, USER_LEAVE_CHAT_PATTERN, BOT_JOINED_NEW_CHAT_PATTERN

router = Router()
router.my_chat_member.filter(F.chat.type == ChatType.CHANNEL)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bot_join_chat(event: ChatMemberUpdated):
    admins = await bot.get_chat_administrators(event.chat.id)
    users = await user_repository.filter(User.id.in_([admin.user.id for admin in admins]))
    markup = user_subscribe_chat_markup(event.chat, ChatAction.subscribe)
    for user in users:
        await bot.send_message(
            user.id,
            BOT_JOINED_NEW_CHAT_PATTERN.format(channel_title=event.chat.title),
            reply_markup=markup
        )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def bot_leave_chat(event: ChatMemberUpdated):
    await user_chat_subscription_repository.delete(chat_id=event.chat.id)


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def user_join_chat(event: ChatMemberUpdated):
    subscriptions = await user_chat_subscription_repository.filter(chat_id=event.chat.id)
    for subscription in subscriptions:
        subscription: UserChatSubscription
        await bot.send_message(
            subscription.user_id,
            USER_JOIN_CHAT_PATTERN.format(
                user_full_name=event.new_chat_member.user.full_name, channel_title=event.chat.title
            ),
            reply_markup=await user_join_chat_markup(user=event.new_chat_member.user, chat=event.chat)
        )


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def user_leave_chat(event: ChatMemberUpdated):
    subscriptions = await user_chat_subscription_repository.filter(chat_id=event.chat.id)
    for subscription in subscriptions:
        subscription: UserChatSubscription
        await bot.send_message(
            subscription.user_id,
            USER_LEAVE_CHAT_PATTERN.format(
                user_full_name=event.new_chat_member.user.full_name, channel_title=event.chat.title
            ),
            reply_markup=await user_join_chat_markup(user=event.new_chat_member.user, chat=event.chat)
        )
