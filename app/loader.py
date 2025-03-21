from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.database.repositories import UserChatSubscriptionRepository, UserRepository

from app.config import settings

bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

user_chat_subscription_repository = UserChatSubscriptionRepository()
user_repository = UserRepository()
