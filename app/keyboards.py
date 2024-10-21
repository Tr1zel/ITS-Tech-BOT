from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)
"""
Пользовательские клавиатуры
"""
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Посмотреть свои баллы')],
    [KeyboardButton(text='Посмотреть историю начислений баллов')]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт из меню...')
