from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)
from aiogram.filters import Command
from aiogram.types import Message

# from run import ADMINS
from config import ADMIN_ID
from app.keyboards import main
from app.functions import (get_creative_points, get_engineers_points,
                           add_creative_points, add_engineers_points)

"""
Все админ клавиатуры, админ хендлеры и все что связано с администратором
"""
router_admin = Router()

admin_keyboard_edit_points = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text='Изменить(посмотреть) количество баллов')],
    [KeyboardButton(text='Выйти из режима Администратора')]
], resize_keyboard=True)

admin_keyboard_type_score = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Изменить инженерные баллы'), KeyboardButton(text='Изменить креативные баллы')],
    [KeyboardButton(text='Выйти из режима Администратора')]
], resize_keyboard=True, input_field_placeholder='Выберите режим изменения баллов...')

admin_keyboard_type_score_with_back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Изменить инженерные баллы'), KeyboardButton(text='Изменить креативные баллы')],
    [KeyboardButton(text='Назад')],
    [KeyboardButton(text='Выйти из режима Администратора')]
], resize_keyboard=True, input_field_placeholder='Выберите режим изменения баллов...')

class UserAdminStates(StatesGroup): # Cостояния для получения имени пользователя и просмотра баллов
    Query_name = State()
    Query_NoneType_points = State()
    Query_engineer_points = State()
    Query_creative_points = State()

@router_admin.message(Command('admin'))
async def admin(message: Message):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer(f'Добро пожаловать в админ меню!\n'
                             f'В админ панели доступно только изменение баллов.\n')
        await message.answer(f'Для изменения баллов нажмите кнопку ниже', reply_markup=admin_keyboard_edit_points),
    else: await message.reply('Нет такой команды!')

@router_admin.message(F.text == 'Выйти из режима Администратора')
async def bye_message(message: Message):
    await message.answer(text='Вы вышли из режима Администратора!',
                         reply_markup=main)

@router_admin.message(F.text == 'Изменить(посмотреть) количество баллов')
async def edit_points(message: Message, state: FSMContext):
    await message.answer(text='Введите имя пользователя, чтобы получить баллы.')
    await state.set_state(UserAdminStates.Query_name)


@router_admin.message(UserAdminStates.Query_name)
async def edit_points_for_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    name = user_data['name']
    eng_points = await get_engineers_points(name)
    creat_points = await get_creative_points(name)
    if eng_points is not None and creat_points is not None:
        await message.answer(f'{name} имеет {eng_points} инженерных баллов и {creat_points} креативных баллов\n')
        await message.answer(f'Выберите режим в котором хотите изменить баллы',
                                    reply_markup=admin_keyboard_type_score_with_back)
        await state.set_state(UserAdminStates.Query_NoneType_points)
    else:
        await message.answer('Пользователь не найден. Попробуйте снова.')

@router_admin.message(F.text == 'Назад')
async def back_to_edit(message: Message):
    await message.answer('Вы вернулись назад.',
                         reply_markup=admin_keyboard_edit_points)

@router_admin.message(F.text == 'Изменить инженерные баллы', UserAdminStates.Query_NoneType_points)
async def change_engineer_score(message: Message, state: FSMContext):
    await message.answer(text='Категория баллов - Инженерные\n'
                              'Введите количество баллов которое вы хотите добавить пользователю.')
    await state.set_state(UserAdminStates.Query_engineer_points)

@router_admin.message(UserAdminStates.Query_engineer_points)
async def change_engineer_score_2(message: Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(add_to_points=message.text)
        user_data = await state.get_data()
        name = user_data['name']
        add_to_points = user_data['add_to_points']
        await add_engineers_points(name, add_to_points)
        await message.answer(f'{add_to_points} прибавлены к инженерным баллам пользователю {name}.',
                             reply_markup=admin_keyboard_edit_points)
        await state.clear()
    else:
        await message.answer('Введен не числовой формат или число не от 1 до 5, попробуйте заново!')

@router_admin.message(F.text == 'Изменить креативные баллы',UserAdminStates.Query_NoneType_points )
async def change_creative_score(message: Message, state: FSMContext):
    await message.answer(text='Категория баллов - креативные\n'
                              'Введите количество баллов которое вы хотите добавить пользователю.')
    await state.set_state(UserAdminStates.Query_creative_points)

@router_admin.message(UserAdminStates.Query_creative_points)
async def change_creative_score_2(message: Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(add_to_points=message.text)
        user_data = await state.get_data()
        name = user_data['name']
        add_to_points = user_data['add_to_points']
        await add_creative_points(name, add_to_points)
        await message.answer(f'{add_to_points} прибавлены к креативным баллам пользователю {name}.', reply_markup=admin_keyboard_edit_points)
        await state.clear()
    else:
        await message.answer('Введен не числовой формат или число не от 1 до 5, попробуйте заново!')
