from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from handlers import start, button_handler, add_expense_handler, calculate_budget_handler, cancel, admin_add_command, \
    admin_add_date_handler, admin_add_amount_handler
from database import init_db

# Состояния для ConversationHandler
CHOOSING, ADD_EXPENSE, CALCULATE_BUDGET, ADMIN_ADD_DATE, ADMIN_ADD_AMOUNT = range(5)

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
                CallbackQueryHandler(button_handler)  # Обработка кнопок главного меню
            ],
            ADD_EXPENSE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_expense_handler)  # Ожидание ввода суммы расхода
            ],
            CALCULATE_BUDGET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_budget_handler)  # Ожидание ввода бюджета
            ],
            ADMIN_ADD_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_add_date_handler)  # Ожидание ввода даты
            ],
            ADMIN_ADD_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_add_amount_handler)  # Ожидание ввода суммы
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],  # Отмена операции
        allow_reentry=True  # Разрешаем повторный вход в диалог
    )

    # Добавляем обработчик для админской команды /add
    application.add_handler(CommandHandler('add', admin_add_command))

    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()