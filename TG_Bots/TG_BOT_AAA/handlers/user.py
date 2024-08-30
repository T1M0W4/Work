from aiogram import F, types, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from kbds.reply import get_keyboard

user_r = Router()

# Определяем состояния
class Form(StatesGroup):
    waiting_for_phone = State()
    waiting_for_access_code = State()
    waiting_for_registration_code = State()

# Клавиатура для выбора действия (Войти или Регистрация)
ENTER_KB = get_keyboard(
    "Войти",
    "Регистрация",
    placeholder="Выберите действие",
    sizes=(1, 1),
)

# Клавиатура для отправки номера телефона
PHONE_KB = get_keyboard(
    "Отправить номер телефона",
    placeholder="Отправьте номер телефона",
    request_contact=0,  # Запрашиваем номер телефона
    sizes=(1,),
)

# Клавиатура для каталога товаров
CATALOG_KB = get_keyboard(
    "Список товаров"
    "Поиск товаров",
    "Информация о товаре",
    "Добавить товары",
    "Корзина",
    placeholder="Выберите раздел каталога",
    sizes=(2, 2, 1),
)


@user_r.message(CommandStart())
async def enter_cmd(message: types.Message):
    await message.answer("Привет, я виртуальный помощник", reply_markup=ENTER_KB)

@user_r.message(F.text == "Войти")
async def login_cmd(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_phone.state)
    await state.update_data(action="login")
    await message.answer("Пожалуйста, отправьте ваш номер телефона для входа.", reply_markup=PHONE_KB)

@user_r.message(F.text == "Регистрация")
async def register_cmd(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_phone.state)
    await state.update_data(action="register")
    await message.answer("Пожалуйста, отправьте ваш номер телефона для регистрации.", reply_markup=PHONE_KB)

@user_r.message(F.contact, StateFilter(Form.waiting_for_phone))
async def process_contact(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    user_data = await state.get_data()
    action = user_data.get("action")

    if action == "login":
        await state.clear()  # Завершить текущее состояние
        await message.answer("Номер телефона сохранен. Пожалуйста, введите ваш код доступа.")
        await state.set_state(Form.waiting_for_access_code.state)
    elif action == "register":
        await state.clear()  # Завершить текущее состояние
        await message.answer("Номер телефона сохранен. Ваш код доступа: 1234. Пожалуйста, введите его.")
        await state.set_state(Form.waiting_for_registration_code.state)
    else:
        await message.answer("Пожалуйста, отправьте номер телефона.")

@user_r.message(F.text, StateFilter(Form.waiting_for_access_code))
async def process_access_code(message: types.Message):
    access_code = message.text
    if access_code == "1234":
        await message.answer("Код доступа верный. Добро пожаловать в каталог товаров!", reply_markup=CATALOG_KB)
    else:
        await message.answer("Неправильный код доступа. Попробуйте еще раз.")

@user_r.message(F.text, StateFilter(Form.waiting_for_registration_code))
async def process_registration_code(message: types.Message):
    registration_code = message.text
    if registration_code == "1234":
        await message.answer("Регистрация завершена. Добро пожаловать в каталог товаров!", reply_markup=CATALOG_KB)
    else:
        await message.answer("Неправильный код доступа. Попробуйте еще раз.")
