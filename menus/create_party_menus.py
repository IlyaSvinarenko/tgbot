from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_party_users_menu(users):
    builder = InlineKeyboardBuilder()
    for i in users:
        builder.row(
            InlineKeyboardButton(
                text=f'{i[1]} / {i[2]}',
                callback_data=f'party {i[0]} {i[1]}'
            )
        )
    builder.row(InlineKeyboardButton(text='Закончить выбор', callback_data='party finish_selection'))
    menu = builder.as_markup()
    return menu
