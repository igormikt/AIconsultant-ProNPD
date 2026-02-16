from utils.logger import logger

async def help_handler(update, context):
    user_id = update.effective_user.id
    logger.info(f"User {user_id} requested help")

    help_message = (
        "Справка по использованию бота\n\n"
        "Я могу помочь по следующим темам:\n"
        "- Регистрация в качестве самозанятого\n"
        "- Налоговые ставки 4% и 6%\n"
        "- Лимит годового дохода 2,4 млн руб.\n"
        "- Правила формирования чеков\n"
        "- Прекращение статуса самозанятого\n"
        "- Общие вопросы по НПД\n\n"
        "Просто напишите ваш вопрос обычным текстом."
    )

    try:
        await update.message.reply_text(help_message)
    except Exception as e:
        logger.error(f"Error sending help message: {e}")
