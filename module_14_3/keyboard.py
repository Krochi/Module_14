from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def create_bot_keyboard():
    bot_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button_buy = KeyboardButton(text="Купить")
    button_calculate = KeyboardButton(text="Рассчитать")
    button_info = KeyboardButton(text="Информация")
    bot_kb.add(button_calculate, button_info, button_buy)
    return bot_kb


def create_inline_product_keyboard():
    inline_kb_products = InlineKeyboardMarkup(row_width=4)
    inline_kb_products.row(
    InlineKeyboardButton(text="Product1", callback_data="product_1"),
            InlineKeyboardButton(text="Product2", callback_data="product_2"),
            InlineKeyboardButton(text="Product3", callback_data="product_3"),
            InlineKeyboardButton(text="Product4", callback_data="product_4")
        )

    return inline_kb_products


def create_inline_price_keyboard(product_id):
    prices = {
        "1": "1000 руб",
        "2": "1200 руб",
        "3": "900 руб",
        "4": "1700 руб"
    }
    inline_kb_prices = InlineKeyboardMarkup(row_width=1)
    inline_kb_prices.add(
        InlineKeyboardButton(text=prices[product_id], callback_data=f"price_{product_id}")
    )
    return inline_kb_prices


