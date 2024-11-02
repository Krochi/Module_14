# Задача "Витамины для всех!"
# Создайте и дополните клавиатуры:
# В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
# Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
# У всех кнопок назначьте callback_data="product_buying"
# Создайте хэндлеры и функции к ним:
# Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
# Функция get_buying_list должна выводить надписи
# 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза.
# После каждой надписи выводите картинки к продуктам. В конце выведите ранее созданное Inline меню с надписью
# "Выберите продукт для покупки:".
# Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
# Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"



#Решение:

from config import API_TOKEN
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboard import create_bot_keyboard, create_inline_product_keyboard, create_inline_price_keyboard


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


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
    for i in range(1, 5):
        await message.answer_photo(
            open(f"product{i}.jpg", "rb"),
            caption=f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}руб'
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




