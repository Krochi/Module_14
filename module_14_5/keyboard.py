from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def create_bot_keyboard():
    bot_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button_buy = KeyboardButton(text="Купить")
    button_calculate = KeyboardButton(text="Рассчитать")
    button_info = KeyboardButton(text="Информация")
    button_reg = KeyboardButton(text="Регистрация")
    bot_kb.add(button_calculate, button_info, button_buy, button_reg)
    return bot_kb


def create_inline_product_keyboard():
    inline_kb_products = InlineKeyboardMarkup(row_width=2)
    for i in range(1, 5):
        inline_kb_products.add(
            InlineKeyboardButton(text=f"Product{i}", callback_data=f"product_{i}")
        )

    return inline_kb_products


def create_inline_price_keyboard(product_id):
    prices = {
        "1": "100 руб",
        "2": "200 руб",
        "3": "300 руб",
        "4": "400 руб"
    }
    inline_kb_prices = InlineKeyboardMarkup(row_width=1)
    inline_kb_prices.add(
        InlineKeyboardButton(text=prices[product_id], callback_data=f"price_{product_id}")
    )
    return inline_kb_prices


