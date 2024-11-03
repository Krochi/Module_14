# Задача "Продуктовая база"
# Создайте файл crud_functions.py и напишите там следующие функции:
# initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:
# id - целое число, первичный ключ
# title(название продукта) - текст (не пустой)
# description(описание) - текст
# price(цена) - целое число (не пустой)
# get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.
#
# Изменения в Telegram-бот:
# В самом начале запускайте ранее написанную функцию get_all_products.
# Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов функцию
# get_all_products. Полученные записи используйте в выводимой надписи:
# "Название: <title> | Описание: <description> | Цена: <price>"
# Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
#
# Примечания:
# Название продуктов и картинок к ним можете выбрать самостоятельно. (Минимум 4)

#Решение:

from config import API_TOKEN
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from crud_functions import initiate_db, populate_initial_products, get_all_products
from keyboard import create_bot_keyboard, create_inline_product_keyboard, create_inline_price_keyboard


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

initiate_db()
populate_initial_products()


bot_kb = create_bot_keyboard()
inline_kb_products = create_inline_product_keyboard()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=bot_kb)


@dp.message_handler(text="Рассчитать")
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb_products)


@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    products = get_all_products()
    for i, product in enumerate(products, start=1):
        product_id, title, description, price = product

        await message.answer_photo(
            open(f"product{i}.jpg", "rb"),
            caption=f'Название: {title} | Описание: {description} | Цена: {price} руб.'
        )

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_kb_products)

@dp.callback_query_handler(lambda call: call.data.startswith("product_"))
async def select_product(call: types.CallbackQuery):
    product_id = call.data.split("_")[1]
    inline_kb_prices = create_inline_price_keyboard(product_id)
    await call.message.answer(f"Цена для Product{product_id}:", reply_markup=inline_kb_prices)


@dp.callback_query_handler(lambda call: call.data.startswith("price_"))
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост (в сантиметрах):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес (в килограммах):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    form = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Ваша норма калорий: {form:.2f} ккал/день')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




