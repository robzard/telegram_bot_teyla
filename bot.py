import logging
from pathlib import Path

from aiogram import Bot, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.types import InputMediaVideo, InputMediaPhoto, ParseMode

from buttons import *
from text_answer import *
import config
from sql import *
import asyncio

ADMINS = config.ADMINS
logging.basicConfig(level=logging.INFO)

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

loop = asyncio.get_event_loop()
db = DBCommands(loop)


def deletefiles(id):
    for filename in Path('.').glob('*' + str(id) + "*"):
        filename.unlink()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(text_start, reply_markup=l1)
    await db.insert_user()


@dp.message_handler(text=['Статистика'])
async def process_start_command(message: types.Message):
    await bot.send_media_group(message.chat.id, await db.get_media_st())
    deletefiles(message.from_user.id)


@dp.message_handler(text=['Сообщения'])
async def process_start_command(message: types.Message):
    filename = await db.get_excel_file_userstext()
    await bot.send_document(message.from_user.id, open(filename, 'rb'))
    deletefiles(message.from_user.id)


@dp.message_handler(text='Меню')
async def process_start_command(message: types.Message):
    if message.from_user.id in ADMINS and l1_st not in l1:
        kb = l1_admin
    else:
        kb = l1
    await message.answer("Возврат в меню.", reply_markup=kb)
    await db.insert_move('Главное меню', 'Меню')


@dp.message_handler(text='Информация о курсе')
async def process_start_command(message: types.Message):
    await message.answer("Выберите, интересующий Вас, курс.", reply_markup=get_kb_l2(1))
    await db.insert_move('Главное меню', 'Информация о курсе')


@dp.message_handler(text='Стоимость курса')
async def process_start_command(message: types.Message):
    await message.answer("Выберите, интересующий Вас, курс.", reply_markup=get_kb_l2(2))
    await db.insert_move('Главное меню', 'Стоимость курса')


@dp.message_handler(text='Оплатить курс')
async def process_start_command(message: types.Message):
    await message.answer("Выберите, интересующий Вас, курс.", reply_markup=get_kb_l2(3))
    await db.insert_move('Главное меню', 'Оплатить курс')


@dp.message_handler(text='Часто задаваемые вопросы')
async def process_start_command(message: types.Message):
    await message.answer("Выберите, интересующий Вас, вопрос.", reply_markup=l2_questions)
    await db.insert_move('Главное меню', 'Часто задаваемые вопросы')


@dp.message_handler(text='Связаться с менеджером')
async def process_start_command(message: types.Message):
    await message.answer("Отправьте нам Ваш контакт и менеджер свяжется с вами.", reply_markup=kbPhone)


#  Информация о курсе
@dp.message_handler(
    text=['ℹ «Стиль для себя» с Татьяной', 'ℹ «Стиль для себя» с куратором', 'ℹ «Профессия-стилист» с Татьяной',
          'ℹ «Профессия-стилист» с куратором'])
async def process_start_command(message: types.Message):
    await db.insert_move('Информация о курсе', message.text.replace('ℹ ', ''))
    await message.answer(getTextInfoCourse(message.text), reply_markup=getkb1(await db.get_last_button_user()), parse_mode=ParseMode.MARKDOWN)



#  Стоимость курса
@dp.message_handler(
    text=['💰 «Стиль для себя» с Татьяной', '💰 «Стиль для себя» с куратором', '💰 «Профессия-стилист» с Татьяной',
          '💰 «Профессия-стилист» с куратором'])
async def process_start_command(message: types.Message):
    await db.insert_move('Стоимость курса', message.text.replace('💰 ', ''))
    await message.answer(getTextInfoCoast(message.text), reply_markup=getkb2(await db.get_last_button_user()))



#  Оплатить курс
@dp.message_handler(
    text=['💳 «Стиль для себя» с Татьяной', '💳 «Стиль для себя» с куратором', '💳 «Профессия-стилист» с Татьяной',
          '💳 «Профессия-стилист» с куратором'])
async def process_start_command(message: types.Message):
    await db.insert_move('Оплатить курс', message.text.replace('💳 ', ''))
    await message.answer(getTextInfoPay(message.text), reply_markup=getkb3(await db.get_last_button_user()))



#  Часто задаваемые вопросы
@dp.message_handler(regexp="\?")
async def process_start_command(message: types.Message):
    if getTextInfoQuestions(message.text) != "К сожалению, я не знаю как ответить на Ваш вопрос. " \
                                             "Выберите вопрос из меню или свяжитесь с менеджером.":
        await message.answer(getTextInfoQuestions(message.text), reply_markup=kbManager)
        await db.insert_move('Часто задаваемые вопросы', message.text)
    else:
        await message.answer(getTextInfoQuestions(message.text), reply_markup=kbManager)
        await message.answer('Так же, у нас присутствует раздел часто задаваемых вопросов.', reply_markup=l2_questions)


@dp.message_handler(regexp="^[+0-9][-0-9]+$")
async def process_start_command(message: types.Message):
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text=f'Просьба связаться с менеджером:\n'
                                                   f'Телефон: {message.text}\n'
                                                   f'Имя: {message.from_user.first_name}\n'
                                                   f'Фамилия: {message.from_user.last_name}')
    await message.answer("Контакт получен! Менеджер напишет Вам в телеграм, ожидайте.", reply_markup=l1)
    last_move = await db.get_last_button_user()
    await db.insert_move(last_move, 'Связаться с менеджером')
    await db.update_phone(message.text, message.from_user.id)


@dp.callback_query_handler(lambda c: c.data == 'menu')
async def callbac_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.from_user.id in ADMINS and l1_st not in l1:
        kb = l1_admin
    else:
        kb = l1
    await bot.send_message(callback_query.from_user.id, "Возврат в меню.", reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'manager')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Оставьте свой номер телефона и менеджер свяжется с Вами.',
                           reply_markup=kbPhone)


# @dp.callback_query_handler(text="pay")
# async def process_callback_button23(callback_query: types.CallbackQuery):
#     #await bot.answer_callback_query(callback_query.id, 'qwe')
#     print('1')


@dp.message_handler(content_types=['contact'])
async def process_start_command(message: types.Message):
    print(message.contact)
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text=f'Просьба связаться с менеджером:\n'
                                                   f'Телефон: {message.contact["phone_number"]}\n'
                                                   f'Имя: {message.contact["first_name"]}\n'
                                                   f'Фамилия: {message.contact["last_name"]}')
    await message.answer("Контакт получен! Менеджер напишет Вам в телеграм, ожидайте.", reply_markup=l1)
    last_move = await db.get_last_button_user()
    await db.insert_move(last_move, 'Связаться с менеджером')
    await db.update_phone(message.contact["phone_number"], message.from_user.id)


@dp.message_handler()
async def any_text(message: types.Message):
    if message.from_user.id in ADMINS and l1_st not in l1:
        kb = l1_admin
    else:
        kb = l1
    await db.insert_text_user()
    await message.answer(text='Выберите, интересующий вас, раздел из меню или обратитесь к менеджеру.', reply_markup=kb)


async def on_startup(db):
    print('start')
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text="Чат-бот запущен.")


async def on_shutdown(db):
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text="Я отключён!")
    loop.close()
    await bot.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown, on_startup=on_startup)
