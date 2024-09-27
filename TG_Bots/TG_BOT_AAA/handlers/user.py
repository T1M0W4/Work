import random
import sqlite3
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
    waiting_for_estimate_text = State()

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
    "Назад",
    placeholder="Отправьте номер телефона",
    request_contact=0,  # Запрашиваем номер телефона
    sizes=(1, 1),
)

# Клавиатура для каталога товаров
CATALOG_KB = get_keyboard(
    "Составить смету",
    "Задачи",
    "Список товаров",
    "Поиск товаров",
    "Информация о товаре",
    "Добавить товары",
    "Корзина",
    placeholder="Выберите раздел каталога",
    sizes=(2, 2, 2, 1),
)

# Клавиатура для ввода текста сметы
ESTIMATE_KB = get_keyboard(
    "Создать",
    "Назад",
    placeholder="Выберите действие",
    sizes=(1, 1),
)

def generate_password():
    """Генерирует случайный пароль."""
    return str(random.randint(1000, 9999))

def save_user(phone_number, password):
    """Сохраняет пользователя в базе данных."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (phone_number, password) VALUES (?, ?)', (phone_number, password))
        conn.commit()
    except sqlite3.IntegrityError:
        # Обработка ошибки, если номер уже существует
        print(f"Пользователь с номером {phone_number} уже существует.")
    conn.close()

def validate_user(phone_number, password):
    """Проверяет пользователя по номеру телефона и паролю.
    
    Возвращает:
    - 'not_registered' если номер телефона не найден
    - 'wrong_password' если пароль неправильный
    - 'valid' если все верно
    """
    print(f"Validating user with phone number: {phone_number} and password: {password}")  # Логирование

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE phone_number = ?', (phone_number,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return 'not_registered'
    
    stored_password = result[0]
    if stored_password == password:
        return 'valid'
    else:
        return 'wrong_password'

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

@user_r.message(F.text == "Назад", StateFilter(Form.waiting_for_phone))
async def back_to_main(message: types.Message, state: FSMContext):
    await state.clear()  # Очистка состояния
    await message.answer("Вы вернулись в главное меню.", reply_markup=ENTER_KB)

@user_r.message(F.contact, StateFilter(Form.waiting_for_phone))
async def process_contact(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number.strip().replace(' ', '')
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number  # Восстанавливаем символ + если его нет

    user_data = await state.get_data()
    action = user_data.get("action")
    
    print(f"Action: {action}, Phone number received: {phone_number}")  # Логирование

    if action == "login":
        await state.update_data(phone_number=phone_number)  # Сохранение номера телефона
        validation_result = validate_user(phone_number, None)
        if validation_result == 'not_registered':
            await message.answer("Этот номер телефона не зарегистрирован. Пожалуйста, зарегистрируйтесь.")
            await state.set_state(Form.waiting_for_phone.state)
        else:
            await message.answer("Номер телефона сохранен. Пожалуйста, введите ваш пароль.")
            await state.set_state(Form.waiting_for_access_code.state)
    elif action == "register":
        # Генерация и сохранение пароля
        password = generate_password()
        save_user(phone_number, password)
        await state.update_data(phone_number=phone_number)  # Сохранение номера телефона
        await message.answer(f"Номер телефона сохранен. Ваш пароль: {password}. Пожалуйста, введите его.")
        await state.set_state(Form.waiting_for_registration_code.state)
    else:
        await message.answer("Пожалуйста, отправьте номер телефона.")

@user_r.message(F.text, StateFilter(Form.waiting_for_phone))
async def process_manual_phone(message: types.Message, state: FSMContext):
    phone_number = message.text.strip().replace(' ', '')  # Убедитесь, что лишние пробелы удалены

    user_data = await state.get_data()
    action = user_data.get("action")
    
    print(f"Action: {action}, Phone number received manually: {phone_number}")  # Логирование

    if action == "login":
        await state.update_data(phone_number=phone_number)  # Сохранение номера телефона
        validation_result = validate_user(phone_number, None)
        if validation_result == 'not_registered':
            await message.answer("Этот номер телефона не зарегистрирован. Пожалуйста, зарегистрируйтесь.")
            await state.set_state(Form.waiting_for_phone.state)
        else:
            await message.answer("Номер телефона сохранен. Пожалуйста, введите ваш пароль.")
            await state.set_state(Form.waiting_for_access_code.state)
    elif action == "register":
        # Генерация и сохранение пароля
        password = generate_password()
        save_user(phone_number, password)
        await state.update_data(phone_number=phone_number)  # Сохранение номера телефона
        await message.answer(f"Номер телефона сохранен. Ваш пароль: {password}. Пожалуйста, введите его.")
        await state.set_state(Form.waiting_for_registration_code.state)
    else:
        await message.answer("Пожалуйста, отправьте номер телефона.")

@user_r.message(F.text, StateFilter(Form.waiting_for_access_code))
async def process_access_code(message: types.Message, state: FSMContext):
    access_code = message.text
    user_data = await state.get_data()
    phone_number = user_data.get('phone_number')
    
    print(f"Validating user with phone number: {phone_number} and password: {access_code}")  # Логирование

    validation_result = validate_user(phone_number, access_code)
    if validation_result == 'valid':
        await message.answer("Пароль верный. Добро пожаловать в каталог товаров!", reply_markup=CATALOG_KB)
        await state.clear()  # Очистка состояния после успешного входа
    elif validation_result == 'wrong_password':
        await message.answer("Неправильный пароль. Попробуйте еще раз.")
    elif validation_result == 'not_registered':
        await message.answer("Этот номер телефона не зарегистрирован. Пожалуйста, зарегистрируйтесь.")

@user_r.message(F.text == "Назад", StateFilter(Form.waiting_for_access_code))
async def back_to_phone_input(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_phone.state)
    await message.answer("Пожалуйста, отправьте ваш номер телефона для входа.", reply_markup=PHONE_KB)

@user_r.message(F.text, StateFilter(Form.waiting_for_registration_code))
async def process_registration_code(message: types.Message, state: FSMContext):
    registration_code = message.text
    user_data = await state.get_data()
    phone_number = user_data.get('phone_number')
    
    print(f"Validating user with phone number: {phone_number} and registration code: {registration_code}")  # Логирование

    validation_result = validate_user(phone_number, registration_code)
    if validation_result == 'valid':
        await message.answer("Регистрация завершена. Добро пожаловать в каталог товаров!", reply_markup=CATALOG_KB)
        await state.clear()  # Очистка состояния после успешной регистрации
    elif validation_result == 'wrong_password':
        await message.answer("Неправильный пароль. Попробуйте еще раз.")
    elif validation_result == 'not_registered':
        await message.answer("Этот номер телефона не зарегистрирован. Пожалуйста, попробуйте снова или зарегистрируйтесь.")

@user_r.message(F.text == "Назад", StateFilter(Form.waiting_for_registration_code))
async def back_to_phone_input_reg(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_phone.state)
    await message.answer("Пожалуйста, отправьте ваш номер телефона для регистрации.", reply_markup=PHONE_KB)




@user_r.message(F.text == "Составить смету")
async def estimate_cmd(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_estimate_text.state)
    await message.answer("Введите текст для сметы:", reply_markup=ESTIMATE_KB)

@user_r.message(F.text, StateFilter(Form.waiting_for_estimate_text))
async def process_estimate_text(message: types.Message, state: FSMContext):
    estimate_text = message.text
    if estimate_text == "Создать":
        # Логика для создания сметы
        await message.answer("Смета создана.", reply_markup=CATALOG_KB)
        await state.clear()  # Очистка состояния после создания сметы
    elif estimate_text == "Назад":
        await message.answer("Вы вернулись в меню каталога товаров.", reply_markup=CATALOG_KB)
        await state.clear()  # Очистка состояния после нажатия кнопки "Назад"
    else:
        await message.answer("Пожалуйста, используйте кнопки 'Создать' или 'Назад'.")

@user_r.message(F.text == "Задачи")
async def tasks_cmd(message: types.Message, state: FSMContext):
    # Получаем текущее состояние
    current_state = await state.get_state()
    print(f"Current state in tasks_cmd: {current_state}")  # Логируем текущее состояние

    # Если бот находится в состоянии ожидания кода доступа, регистрационного кода или текста сметы, игнорируем запрос
    if current_state in [Form.waiting_for_access_code.state, Form.waiting_for_registration_code.state, Form.waiting_for_estimate_text.state]:
        print("Bot is in waiting state for access code, registration code, or estimate text.")  # Логируем состояние
        await message.answer("Пожалуйста, завершите текущий процесс входа, регистрации или создания сметы.")
        return

    # Если бот не в ожидаемом состоянии, продолжаем обработку
    await message.answer("Задачи на сегодня:\n1. Покушать\n2. Поспать")
