from utils.logger import logger

async def start_handler(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"

    logger.info(f"User {user_id} ({username}) started the bot")

    welcome_message = (
        "Здравствуйте! Я информационный ассистент по вопросам самозанятости (НПД).\n\n"
        "Я могу помочь вам с вопросами о:\n"
        "- Регистрации самозанятого\n"
        "- Ставках налога (4% и 6%)\n"
        "- Лимите дохода 2,4 млн рублей\n"
        "- Формировании чеков\n"
        "- Прекращении статуса НПД\n\n"
        "Просто задайте свой вопрос текстом.\n\n"
        "Используйте /help для получения дополнительной информации."
    )

    try:
        await update.message.reply_text(welcome_message)
    except Exception as e:
        logger.error(f"Error sending start message: {e}")
