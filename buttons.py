from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from text_answer import *

menu = KeyboardButton('Меню')

# Инлайн (Контакт)
inline_menu = InlineKeyboardButton('Меню', callback_data='menu')
inline_rassrochka = InlineKeyboardButton('Хочу рассрочку', callback_data='rassrochka', url='https://www.teylaschool.ru/rassrochka')
inline_phone = InlineKeyboardButton('Связаться с менеджером', callback_data='manager')
inline_rassrochka2 = InlineKeyboardButton('Заявка на рассрочку', callback_data='rassrochka', url='https://www.teylaschool.ru/rassrochka')


kbPhone = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True, callback_data='button1',)
).add(menu)


# Первый уровень (Меню)
l1_info = KeyboardButton('Информация о курсе')
l1_coast = KeyboardButton('Стоимость курса')
l1_pay = KeyboardButton('Оплатить курс')
l1_questions = KeyboardButton('Часто задаваемые вопросы')
l1_manager = KeyboardButton('Связаться с менеджером')
l1_st = KeyboardButton('Статистика')
l2_st = KeyboardButton('Сообщения')
l1 = ReplyKeyboardMarkup(resize_keyboard=True).row(l1_info, l1_coast, l1_pay).add(l1_questions, l1_manager)
l1_admin = l1.add(l1_st).add(l2_st)


# Часто задаваемые вопросы
l2_questions_1 = KeyboardButton('Когда начало курса?')
l2_questions_2 = KeyboardButton('Чем отличаются курсы?')
l2_questions_3 = KeyboardButton('Какие есть варианты оплаты?')
l2_questions_4 = KeyboardButton('Сколько идет курс и уроки?')
l2_questions_5 = KeyboardButton('Я могу не выполнять домашние задания?')
l2_questions_6 = KeyboardButton('Я уезжаю в отпуск, смогу смотреть уроки?')
kbManager = InlineKeyboardMarkup(resize_keyboard=True).row(inline_phone)
l2_questions = ReplyKeyboardMarkup().row(l2_questions_1, l2_questions_2).add(l2_questions_4).add(l2_questions_6).add(l2_questions_3).add(l2_questions_5).add(menu)


# Второй уровень (Информация о курсе)
def get_kb_l2(type):
    if type == 1:
        smile = 'ℹ'
    elif type == 2:
        smile = '💰'
    elif type == 3:
        smile = '💳'
    l2_1 = KeyboardButton(f'{smile} «Стиль для себя» с Татьяной')
    l2_2 = KeyboardButton(f'{smile} «Стиль для себя» с куратором')
    l2_3 = KeyboardButton(f'{smile} «Профессия-стилист» с Татьяной')
    l2_4 = KeyboardButton(f'{smile} «Профессия-стилист» с куратором')
    l2 = ReplyKeyboardMarkup().row(l2_1, l2_2).add(l2_3, l2_4).add(menu)
    return l2

def getkb1(text):
    if '«Стиль для себя» с Татьяной' in text:
        url = 'https://teylaschool.getcourse.ru/myself'
    elif '«Стиль для себя» с куратором' in text:
        url = 'https://teylaschool.getcourse.ru/myself_kurator'
    elif'«Профессия-стилист» с Татьяной' in text:
        url = 'https://teylaschool.getcourse.ru/stylist'
    elif '«Профессия-стилист» с куратором' in text:
        url = 'https://teylaschool.getcourse.ru/stylist_kurator'
    else:
        url = 'https://www.teylaschool.ru'
    inline_pay = InlineKeyboardButton('Перейти к оплате', callback_data='pay', url=url)
    return InlineKeyboardMarkup(resize_keyboard=True).row(inline_pay).add(inline_phone).add(inline_menu)


def getkb2(text):
    if '«Стиль для себя» с Татьяной' in text:
        url = 'https://teylaschool.getcourse.ru/myself'
    elif '«Стиль для себя» с куратором' in text:
        url = 'https://teylaschool.getcourse.ru/myself_kurator'
    elif'«Профессия-стилист» с Татьяной' in text:
        url = 'https://teylaschool.getcourse.ru/stylist'
    elif '«Профессия-стилист» с куратором' in text:
        url = 'https://teylaschool.getcourse.ru/stylist_kurator'
    else:
        url = 'https://www.teylaschool.ru'
    inline_pay = InlineKeyboardButton('Перейти к оплате', callback_data='pay', url=url)
    return InlineKeyboardMarkup(resize_keyboard=True).row(inline_pay).add(inline_phone).add(inline_rassrochka).add(inline_menu)


def getkb3(text):
    if '«Стиль для себя» с Татьяной' in text:
        url = 'https://teylaschool.getcourse.ru/myself'
    elif '«Стиль для себя» с куратором' in text:
        url = 'https://teylaschool.getcourse.ru/myself_kurator'
    elif'«Профессия-стилист» с Татьяной' in text:
        url = 'https://teylaschool.getcourse.ru/stylist'
    elif '«Профессия-стилист» с куратором' in text:
        url = 'https://teylaschool.getcourse.ru/stylist_kurator'
    else:
        url = 'https://www.teylaschool.ru'
    inline_pay_full_sum = InlineKeyboardButton('Оплатить всю сумму полностью', callback_data='pay',
                                               url=url)
    inline_pay_predoplata = InlineKeyboardButton('Внести предоплату (забронировать)', callback_data='pay',
                                                 url=url)
    return InlineKeyboardMarkup(resize_keyboard=True).add(inline_pay_full_sum).add(inline_pay_predoplata).add(inline_rassrochka2).add(inline_menu)