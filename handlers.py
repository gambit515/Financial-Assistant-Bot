# handlers.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database import add_expense, get_total_expenses, get_monthly_expenses
from utils import format_month_year, calculate_budget_distribution

# Состояния для ConversationHandler
CHOOSING, ADD_EXPENSE, CALCULATE_BUDGET = range(3)

# Тексты для справочной информации
FINANCIAL_LITERACY_TEXT = """
Правила, которые позволят вам повысить уровень финансовой грамотности:
1) Сформируйте подушку безопасности.
2) Ведите ежемесячный бюджет.
3) Измените отношение к покупкам.
4) Держите персональные данные в сохранности.
5) Получайте льготы от государства.
"""

SAVING_MONEY_TEXT = """
Как копить деньги, если у вас небольшой доход?
- Оставляйте на счёте «круглые» суммы.
- Складывайте мелочь в копилку.
- Используйте копилку-таблицу.

Как накопить деньги быстро?
- Откладывайте не меньше 10% от доходов.
- Каждый месяц откладывайте больше, чем в предыдущий.
- Откажитесь от одной статьи расходов.
"""


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем инлайн-кнопки
    keyboard = [
        [InlineKeyboardButton("Учет расходов 💸", callback_data="add_expense")],
        [InlineKeyboardButton("Показать общую сумму 💰", callback_data="show_total")],
        [InlineKeyboardButton("Статистика по месяцам 📅", callback_data="monthly_stats")],
        [InlineKeyboardButton("Рассчитать бюджет на месяц 🧮", callback_data="calculate_budget")],
        [InlineKeyboardButton("Справочная информация ℹ️", callback_data="info_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Проверяем, был ли вызов из CallbackQuery (нажатие кнопки) или из команды /start
    if update.callback_query:
        query = update.callback_query
        await query.answer()  # Подтверждаем обработку запроса
        await query.edit_message_text("Выберите действие:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

    return CHOOSING


# Обработка нажатий на инлайн-кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Подтверждаем обработку запроса

    user_id = query.from_user.id
    data = query.data

    if data == "add_expense":
        # Добавляем кнопку "Возврат в главное меню"
        await query.edit_message_text("Введите сумму расхода:")
        return ADD_EXPENSE
    elif data == "show_total":
        total = get_total_expenses(user_id)
        keyboard = [[InlineKeyboardButton("Возврат в главное меню 🏠", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"Общая сумма ваших расходов: {total:.2f}", reply_markup=reply_markup)
        return CHOOSING
    elif data == "monthly_stats":
        monthly_expenses = get_monthly_expenses(user_id)
        if monthly_expenses:
            response = "Ваши расходы по месяцам:\n"
            for month_key, total in monthly_expenses:
                formatted_month = format_month_year(month_key)
                response += f"{formatted_month}: {total:.2f}\n"
        else:
            response = "Нет данных о расходах."
        keyboard = [[InlineKeyboardButton("Возврат в главное меню 🏠", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup)
        return CHOOSING
    elif data == "calculate_budget":
        keyboard = [[InlineKeyboardButton("Возврат в главное меню 🏠", callback_data="main_menu")]]
        await query.edit_message_text("Введите общий бюджет на месяц:")
        return CALCULATE_BUDGET
    elif data == "info_menu":
        # Меню справочной информации
        keyboard = [
            [InlineKeyboardButton("Как повысить финансовую грамотность?", callback_data="financial_literacy")],
            [InlineKeyboardButton("Как начать копить?", callback_data="saving_money")],
            [InlineKeyboardButton("Возврат в главное меню 🏠", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите раздел справочной информации:", reply_markup=reply_markup)
        return CHOOSING
    elif data == "financial_literacy":
        # Вывод текста о финансовой грамотности
        keyboard = [
            [InlineKeyboardButton("Назад ⬅️", callback_data="info_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(FINANCIAL_LITERACY_TEXT, reply_markup=reply_markup)
        return CHOOSING
    elif data == "saving_money":
        # Вывод текста о том, как начать копить
        keyboard = [
            [InlineKeyboardButton("Назад ⬅️", callback_data="info_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(SAVING_MONEY_TEXT, reply_markup=reply_markup)
        return CHOOSING
    elif data == "main_menu":
        # Возвращаемся в главное меню
        return await start(update, context)


# Добавление расхода
async def add_expense_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
        user_id = update.message.from_user.id
        add_expense(user_id, amount)

        # Добавляем кнопку "Возврат в главное меню"
        keyboard = [[InlineKeyboardButton("Возврат в главное меню 🏠", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Расход {amount:.2f} добавлен.", reply_markup=reply_markup)
    except ValueError:
        await update.message.reply_text("Неверный формат суммы. Пожалуйста, введите число.")

    return CHOOSING


# Расчет бюджета
async def calculate_budget_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        budget = float(update.message.text)
        if budget <= 0:
            raise ValueError()

        response = calculate_budget_distribution(budget)

        # Добавляем кнопку "Возврат в главное меню"
        keyboard = [[InlineKeyboardButton("Возврат в главное меню 🏠", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(response, reply_markup=reply_markup)
    except ValueError:
        await update.message.reply_text("Неверный формат бюджета. Пожалуйста, введите положительное число.")

    return CHOOSING


# Отмена операции
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END