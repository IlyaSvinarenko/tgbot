from aiogram import Router
from aiogram.types import CallbackQuery

import menus
from .command_handlers import temp_selection
from create_bot import bot

callback_router = Router()


@callback_router.callback_query(lambda c: c.data.startswith("timer"))
async def select_user(callback_query: CallbackQuery):
    pass


@callback_router.callback_query(lambda c: c.data.startswith("party"))
async def select_user(callback_query: CallbackQuery):
    if callback_query.data.split()[1] == "finish_selection":
        timer_menu = menus.create_timer_menu()
        await bot.send_message(text=f"Сколько нужно времени для реди", chat_id=callback_query.message.chat.id,
                               reply_markup=timer_menu)
        user_set = temp_selection.get(callback_query.from_user.id, set())
        initiator_id = callback_query.from_user.id
        if not user_set or len(user_set) == 0:
            await bot.send_message(callback_query.message.chat.id, "Ты никого не выбрал")
        else:
            for user_id in user_set:
                agreement_menu = menus.create_agreement_menu(initiator_id=initiator_id)
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


@callback_router.callback_query(lambda c: c.data.startswith("answer"))
async def answer(callback_query: CallbackQuery):
    data_list = callback_query.data.split()[1::]
    print(data_list[0], data_list[1])
    gog = int(data_list[0])
    initiator_id = int(data_list[1])
    await bot.send_message(chat_id=initiator_id, text=f"{callback_query.from_user.username} ответил {gog}")
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text=f"Твой выбор отправлен пользователю")
