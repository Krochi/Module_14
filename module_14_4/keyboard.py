from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def create_bot_keyboard():
    bot_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button_calculate = KeyboardButton(text="Рассчитать")
    button_info = KeyboardButton(text="Информация")
    button_buy = KeyboardButton(text="Купить")
    bot_kb.add(button_calculate, button_info, button_buy)
    return bot_kb


def create_inline_product_keyboard():
    inline_kb_products = InlineKeyboardMarkup(row_width=2)
    inline_kb_products.row(
InlineKeyboardButton(text="Product1", callback_data="product_buying_1"),
        InlineKeyboardButton(text="Product2", callback_data="product_buying_2"),
        InlineKeyboardButton(text="Product3", callback_data="product_buying_3"),
        InlineKeyboardButton(text="Product4", callback_data="product_buying_4"),
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
        InlineKeyboardButton(text=f"Подтвердить покупку {prices[product_id]}", callback_data=f"price_{product_id}")
    )
    return inline_kb_prices



