import asyncpg
import logging
import asyncio

import numpy as np
from aiogram import types
from aiogram.types import InputMediaPhoto
from asyncpg import Connection, Record
from config import HOST, PG_USER, PG_PASS, PORT, DATABASE
import pandas as pd
from matplotlib import pyplot as plt





def create_img_graphic_2(df: pd.DataFrame, filename, title):
    plt.style.use('dark_background')
    fig = df.plot(x='dates', y='counts', marker='.', markersize=10, x_compat=True,
                  figsize=(15, 10))  # , figsize=(15,10)
    plt.ylabel('Количество действий', fontsize=20)
    if type(df['dates'][0]) == np.float64:
        plt.xlabel('Время', fontsize=20)
        plt.xticks(df['dates'], fontsize=20)
        ax = plt.gca()
        df.apply(lambda x: ax.annotate(x['counts'], (x['dates'] + 0.1, x['counts'])), axis=1)
    else:
        plt.xlabel('Дата', fontsize=20)
        plt.xticks(df['dates'], fontsize=12)
        # i=0
        # df.apply(lambda x: ax.annotate(x['counts'], (x['dates'][3], x['counts'])), axis=1)
    markerline, stemlines, baseline = plt.stem(df['dates'], df['counts'], linefmt=":",  basefmt=" ")
    plt.setp(stemlines, 'linewidth', 0.5)
    fig.figure.suptitle(title, fontsize=20)
    fig.figure.savefig(filename + '_st.jpg', bbox_inches='tight')
    plt.close()
    return filename + '_st.jpg'


def create_img_st_1(d, filename):
    plt.style.use('dark_background')
    index = np.arange(len(d['course_name']))
    values1 = d['counts']
    plt.title('Количество нажатий по кнопке')
    plt.barh(index, values1, error_kw={'ecolor': '0.1', 'capsize': 10}, alpha=0.7, label='First', color='#40E0D0')
    plt.yticks(index + 0.4, d['course_name'])
    plt.savefig(filename + '_st.jpg', bbox_inches='tight')
    plt.close()
    return filename + '_st.jpg'


