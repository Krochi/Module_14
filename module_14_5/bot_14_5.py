# Задача "Регистрация покупателей"

# Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
# initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:
# id - целое число, первичный ключ
# username - текст (не пустой)
# email - текст (не пустой)
# age - целое число (не пустой)
# balance - целое число (не пустой)
# add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
# Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
# Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.
# is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users,
# в противном случае False. Для получения записей используйте SQL запрос.
#
# Изменения в Telegram-бот:
# Кнопки главного меню дополните кнопкой "Регистрация".
# Напишите новый класс состояний RegistrationState
# с следующими объектами класса State: username, email, age, balance(по умолчанию 1000).
# Создайте цепочку изменений состояний RegistrationState.
# Фукнции цепочки состояний RegistrationState:
# sing_up(message):
# Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
# Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
# После ожидать ввода возраста в атрибут RegistrationState.username при помощи метода set.
# set_username(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
# Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text.
# Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
# Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует,
# введите другое имя" и запрашивать новое состояние для RegistrationState.username.
# set_email(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
# Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
# Далее выводить сообщение "Введите свой возраст:":
# После ожидать ввода возраста в атрибут RegistrationState.age.
# set_age(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
# Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
# Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users
# при помощи ранее написанной crud-функции add_user.
# В конце завершать приём состояний при помощи метода finish().

#Решение:

from config import API_TOKEN
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from crud_functions import initiate_db, populate_initial_products, get_all_products, is_included, add_user
from keyboard import create_bot_keyboard, create_inline_product_keyboard, create_inline_price_keyboard


# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализация базы данных
initiate_db()
populate_initial_products()

# Создание клавиатур
bot_kb = create_bot_keyboard()
inline_kb_products = create_inline_product_keyboard()

# Состояния пользователя
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Состояния регистрации
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

# Команда /start
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=bot_kb)


@dp.message_handler(text="Регистрация")
async def sing_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя.")
        return
    await state.update_data(username=username)
    await message.answer("Введите свой email:")
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    data = await state.get_data()
    username = data['username']
    email = data['email']

    add_user(username, email, age)  # добавляем пользователя в базу
    await message.answer("Регистрация успешна!")
    await state.finish()

# Обработчик кнопки "Рассчитать"
@dp.message_handler(text="Рассчитать")
async def calculate_calories(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    products = get_all_products()
    for product in products:
        product_id, title, description, price = product
        try:
            # Используем `product_id` для получения правильного изображения
            await message.answer_photo(
                open(f"product{product_id}.jpg", "rb"),
                caption=f'Название: {title} | Описание: {description} | Цена: {price} руб.'
            )
        except FileNotFoundError:
            await message.answer(f"Изображение для продукта {title} отсутствует.")

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_kb_products)


# Обработчик выбора продукта
@dp.callback_query_handler(lambda call: call.data.startswith("product_"))
async def select_product(call: types.CallbackQuery):
    product_id = call.data.split("_")[1]
    inline_kb_prices = create_inline_price_keyboard(product_id)
    await call.message.answer(f"Цена для Product{product_id}:", reply_markup=inline_kb_prices)

# Обработчик завершения покупки
@dp.callback_query_handler(lambda call: call.data.startswith("price_"))
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")

# Обработчик состояния для расчета калорий
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

# Обработчик кнопки "Регистрация"
@dp.message_handler(text="Регистрация")
async def sing_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинские алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if not is_included(username):
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя:")

@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age_registration(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        data = await state.get_data()
        username = data['username']
        email = data['email']

        add_user(username, email, age)
        await message.answer("Регистрация пройдена! Ваш баланс: 1000.")
        await state.finish()
    except ValueError:
        await message.answer("Возраст должен быть числом! Попробуйте ещё раз:")

@dp.message_handler(text="Информация")
async def send_info(message: types.Message):
    await message.answer("Здесь будет информация о ботe.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




