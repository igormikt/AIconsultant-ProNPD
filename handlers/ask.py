from services.faq_service import check_typical_question
from services.rag_service import generate_answer
from utils.logger import logger
from utils.token_control import count_tokens
from database.db_manager import save_user, save_question


async def ask_handler(update, context):
    """Обработчик текстовых вопросов пользователя"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    first_name = update.effective_user.first_name or ""
    last_name = update.effective_user.last_name or ""
    user_question = update.message.text

    logger.info(f"User {user_id} ({username}) asked: {user_question[:100]}...")

    # Сохранить пользователя в БД
    try:
        await save_user(user_id, username, first_name, last_name)
    except Exception as e:
        logger.error(f"Failed to save user to database: {e}")

    try:
        # 1. Проверка FAQ (БЕЗ токенов)
        faq_answer = check_typical_question(user_question)
        if faq_answer:
            logger.info(f"FAQ answer provided for user {user_id}")
            await update.message.reply_text(faq_answer)

            # Сохранить вопрос в БД
            try:
                await save_question(
                    user_id=user_id,
                    question=user_question,
                    answer=faq_answer,
                    answer_type='faq',
                    tokens_used=0
                )
            except Exception as e:
                logger.error(f"Failed to save question to database: {e}")

            return

        # 2. RAG ответ (с токенами)
        logger.info(f"Processing RAG query for user {user_id}")

        # Отправить сообщение о начале обработки
        processing_message = await update.message.reply_text("🔍 Ищу информацию в базе знаний...")

        try:
            answer = await generate_answer(user_question)

            # Удалить сообщение о обработке
            await processing_message.delete()

            # Отправить ответ
            await update.message.reply_text(answer)

            # Подсчитать токены
            tokens_used = count_tokens(user_question) + count_tokens(answer)
            logger.info(f"RAG answer successfully generated for user {user_id}, tokens used: {tokens_used}")

            # Сохранить вопрос в БД
            try:
                await save_question(
                    user_id=user_id,
                    question=user_question,
                    answer=answer,
                    answer_type='rag',
                    tokens_used=tokens_used
                )
            except Exception as e:
                logger.error(f"Failed to save question to database: {e}")

        except Exception as e:
            logger.error(f"Error generating RAG answer for user {user_id}: {e}", exc_info=True)
            await processing_message.delete()
            await update.message.reply_text(
                "❌ Извините, произошла ошибка при обработке вашего вопроса. "
                "Пожалуйста, попробуйте переформулировать вопрос или попробуйте позже."
            )

            # Сохранить ошибку в БД
            try:
                await save_question(
                    user_id=user_id,
                    question=user_question,
                    answer="[ERROR]",
                    answer_type='error',
                    tokens_used=0
                )
            except:
                pass

    except Exception as e:
        logger.error(f"Unexpected error in ask_handler for user {user_id}: {e}", exc_info=True)
        await update.message.reply_text(
            "❌ Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
        )