class DBCommands:
    def __init__(self, loop):
        self.loop = loop
        self.db: Connection = self.loop.run_until_complete(self.create_pool())

        self.SQL_INSERT_MOVE = "INSERT INTO public.movies \
                                (chat_id, username, full_name, category_move, button_name_move, datetime_move) \
                                VALUES ($1,$2,$3,$4,$5,NOW())"
        self.SQL_INSERT_USER = """  
                                    INSERT INTO public.users(
                                    chat_id, username, full_name)
                                    SELECT $1 as chat_id,$2 as username,$3 as full_name
                                    WHERE
                                        NOT EXISTS(
                                            SELECT chat_id FROM public.users WHERE chat_id = $1	
                                        )
        """
        self.SQL_INSERT_USER_TEXT = """  
                                            INSERT INTO public.userstext(
                                            chat_id, username, firstname, lastname, text, dateinsert)
                                            VALUES ($1,$2,$3,$4,$5, NOW());
                """
        self.SQL_LAST_BUTTON = "SELECT category_move || ';' || button_name_move " \
                               "FROM movies " \
                               "WHERE datetime_move = (SELECT max(datetime_move) FROM movies WHERE chat_id = $1) " \
                               "and button_name_move not like 'Связаться с менеджером'" \
                               "and chat_id = $1"
        self.SQL_UPDATE_PHONE = "UPDATE users SET phone = $1 WHERE chat_id = $2"

        #  Количество всех нажатых кнопок
        self.SQL_STATISTIC_1 = """
                                    select button_name_move, count(*)
                                    from movies
                                    group by button_name_move
                                    order by 1;
                                """
        self.SQL_STATISTIC_2 = """
                                    SELECT dates::date as dates,0 as counts FROM generate_series(date_trunc('day',NOW()) - INTERVAL '14 day', NOW(), interval '1 day') AS dates
                                    WHERE dates NOT IN (SELECT date_trunc('day',datetime_move) FROM movies)
                                    UNION
                                    select date_trunc('day',datetime_move) as dates, count(*) as count
                                    FROM public.movies
                                    group by date_trunc('day',datetime_move)
                                    order by 1;
                                """
        self.SQL_STATISTIC_3 = """
                                    
                                    SELECT EXTRACT(hour from dates),0 as counts 
                                    FROM 
                                    (
                                        select dates,0 as counts FROM generate_series(date_trunc('hour',NOW()) - INTERVAL '1 day', NOW(), interval '1 hour') AS dates
                                        where EXTRACT(day from dates) = EXTRACT(day from NOW())
                                    ) as t
                                    WHERE dates NOT IN (SELECT date_trunc('hour',datetime_move) FROM movies)
                                    UNION
                                    select EXTRACT(hour from date_trunc('hour',datetime_move)) as dates, count(*) as counts
                                    FROM public.movies
                                    where EXTRACT(day from datetime_move) = EXTRACT(day from NOW())
                                    group by date_trunc('hour',datetime_move)
                                    order by 1;
                                """
        self.SQL_STATISTIC_4 = """
                                    select hour as dates, AVG(count)::int as counts
                                    FROM (
                                            select EXTRACT(day from datetime_move),EXTRACT(hour from datetime_move) as hour, count(*) as count
                                            FROM public.movies
                                            group by EXTRACT(day from datetime_move),EXTRACT(hour from datetime_move)
                                        ) t1
                                    group by hour
                                    order by 1;
                               """
        self.SQL_STATISTIC_5 = """
                                    SELECT id, chat_id as id_чата, username as Логин, firstname as Имя, lastname as Фамилия, text as Сообщение, dateinsert as Время
                                    FROM public.userstext order by id;
                               """

    async def db_create_tables(self):
        logging.info("Connecting to db.")
        create_db_tables = open("create_tables.sql", "r").read()
        conn = await asyncpg.connect(user=PG_USER, password=PG_PASS, host=HOST, port=PORT, database=DATABASE)
        try:
            await conn.execute(create_db_tables)
            await conn.close()
        except Exception as ex:
            print(ex)
            await conn.close()


    async def create_pool(self):
        logging.info("Connecting to db.")
        await self.db_create_tables()
        return await asyncpg.create_pool(user=PG_USER, password=PG_PASS, host=HOST, port=PORT, database=DATABASE,
                                         server_settings={'timezone': 'UTC-5'})

    async def insert_move(self, category_move, button_name_move):
        user = types.User.get_current()
        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = (chat_id, username, full_name, category_move, button_name_move)
        await self.db.fetchval(self.SQL_INSERT_MOVE, *args)

    async def get_last_button_user(self):
        user = types.User.get_current()
        chat_id = user.id
        return await self.db.fetchval(self.SQL_LAST_BUTTON, chat_id)

    async def insert_user(self):
        user = types.User.get_current()
        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = (chat_id, username, full_name)
        await self.db.fetchval(self.SQL_INSERT_USER, *args)

    async def update_phone(self, phone, chat_id):
        await self.db.fetchval(self.SQL_UPDATE_PHONE, phone, chat_id)

    async def get_media_st(self):
        user = types.User.get_current()
        chat_id = str(user.id)
        media = []
        m1 = await self.st_countAllButtons('1_' + chat_id)
        #await asyncio.sleep(1)
        media.append(InputMediaPhoto(m1, 'Количество нажатий на кнопки за всё время.'))
        media.append(InputMediaPhoto(
            await self.st_graphic(self.SQL_STATISTIC_2, '2_' + chat_id, 'Количество нажатий на кнопки за 2 недели.'),
            'Количество нажатий на кнопки за 2 недели.'))
        media.append(InputMediaPhoto(await self.st_graphic(self.SQL_STATISTIC_3, '3_' + chat_id,
                                                           'Количество нажатий на кнопки за последние 24 часа.'),
                                     'Количество нажатий на кнопки за последние 24 часа.'))
        media.append(InputMediaPhoto(
            await self.st_graphic(self.SQL_STATISTIC_4, '4_' + chat_id, 'Средняя активность по времени.'),
            'Средняя активность по времени.'))
        return media

    async def st_countAllButtons(self, filename):
        dict = {'course_name': [], 'counts': []}
        data = await self.db.fetch(self.SQL_STATISTIC_1)
        for name, count in data:
            dict['course_name'].append(name)
            dict['counts'].append(count)
        img = open(create_img_st_1(dict, filename), 'rb')
        return img

    async def st_graphic(self, sql, filename, title):
        dict = {'dates': [], 'counts': []}
        data = await self.db.fetch(sql)
        for name, count in data:
            dict['dates'].append(name)
            dict['counts'].append(count)
        df = pd.DataFrame(data=dict)
        img = open(create_img_graphic_2(df, filename, title), 'rb')
        return img


    async def insert_text_user(self):
        user = types.User.get_current()
        message = types.Message.get_current().text
        chat_id = str(user.id)
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        args = (chat_id, username, first_name, last_name, message)
        await self.db.fetchval(self.SQL_INSERT_USER_TEXT, *args)


    async def get_excel_file_userstext(self):
        user = types.User.get_current()
        chat_id = str(user.id)
        data = await self.db.fetch(self.SQL_STATISTIC_5)
        df = pd.DataFrame(data=data, columns=['id','id_чата', 'Логин', 'Имя', 'Фамилия', 'Сообщение', 'Дата'])
        print(df['Дата'])
        df['Дата'] = df['Дата'].apply(lambda a: pd.to_datetime(a).date())
        filename = f'{chat_id}_messages.xlsx'
        df.to_excel(filename, index=False)
        return filename
