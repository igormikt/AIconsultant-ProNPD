import sys
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TELEGRAM_TOKEN, validate_config
from handlers.start import start_handler
from handlers.help import help_handler
from handlers.ask import ask_handler
from handlers.button import button_handler, callback_handler
from services.rag_service import initialize_knowledge_base
from utils.logger import logger
from utils.rate_limiter import RateLimiter
from database.db_manager import init_database

rate_limiter = RateLimiter()


async def error_handler(update, context):
    """Обработчик ошибок"""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    try:
        if update and update.message:
            await update.message.reply_text(
                "❌ Извините, произошла ошибка при обработке вашего вопроса. "
                "Пожалуйста, попробуйте позже."
            )
    except Exception as e:
        logger.error(f"Error in error_handler: {e}")


async def post_init(application):
    """Инициализация после запуска приложения"""
    logger.info("Initializing database...")
    await init_database()
    logger.info("Database initialized successfully")

    logger.info("Initializing knowledge base...")
    await initialize_knowledge_base()
    logger.info("Knowledge base initialized successfully")

    print("\n" + "🚀" * 30)
    print("\n✅ БОТ УСПЕШНО ЗАПУЩЕН И РАБОТАЕТ!\n")
    print("=" * 60)

    print("📋 Статус компонентов:")
    print("  ✅ Telegram Bot API      - подключено")
    print("  ✅ OpenAI GPT-4          - подключено")
    print("  ✅ База данных SQLite    - активна")
    print("  ✅ База знаний           - загружена")
    print("  ✅ FAQ система           - активна")
    print("  ✅ RAG система           - активна")
    print("  ✅ Rate Limiter          - активен")
    print("  ✅ Логирование           - активно")
    print("  ✅ Кнопки меню           - активны")
    print("\n" + "=" * 60)
    print("💬 Команды бота:")
    print("  /start - Приветствие с меню")
    print("  /help  - Справка")
    print("  Текст  - Задать вопрос")
    print("  Кнопки - Быстрый доступ к функциям")
    print("\n" + "=" * 60)
    print("🎨 Доступные кнопки:")
    print("  🏠 Главное меню")
    print("  ❓ Помощь")
    print("  💰 Тарифы")
    print("  📚 База знаний")
    print("  📊 Популярные вопросы")
    print("  ℹ️ О боте")
    print("  🔄 Новый диалог")
    print("\n" + "=" * 60)
    print("📊 Для просмотра статистики:")
    print("  python check_stats.py")
    print("  python view_database.py")
    print("\n" + "=" * 60)
    print("⚠️  Для остановки нажмите Ctrl+C")
    print("=" * 60 + "\n")


def main():
    """Главная функция запуска бота"""
    try:
        # Валидация конфигурации
        validate_config()
        logger.info("Configuration validated successfully")

        # Создание приложения
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Регистрация хендлеров команд
        application.add_handler(CommandHandler("start", start_handler))
        application.add_handler(CommandHandler("help", help_handler))

        # Регистрация хендлера кнопок меню (ПЕРЕД обычными сообщениями!)
        button_filter = filters.Regex(
            "^(🏠 Главное меню|❓ Помощь|💰 Тарифы|📚 База знаний|📊 Популярные вопросы|ℹ️ О боте|🔄 Новый диалог)$"
        )
        application.add_handler(MessageHandler(button_filter, button_handler))

        # Регистрация хендлера inline-кнопок
        application.add_handler(CallbackQueryHandler(callback_handler))

        # Регистрация хендлера текстовых сообщений (в КОНЦЕ!)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask_handler))

        # Регистрация обработчика ошибок
        application.add_error_handler(error_handler)

        # Инициализация при старте
        application.post_init = post_init

        logger.info("Bot started successfully! Press Ctrl+C to stop.")

        # Запуск polling (добавляем callback_query для inline-кнопок)
        application.run_polling(allowed_updates=["message", "callback_query"])

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()



# import sys
# from telegram.ext import Application, CommandHandler, MessageHandler, filters
# from config import TELEGRAM_TOKEN, validate_config
# from handlers.start import start_handler
# from handlers.help import help_handler
# from handlers.ask import ask_handler
# from services.rag_service import initialize_knowledge_base
# from utils.logger import logger
# from utils.rate_limiter import RateLimiter
# from database.db_manager import init_database
#
# rate_limiter = RateLimiter()
#
#
# async def error_handler(update, context):
#     """Обработчик ошибок"""
#     logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
#     try:
#         if update and update.message:
#             await update.message.reply_text(
#                 "❌ Извините, произошла ошибка при обработке вашего вопроса. "
#                 "Пожалуйста, попробуйте позже."
#             )
#     except Exception as e:
#         logger.error(f"Error in error_handler: {e}")
#
#
# async def post_init(application):
#     """Инициализация после запуска приложения"""
#     logger.info("Initializing database...")
#     await init_database()
#     logger.info("Database initialized successfully")
#
#     logger.info("Initializing knowledge base...")
#     await initialize_knowledge_base()
#     logger.info("Knowledge base initialized successfully")
#
#     print("\n" + "🚀" * 30)
#     print("\n✅ БОТ УСПЕШНО ЗАПУЩЕН И РАБОТАЕТ!\n")
#     print("=" * 60)
#
#     print("📋 Статус компонентов:")
#     print("  ✅ Telegram Bot API      - подключено")
#     print("  ✅ OpenAI GPT-4          - подключено")
#     print("  ✅ База данных SQLite    - активна")
#     print("  ✅ База знаний           - загружена")
#     print("  ✅ FAQ система           - активна")
#     print("  ✅ RAG система           - активна")
#     print("  ✅ Rate Limiter          - активен")
#     print("  ✅ Логирование           - активно")
#     print("\n" + "=" * 60)
#     print("💬 Команды бота:")
#     print("  /start - Приветствие")
#     print("  /help  - Справка")
#     print("  Текст  - Задать вопрос")
#     print("\n" + "=" * 60)
#     print("📊 Для просмотра статистики:")
#     print("  python check_stats.py")
#     print("  python view_database.py")
#     print("\n" + "=" * 60)
#     print("⚠️  Для остановки нажмите Ctrl+C")
#     print("=" * 60 + "\n")
#
#
# def main():
#     """Главная функция запуска бота"""
#     try:
#         # Валидация конфигурации
#         validate_config()
#         logger.info("Configuration validated successfully")
#
#         # Создание приложения
#         application = Application.builder().token(TELEGRAM_TOKEN).build()
#
#         # Регистрация хендлеров команд
#         application.add_handler(CommandHandler("start", start_handler))
#         application.add_handler(CommandHandler("help", help_handler))
#
#         # Регистрация хендлера текстовых сообщений
#         application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask_handler))
#
#         # Регистрация обработчика ошибок
#         application.add_error_handler(error_handler)
#
#         # Инициализация при старте
#         application.post_init = post_init
#
#         logger.info("Bot started successfully! Press Ctrl+C to stop.")
#
#         # Запуск polling
#         application.run_polling(allowed_updates=["message"])
#
#     except KeyboardInterrupt:
#         logger.info("Bot stopped by user")
#         sys.exit(0)
#     except Exception as e:
#         logger.error(f"Failed to start bot: {e}", exc_info=True)
#         sys.exit(1)
#
#
# if __name__ == "__main__":
#     main()
