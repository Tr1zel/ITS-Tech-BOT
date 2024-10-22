from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboards import main
from app.functions import (add_user, get_engineers_points,
                           get_name_from_id, get_creative_points,
                           validate_name, check_registration, validate_group)

router = Router()

class Reg(StatesGroup):
    waiting_name = State()
    waiting_study_group = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привет! Для регистрации введи команду /reg')

@router.message(Command('reg')) # Начало состояния регистрации
async def reg_name_one(message: Message, state:FSMContext):
    await message.answer(text='Введите свое Имя и Фамилию')
    await state.set_state(Reg.waiting_name)

@router.message(Reg.waiting_name) # ожидание имени для регистрации
async def reg_name_two(message: Message, state: FSMContext):
    if await validate_name(message.text):
        await state.update_data(name=message.text)
        await message.answer(text='Cпасибо! Теперь введите свою учебную группу')
        await state.set_state(Reg.waiting_study_group)
    else:
        await message.answer('Введите Имя и Фамилию через пробел на русском языке')


@router.message(Reg.waiting_study_group) # ожидание номера группы для регистрации
async def reg_study_group_one(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if await validate_group(message.text):
        await state.update_data(study_group=message.text)
        user_data = await state.get_data()
        user_id = message.from_user.id
        name = user_data['name']
        study_group = user_data['study_group']
        # Добавление пользователя в базу данных
        user_added = await add_user(user_id, name, study_group, 0, 0)

        if user_added:
            await message.answer('Вы успешно добавлены, ваши инженерные и креативные баллы = 0!',
                                 reply_markup=main)
        else:
            await message.answer('Вы уже зарегистрированы в базе данных.')
            await message.answer('Вам доступны следующие функции:', reply_markup=main)
        await state.clear()

    else: await message.answer('Введите номер группы как в ЭУ!')

@router.message(Command('help')) # oбработчик команд Help
async def get_help(message: Message):
    await message.answer('Это бот создан в рамках технического задания для ITS Tech\n'
                         'Для регистрации введите команду /help\n'
                         'В данный момент для обычных пользователей доступно только просмотр баллов\n'
                         'Для админов доступно просмотр баллов и изменение творческих и инженерных баллов')

@router.message(Command('check_id')) # Можно узнать свой айди
async def take_id(message: Message):
    await message.answer(f'Ваш айди: {message.from_user.id}')


@router.message(F.text == 'Посмотреть свои баллы') # хендлер для пользователя просмотра баллов
async def check_score(message: Message):
    user_id = message.from_user.id
    if await check_registration(user_id):
        name = await get_name_from_id(message.from_user.id) # функция получения Имени по id
        eng_points = await get_engineers_points(name) # функция получения баллов из бд по имени
        creat_points = await get_creative_points(name)
        await message.answer(f'У вас {eng_points} инженерных баллов, {creat_points} креативных баллов',
                             reply_markup=main)
    else: await message.answer('Вы не зарегистрированы!\nДля продолжения введите команду /reg',
                               reply_markup=ReplyKeyboardRemove())

@router.message(F.text == 'Посмотреть историю начислений баллов') # хендлер для просмотра истории баллов
async def check_history_score(message: Message):
    user_id = message.from_user.id
    if await check_registration(user_id):
        await message.answer(f'Функция допиливается...')
        await message.answer_sticker('CAACAgIAAxkBAAEM_79nFnDLOaSJC11zLy08xw3WMVLSeAACmiMAAg8TOUqugVGCBehjrTYE')
    else: await message.answer('Вы не зарегистрированы! Для продолжения введите команду /reg',
                               reply_markup=ReplyKeyboardRemove())
