"""
Обработчик команды /start
"""
from telegram import Update
from telegram.ext import ContextTypes
from handlers.keyboards import get_main_menu_keyboard
from utils.logger import logger


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user

    welcome_message = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Я **AI-консультант по самозанятости (НПД)** с поддержкой GPT-4.\n\n"
        "🎯 **Я помогу вам разобраться с:**\n"
        "• Регистрацией самозанятости\n"
        "• Налогами и лимитами доходов\n"
        "• Отчётностью и платежами\n"
        "• Закрытием статуса НПД\n\n"
        "💬 **Задавайте любые вопросы или используйте кнопки меню!**"
    )

    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown',
        reply_markup=get_main_menu_keyboard()
    )

    logger.info(f"Пользователь {user.id} ({user.username}) запустил бота")

# from utils.logger import logger
#
# async def start_handler(update, context):
#     user_id = update.effective_user.id
#     username = update.effective_user.username or "Unknown"
#
#     logger.info(f"User {user_id} ({username}) started the bot")
#
#     welcome_message = (
#         "Здравствуйте! Я информационный ассистент по вопросам самозанятости (НПД).\n\n"
#         "Я могу помочь вам с вопросами о:\n"
#         "- Регистрации самозанятого\n"
#         "- Ставках налога (4% и 6%)\n"
#         "- Лимите дохода 2,4 млн рублей\n"
#         "- Формировании чеков\n"
#         "- Прекращении статуса НПД\n\n"
#         "Просто задайте свой вопрос текстом.\n\n"
#         "Используйте /help для получения дополнительной информации."
#     )
#
#     try:
#         await update.message.reply_text(welcome_message)
#     except Exception as e:
#         logger.error(f"Error sending start message: {e}")
