# utils.py

def format_month_year(month_key):
    """Преобразует ключ месяца YYYY-MM в формат 'название месяца (год)'."""
    year, month = map(int, month_key.split('-'))
    month_names = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    return f"{month_names[month - 1]} ({year})"

def calculate_budget_distribution(budget):
    """Рассчитывает распределение бюджета по категориям."""
    groceries = budget * 0.45
    hygiene_household = budget * 0.15
    transport_education = budget * 0.15
    personal_entertainment = budget * 0.20
    savings = budget * 0.15

    return (
        f"Распределение бюджета на месяц ({budget:.2f}):\n"
        f"- Продукты: {groceries:.2f}\n"
        f"- Товары личной гигиены и бытовые расходы: {hygiene_household:.2f}\n"
        f"- Расходы на проезд, товары для учебы: {transport_education:.2f}\n"
        f"- Личные цели и развлечения: {personal_entertainment:.2f}\n"
        f"- В копилку (отложить): {savings:.2f}"
    )