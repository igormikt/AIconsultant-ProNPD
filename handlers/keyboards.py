"""
Клавиатуры для Telegram бота
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard():
    """Главное меню с кнопками"""
    keyboard = [
        [
            KeyboardButton("🏠 Главное меню"),
            KeyboardButton("❓ Помощь")
        ],
        [
            KeyboardButton("💰 Тарифы"),
            KeyboardButton("📚 База знаний")
        ],
        [
            KeyboardButton("📊 Популярные вопросы")
        ],
        [
            KeyboardButton("ℹ️ О боте"),
            KeyboardButton("🔄 Новый диалог")
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        input_field_placeholder="Задайте вопрос или выберите действие..."
    )


def get_inline_menu():
    """Inline-кнопки для быстрого доступа"""
    keyboard = [
        [
            InlineKeyboardButton("💰 Тарифы", callback_data="pricing"),
            InlineKeyboardButton("📚 База знаний", callback_data="knowledge")
        ],
        [
            InlineKeyboardButton("📊 FAQ", callback_data="faq"),
            InlineKeyboardButton("ℹ️ О боте", callback_data="about")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_topics_keyboard():
    """Клавиатура с темами базы знаний"""
    keyboard = [
        [InlineKeyboardButton("📝 Регистрация самозанятости", callback_data="topic_registration")],
        [InlineKeyboardButton("💸 Налоги и лимиты доходов", callback_data="topic_taxes")],
        [InlineKeyboardButton("📊 Отчётность и платежи", callback_data="topic_reporting")],
        [InlineKeyboardButton("❌ Закрытие самозанятости", callback_data="topic_closing")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_faq_keyboard():
    """Топ-5 популярных вопросов"""
    keyboard = [
        [InlineKeyboardButton("❓ Как зарегистрироваться?", callback_data="faq_registration")],
        [InlineKeyboardButton("💰 Какой лимит дохода?", callback_data="faq_limit")],
        [InlineKeyboardButton("📊 Как платить налог?", callback_data="faq_tax_payment")],
        [InlineKeyboardButton("🏦 Могу ли работать с организациями?", callback_data="faq_b2b")],
        [InlineKeyboardButton("❌ Как закрыть самозанятость?", callback_data="faq_close")],
        [InlineKeyboardButton("🔙 Назад в меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
