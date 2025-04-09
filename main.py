# bot.py

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from handlers import start, button_handler, add_expense_handler, calculate_budget_handler, cancel
from database import init_db

# Состояния для ConversationHandler
CHOOSING, ADD_EXPENSE, CALCULATE_BUDGET = range(3)

# Основная функция
def main():
    # Инициализация базы данных
    init_db()

    # Создание приложения
    application = ApplicationBuilder().token("7952771531:AAGDTEgkj2ux8sXcx4vQeKOIcIEiuprhswU").build()

    # Определение обработчиков
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                CallbackQueryHandler(button_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_expense_handler)
            ],
            ADD_EXPENSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_expense_handler)],
            CALCULATE_BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_budget_handler)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()