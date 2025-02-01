import logging
import os

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, PollAnswer

import menus
from db_handler import users_table
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from create_bot import bot

log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)s %(message)s')
start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    chat_id = message.chat.id
    user_in_chat = users_table.get_user(user_id, chat_id)
    logging.info(f'in command_handlers / def cmd_start:  user added == {user_in_chat}')
    if not user_in_chat:
        users_table.add_user(user_id, user_name, user_first_name, chat_id)
        await message.answer(f"@{user_name} \n Добро пожаловать на борт!")


# @start_router.message(Command("party"))
# async def all_message_handler(message: Message):
#     if message.chat.type == "private":
#         message.answer("Выбери тех, кому отправится сообщение:", )


@start_router.message(F.text == '/start_3')
async def cmd_start_3(message: Message):
    await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!')


temp_selection = {}


# Команда /create_party
@start_router.message(Command("create_party"))
async def create_party(message: Message):
    if message.chat.type != "private":
        users_from_db = users_table.get_users_in_chat(message.chat.id)
        temp_selection[message.from_user.id] = set()
        users = []
        for user in users_from_db:
            user_id, user_name, user_first_name = user[0], user[2], user[4]
            users.append([user_id, user_name, user_first_name])
    else:
        users_from_db = users_table.get_users()
        temp_selection[message.from_user.id] = set()  # Инициализация выбора для пользователя
        users = []
        for user in users_from_db:
            user_id, user_name, user_first_name = user[0], user[2], user[4]
            users.append([user_id, user_name, user_first_name])
    # Создаем кнопки
    menu = menus.create_party_users_menu(users)
    await message.answer("Выберите пользователей для группы (нажмите на ник):", reply_markup=menu)


# Обработка нажатий на кнопки выбора
@start_router.callback_query(lambda c: c.data.startswith("party"))
async def select_user(callback_query: CallbackQuery):
    if callback_query.data.split()[1] == "finish_selection":
        user_set = temp_selection.get(callback_query.from_user.id, set())
        initiator_id = callback_query.from_user.id
        if not user_set or len(user_set) == 0:
            await bot.send_message(callback_query.message.chat.id, "Ты никого не выбрал")
        else:
            for user_id in user_set:
                agreement_menu = menus.create_agreement_menu(initiator_id=initiator_id, user_id=user_id)

                await bot.send_message(chat_id=user_id,
                                       text=f"Тебя призывает в доту {callback_query.from_user.username}",
                                       reply_markup=agreement_menu)
            del temp_selection[callback_query.from_user.id]
    else:
        user_id = int(callback_query.data.split()[1])
        user_name = callback_query.data.split()[2]
        user_set = temp_selection.get(callback_query.from_user.id, set())

        if user_id in user_set:
            user_set.remove(user_id)  # Убираем из выбора, если уже выбран
            await callback_query.answer(f"Пользователь {user_name} убран из выбора.")
        else:
            user_set.add(user_id)  # Добавляем в выбор
            await callback_query.answer(f"Пользователь {user_name} добавлен в выбор.")

        temp_selection[callback_query.from_user.id] = user_set


@start_router.callback_query(lambda c: c.data.startswith("answer"))
async def answer(callback_query: CallbackQuery):
    data_list = callback_query.data.split()[1::]
    print(data_list[0], data_list[1])
    gog = int(data_list[0])
    initiator_id = int(data_list[1])
    await bot.send_message(chat_id=initiator_id, text=f"{callback_query.from_user.username} ответил {gog}")
    await bot.delete_message(chat_id=callback_query.from_user.id, me=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text=f"Твой выбор отправлен пользователю")
# # Завершение выбора
# @start_router.callback_query(lambda c: c.data == "finish_selection")
# async def finish_selectio(callback_query: CallbackQuery):
#     user_set = temp_selection.get(callback_query.from_user.id, set())
#
#     if not user_set:
#         await callback_query.answer("Вы никого не выбрали!", show_alert=True)
#         return
#
#     # Отправляем результат выбора
#     await callback_query.message.edit_text(
#         f"Вы выбрали следующих пользователей: {user_set}"
#     )
#     del temp_selection[callback_query.from_user.id]  # Очищаем временное хранилище
