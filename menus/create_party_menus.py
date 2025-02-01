from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_party_users_menu(users):
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


def create_timer_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f'Готовность 5-10 мин',
            callback_data=f'timer 1'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f'Готовность 10-20 мин',
            callback_data=f'timer 2'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f'Готовность 20-30 мин',
            callback_data=f'timer 3'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f'Готовность 30-40 мин',
            callback_data=f'timer 4'
        )
    )
    menu = builder.as_markup()
    return menu

def create_agreement_menu(initiator_id, user_id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f'Гог',
            callback_data=f'answer 1 {initiator_id}'
        )
    )
    builder.row(InlineKeyboardButton(text='Не Гог', callback_data=f'answer 0 {initiator_id}'))
    builder = builder.as_markup()
