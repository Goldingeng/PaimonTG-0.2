import asyncio
import aiosqlite
import datetime
import random
import traceback

#Проверка
async def is_user_registered(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT user_id FROM users WHERE user_id=? LIMIT 1", (user_id,))
            result = await cursor.fetchone()
            await cursor.close()
            return result is not None
    except Exception as e:
         print(e)

#Регестрация
async def login_user(user_id, user_name):
    try:
        async with aiosqlite.connect('BD') as conn:
            await conn.execute("INSERT INTO users (user_id, user_name, status) VALUES (?, ?, ?)", (user_id, user_name, "Отсутствует"))
            await conn.commit()
            await conn.execute("INSERT INTO personLegend (user_id) VALUES (?)", (user_id,))
            await conn.execute("INSERT INTO personEpic (user_id) VALUES (?)", (user_id,))
            await conn.execute("INSERT INTO kettle (user_id) VALUES (?)", (user_id,))
            await conn.commit()
    except Exception as e:
         print(e)

#Отправка аккаунта
async def acc(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
            user_info = await cursor.fetchone()
            guarantee = "Нет" if user_info[6] == 1 else "Да"
            if user_info[12] == 1:
                cursor = await conn.execute(f"SELECT * FROM kettle WHERE user_id = {user_id}")
                kettle_info = await cursor.fetchone()
                guarantee = "Нет" if user_info[6] == 1 else "Да"
                home = "Отсутствует" if kettle_info[1] == 0 else "Халупа 🛖" \
                    if kettle_info[1] == 1 else "Сломаный дом 🏚️" \
                    if kettle_info[1] == 2 else "Обычный дом 🏠" \
                    if kettle_info[1] == 3 else "Особняк 🕌" \
                    if kettle_info[1] == 4 else "Дворец 🕍"

                pool = "Отсутствует" if kettle_info[2] == 0 else "Пруд 🚣‍♂️" \
                    if kettle_info[2] == 1 else "Обычный бассейн 🏊" \
                    if kettle_info[2] == 2 else "Большой бассейн 🤽‍♂️" \
                    if kettle_info[2] == 3 else "Море 🏄" \
                    if kettle_info[2] == 4 else "TOI-1452 b 🔭" 

                fence = "Отсутствует" if kettle_info[2] == 0 else "Деревянный забор 🪵" \
                    if kettle_info[2] == 1 else "Каменный забор 🪨" \
                    if kettle_info[2] == 2 else "Горы ⛰️" \
                    if kettle_info[2] == 3 else "Холодные горы 🏔️" \
                    if kettle_info[2] == 4 else "Вулкан 🌋"

                home_improvement = "Отсутствует" if kettle_info[2] == 0 else "Советский ремонт 🪑" \
                    if kettle_info[2] == 1 else "Современная отделка 🧱" \
                    if kettle_info[2] == 2 else "Евро ремонт 🪞" \
                    if kettle_info[2] == 3 else "Дизайнерский ремонт 🛋️" \
                    if kettle_info[2] == 4 else "Кастомный ремонт 🚽" 

                scenery = "Отсутствует" if kettle_info[2] == 0 else "Туман 🌫️" \
                    if kettle_info[2] == 1 else "Пустыня 🏜️" \
                    if kettle_info[2] == 2 else "Гора 🏞️" \
                    if kettle_info[2] == 3 else "Восход 🌅" \
                    if kettle_info[2] == 4 else "Восход за горами 🌄" 

                message = f"""<b>{user_info[1]}</b> ✔️
{user_info[4]}

<b>Примогемы:</b>  {user_info[5]} 💠    
<b>Ранг:</b>  {user_info[2]} 🔮     <b>Опыт:</b>{user_info[3]}/1000 📜        
<b>История:</b>  {user_info[7]} ⏳  <b>Гарант:</b> {guarantee} 🧿

<b>Чайник</b>
 
<b>Дом:</b>  {home}
<b>Обустройство:</b> {home_improvement}
<b>Бассейн:</b>  {pool}
<b>Ограждение:</b>  {fence}
<b>Пейзаж:</b>  {scenery}"""
            if user_info[12] == 2:
                leg = ""
                cursor = await conn.execute(f"SELECT * FROM personLegend WHERE user_id = {user_id}")
                row = await cursor.fetchone()
                columns = [description[0] for description in cursor.description]
                for i in range(1, len(columns)):
                    if row[i] != 0:
                        leg += f"{columns[i]}: {row[i]}⭐️⭐️⭐️⭐️⭐️"
                        if i < len(columns) - 1:
                            leg += "\n"
                        else:
                            leg += ""  # add an empty string to avoid a trailing newline
                message = f"""<b>{user_info[1]}</b> ✔️
{user_info[4]}

<b>Примогемы:</b>  {user_info[5]} 💠    
<b>Ранг:</b>  {user_info[2]} 🔮     <b>Опыт:</b>{user_info[3]}/1000 📜        
<b>История:</b>  {user_info[7]} ⏳  <b>Гарант:</b> {guarantee} 🧿

<b>Леги:</b>

{leg}
"""
            if user_info[12] == 3:
                leg = ""
                cursor = await conn.execute(f"SELECT * FROM personEpic WHERE user_id = {user_id}")
                row = await cursor.fetchone()
                columns = [description[0] for description in cursor.description]
                for i in range(1, len(columns)):
                    if row[i] != 0:
                        leg += f"{columns[i]}: {row[i]}⭐️⭐️⭐️⭐️"
                        if i < len(columns) - 1:
                            leg += "\n"
                        else:
                            leg += ""  # add an empty string to avoid a trailing newline
                message = f"""<b>{user_info[1]}</b> ✔️
{user_info[4]}

<b>Примогемы:</b>  {user_info[5]} 💠    
<b>Ранг:</b>  {user_info[2]} 🔮     <b>Опыт:</b>{user_info[3]}/1000 📜        
<b>История:</b>  {user_info[7]} ⏳  <b>Гарант:</b> {guarantee} 🧿

<b>Эпики:</b>

{leg}
"""
            await cursor.close()
            return message
    except Exception as e:
         print(e)

#получение лег персов
async def leg(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute(f"SELECT user_name FROM users WHERE user_id = {user_id}")
            user_name = await cursor.fetchone()
            message = ""
            cursor = await conn.execute(f"SELECT * FROM personLegend WHERE user_id = {user_id}")
            row = await cursor.fetchone()
            columns = [description[0] for description in cursor.description]
            for i in range(1, len(columns)):
                if row[i] != 0:
                    message += f"{columns[i]}: {row[i]}⭐️⭐️⭐️⭐️⭐️"
                    if i < len(columns) - 1:
                        message += "\n"
                    if message == None:
                        message = "У тебя нет легендарок!"
            message = f"""▶️ {user_name[0]}
Твои  легендарки:
{message}"""
            await cursor.close()
            return message
    except Exception as e:
         print(e)
    return message

#получение эпик персов
async def epic(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            message = ""
            cursor = await conn.execute(f"SELECT user_name FROM users WHERE user_id = {user_id}")
            user_name = await cursor.fetchone()
            cursor = await conn.execute(f"SELECT * FROM personEpic WHERE user_id = {user_id}")
            row = await cursor.fetchone()
            columns = [description[0] for description in cursor.description]
            for i in range(1, len(columns)):
                if row[i] != 0:
                    message += f"{columns[i]}: {row[i]}⭐️⭐️⭐️⭐️"
                    if i < len(columns) - 1:
                        message += "\n"
                    if message == None:
                        message = "У тебя нет эпиков!"
            message = f"""▶️ {user_name[0]}
Твои эпики:
{message}"""
            await cursor.close()
            return message
    except Exception as e:
         print(e)
    return message



#Смена ника
async def name(user_id, user_name):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute(f"SELECT user_name FROM users WHERE user_id = {user_id}")
            await cursor.execute("UPDATE users SET user_name = ? WHERE user_id = ?", (user_name, user_id))
            await cursor.close()
            await conn.commit()
    except Exception as e:
         await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

#Смена статуса
async def status(user_status, user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute(f"SELECT status FROM users WHERE user_id = {user_id}")
            await cursor.execute("UPDATE users SET status = ? WHERE user_id = ?", (user_status, user_id))
            await cursor.close()
            await conn.commit()
    except Exception as e:
         print(e)


#еже
async def daily(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT time, exp, user_name FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            last_request_time = row[0]
            if datetime.datetime.now().hour != last_request_time:
                amount = random.randint(30, 1200)
                exp = random.randint(10, 70)
                cursor = await conn.execute("UPDATE users SET wallet = wallet + ?, exp = exp + ? WHERE user_id = ?", (amount, exp, user_id))
                cursor = await conn.execute("UPDATE users SET time = ? WHERE user_id = ?", (datetime.datetime.now().hour, user_id))
                await cursor.close()
                await conn.commit()
                message = f"▶️ {row[2]}\nТы получил {amount} 💠 и {exp} 📜!"
            else:
                message = f"▶️ {row[2]}\nТы уже запрашивал награду.\nПопробуй через час! 🕐"
            return message
    except Exception as e:
         print(e)

#луна
async def moon(user_id, moon):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT pass_time, exp, user_name FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            last_request_time = row[0]
            if moon == True:
                if datetime.datetime.now().hour != last_request_time:
                    amount = random.randint(200, 600)
                    exp = random.randint(5, 25)
                    cursor = await conn.execute("UPDATE users SET wallet = wallet + ?, exp = exp + ? WHERE user_id = ?", (amount, exp, user_id))
                    cursor = await conn.execute("UPDATE users SET pass_time = ? WHERE user_id = ?", (datetime.datetime.now().hour, user_id))
                    await cursor.close()
                    await conn.commit()
                    message = f"▶️ {row[2]}\nТы получил {amount} 💠 и {exp} 📜!"
                else:
                    message = f"▶️ {row[2]}\nТы уже запрашивал награду.\nПопробуй через час! 🕐"
            else:
                message = f"▶️ Отказано!\n{row[2]}, что бы получать дополнительные подарки, оформи подписку Telegram Premium :)"
            return message
    except Exception as e:
         print(e)


#баннер
async def banner():
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT * FROM personLegend LIMIT 1")
            columns = [description[0] for description in cursor.description]
            cursor = await conn.execute("SELECT banner FROM help")
            banner_data = await cursor.fetchone()
            banner_index = banner_data[0]
            banner_ = columns[banner_index]
            message = f"""▶️Сегодня баннер: 🪝{banner_}🪝"""
            await cursor.close()
            return message
    except Exception as e:  
         print(e)


# Обновление баннера
async def change_banner():
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT banner FROM help")
            row = await cursor.fetchone()
            if row is None:
                current_banner = 1
            else:
                current_banner = row[0]
            new_banner = current_banner + 1 
            BazaLeg = [7, 8, 15, 16, 24, 26, 31]
            while new_banner in BazaLeg:
                new_banner += 1
            if current_banner >= 30:
                new_banner = 1
            print(current_banner)
            await conn.execute("UPDATE help SET banner = ?", (new_banner,))
            await cursor.close()
            await conn.commit()
    except Exception as e:
        print(e)

#Обновление баннера
async def examination_banner(banner_day):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT banner_day FROM help")
            row = await cursor.fetchone()
            bannerDayBd = row[0]
            if banner_day != bannerDayBd:
                await change_banner()
                cursor = await conn.execute("UPDATE help SET banner_day = ?", (banner_day,))
                await cursor.close()
                await conn.commit()
    except Exception as e:
        print(e)

#Получение даных об пользователе
async def info_twist(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT exp, wallet, guarantee, hystory, hystoryEpic FROM users WHERE user_id = ?", (user_id,))
            info = await cursor.fetchone()
            info = info
            await cursor.close()
        return info
    except Exception as e:
        print(e)

#Крутки...
async def twist(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.cursor()
            chance = 0.005
            reward = []
            prim = 0
            cursor = await conn.execute("SELECT * FROM personLegend LIMIT 1")
            columns = [description[0] for description in cursor.description]
            cursor = await conn.execute("SELECT banner FROM help")
            banner_data = await cursor.fetchone()
            if banner_data is not None and banner_data[0] is not None:
                banner_index = banner_data[0]
                banner = columns[banner_index] 
            ignore_column = 'user_id'
            cursor = await conn.execute("SELECT * FROM personEpic LIMIT 1") 
            columnsEpic = [description[0] for description in cursor.description if description[0] != ignore_column]
            three_star = ["Эпос драконоборцах", "Чёрная кисть", "Холодное лезвие", "Филейный нож", "Тёмный меч", "Рогатка", "Предвестник зари", "Потусторонняя история", "Посыльный", "Парный нефрит", "Меч", "Меч всадника", "Меч из железа", "Меч крови", "Металлическая тень", "Лук ворона", "Клятва стрелка", "Изумрудный шар","Изогнутый лук", "Дубина переговоров", "Большой меч", "Белая кисть", "Алебарда Миллелита"]
            for i in range(10):
                cursor = await conn.execute("SELECT exp, wallet, guarantee, hystory, hystoryEpic, user_name FROM users WHERE user_id = ?", (user_id,))
                info = await cursor.fetchone()
                leg = random.choice((7, 8, 15, 16, 24, 26, 31))
                banner_baza = columns[leg]
                if info[3] >= 80:
                    if info[2] == 2:
                        cursor = await conn.execute(f"SELECT {banner} FROM personLegend WHERE user_id = ?", (user_id,))
                        current_value = await cursor.fetchone()
                        if current_value is not None:
                            new_value = current_value[0] + 1
                            if new_value <= 6:
                                cursor = await conn.execute(f"UPDATE personLegend SET {banner} = ? WHERE user_id = ?", (new_value, user_id))
                                cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (1, 0, user_id))
                                reward.append(f"🟨<b>{(banner)}⭐⭐⭐⭐⭐</b>\n")
                                await conn.commit()
                            else:
                                prim += 1600
                                cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (1, 0, user_id))
                                reward.append(f"🟨<b>{(banner)}⭐⭐⭐⭐⭐(1600💠)</b>\n")                        
                                await conn.commit()
                    else:
                        if random.randint(1, 2) == 1:
                            cursor = await conn.execute(f"SELECT {banner_baza} FROM personLegend WHERE user_id = ?", (user_id,))
                            current_value = await cursor.fetchone()
                            if current_value is not None:
                                new_value = current_value[0] + 1
                                if new_value <= 6:
                                    cursor = await conn.execute(f"UPDATE personLegend SET {banner_baza} = ? WHERE user_id = ?", (new_value, user_id))
                                    cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (2, 0, user_id))
                                    reward.append(f"🟨<b>{(banner_baza)}⭐⭐⭐⭐⭐</b>\n")
                                    await conn.commit()
                                else:
                                    prim += 1600
                                    reward.append(f"🟨<b>{(banner_baza)}⭐⭐⭐⭐⭐(1600💠)</b>\n")   
                                    cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (2, 0, user_id))
                                    await conn.commit()
                        else:
                            cursor = await conn.execute(f"SELECT {banner} FROM personLegend WHERE user_id = ?", (user_id,))
                            current_value = await cursor.fetchone()
                            if current_value is not None:
                                new_value = current_value[0] + 1
                                if new_value <= 6:
                                    cursor = await conn.execute(f"UPDATE personLegend SET {banner} = ? WHERE user_id = ?", (new_value, user_id))
                                    cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (1, 0, user_id))
                                    await conn.commit()
                                    reward.append(f"🟨<b>{(banner)}⭐⭐⭐⭐⭐</b>\n")
                                else:
                                    prim += 1600
                                    cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (1, 0, user_id))
                                    reward.append(f"🟨<b>{(banner)}⭐⭐⭐⭐⭐(1600💠)</b>\n")
                                    await conn.commit()
                else:
                    result = random.choices([0, 1], weights=[1 - chance, chance])[0]
                    if result == 1:
                        if info[2] == 2:
                            cursor = cursor = await conn.execute(f"SELECT {banner} FROM personLegend WHERE user_id = ?", (user_id,))
                            current_value = await cursor.fetchone()
                            if current_value is not None:
                                new_value = current_value[0] + 1
                                if new_value <= 6:
                                    cursor = await conn.execute(f"UPDATE personLegend SET {banner} = ? WHERE user_id = ?", (new_value, user_id))
                                    cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (1, 0, user_id))
                                    await conn.commit()
                                    reward.append(f"🟨<b>{(banner)}⭐⭐⭐⭐⭐</b>\n")
                                else:
                                    prim += 1600
                                    cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (1, 0, user_id))
                                    reward.append(f"🟨<b>{(banner)}⭐⭐⭐⭐⭐(1600💠)</b>\n")
                                    await conn.commit()
                        else:
                            if random.randint(1, 2) == 1:
                                cursor = await conn.execute(f"SELECT {banner_baza} FROM personLegend WHERE user_id = ?", (user_id,))
                                current_value = await cursor.fetchone()
                                if current_value is not None:
                                    new_value = current_value[0] + 1
                                    if new_value <= 6:
                                        cursor = await conn.execute(f"UPDATE personLegend SET {banner_baza} = ? WHERE user_id = ?", (new_value, user_id))
                                        cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (2, 0, user_id))
                                        await conn.commit()
                                        reward.append(f"🟨<b>{(banner_baza)}⭐⭐⭐⭐⭐</b>\n")
                                    else:
                                        prim += 1600
                                        cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (2, 0, user_id))
                                        reward.append(f"<b>🟨{(banner_baza)}⭐⭐⭐⭐⭐(1600💠)</b>\n")
                                        await conn.commit()
                            else:
                                cursor = await conn.execute(f"SELECT {banner} FROM personLegend WHERE user_id = ?", (user_id,))
                                current_value = await cursor.fetchone()
                                if current_value is not None:
                                    new_value = current_value[0] + 1
                                    if new_value <= 6:
                                        cursor = await conn.execute(f"UPDATE personLegend SET {banner} = ? WHERE user_id = ?", (new_value, user_id))
                                        cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (1, 0, user_id))
                                        await conn.commit()
                                        reward.append(f"🟨<b>{(banner)}⭐⭐⭐⭐⭐</b>\n")
                                    else:
                                        prim += 1600
                                        reward.append(f"🟨<b>{(banner)}⭐⭐⭐⭐⭐(1600💠)</b>\n")
                                        cursor = await conn.execute("UPDATE users SET guarantee = ?, hystory = ?, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (1, 0, user_id))
                                        await conn.commit()
                    else:
                        if info[4] >= 9:
                            epic = random.choice(columnsEpic)
                            cursor = await conn.execute(f"SELECT {epic} FROM personEpic WHERE user_id = ?", (user_id,))
                            current_value = await cursor.fetchone()
                            if current_value is not None:
                                new_value = current_value[0] + 1
                                if new_value <= 6:
                                    cursor = await conn.execute(f"UPDATE personEpic SET {epic} = ? WHERE user_id = ?", (new_value, user_id))
                                    cursor = await conn.execute("UPDATE users SET hystoryEpic = ?, hystory = hystory + 1 WHERE user_id = ?", (0, user_id))
                                    await conn.commit()
                                    reward.append(f"🟪<b>{(epic)}⭐⭐⭐⭐</b>\n")
                                else:
                                    prim += 400
                                    reward.append(f"🟪<b>{(epic)}⭐⭐⭐⭐(400💠)</b>\n")
                                    cursor = await conn.execute("UPDATE users SET hystoryEpic = ?, hystory = hystory + 1 WHERE user_id = ?", (0, user_id))
                                    await conn.commit()
                        else:
                            chanceEpic = 6
                            resultEpic = random.choices([0, 1], weights=[100 - chanceEpic, chanceEpic])[0]
                            if resultEpic == 1:
                                epic = random.choice(columnsEpic)
                                cursor = await conn.execute(f"SELECT {epic} FROM personEpic WHERE user_id = ?", (user_id,))
                                current_value = await cursor.fetchone()
                                if current_value is not None:
                                    new_value = current_value[0] + 1
                                    if new_value <= 6:
                                        cursor = await conn.execute(f"UPDATE personEpic SET {epic} = ? WHERE user_id = ?", (new_value, user_id))
                                        cursor = await conn.execute("UPDATE users SET hystory = hystory + 1 WHERE user_id = ?", (user_id,))
                                        await conn.commit()
                                        reward.append(f"<b>🟪{(epic)}⭐⭐⭐⭐</b>\n")
                                    else:
                                        prim += 400
                                        reward.append(f"<b>🟪{(epic)}⭐⭐⭐⭐(400💠)</b>\n")
                                        cursor = await conn.execute("UPDATE users SET hystory = hystory + 1 WHERE user_id = ?", (user_id,))
                                        await conn.commit()
                            else:
                                reward.append(f"⬜️{random.choice(three_star)}⭐⭐⭐\n")
                                prim += 15
                                cursor = await conn.execute("UPDATE users SET hystory = hystory + 1, hystoryEpic = hystoryEpic + 1 WHERE user_id = ?", (user_id,))
                                await conn.commit()
            cursor = await conn.execute(f"UPDATE users SET exp = exp + 150, wallet = (wallet - 1600) + {prim} WHERE user_id = ?", (user_id,))
            await conn.commit()
            await cursor.close()
        message_twist_str = "".join(reward)
        message_banner = f"""▶️{info[5]}
Твоя награда:\n
{message_twist_str}
▶️Примогемы: {prim} 💠
▶️Опыт: 150 📜"""
        return f"{message_banner}"
    except Exception as e:
        traceback.print_exc()

#Кости
async def bones(user_id, number):
    try:
        if isinstance(number, int):
            if number > 0:
                async with aiosqlite.connect('BD') as conn:
                    cursor = await conn.cursor()
                    await cursor.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
                    wallet_row = await cursor.fetchone()
                    cursor = await conn.execute(f"SELECT user_name FROM users WHERE user_id = {user_id}")
                    user_name = await cursor.fetchone()
                    await cursor.close()
                    if wallet_row is not None:
                        wallet = wallet_row[0]
                        if number <= wallet:
                            if random.randint(1, 2) == 1:
                                wallet += number * 2
                                message = f"▶️{user_name}\nТебе повезло.🎲\nТы выиграл {number*2} 💠!"
                                cursor = await conn.execute("UPDATE users SET wallet = ? WHERE user_id = ?", (wallet, user_id))
                                await cursor.close()
                                await conn.commit()
                            else:
                                message = f"Я выиграл. Примогемов не будет. ☠️"
                                cursor = await conn.execute("UPDATE users SET wallet = wallet - ? WHERE user_id = ?", (number, user_id))
                                await cursor.close()
                                await conn.commit()
                        else:
                            message = "▶️У тебя недостаточно примогемов! 🧮\nЕсли что-то не понятно - пиши /помощь"
                    else:
                        message = "▶️Произошла ошибка при получении кошелька пользователя! 🚫\nЕсли что-то не понятно - пиши /помощь"
            else:
                message = "▶️Число должно быть больше нуля ☠️\nЕсли что-то не понятно - пиши /помощь"
        else:
            message = "▶️Введи число после команды! 🕯️\nЕсли что-то не понятно - пиши /помощь"
        return message
    except Exception as e:
        traceback.print_exc()

#Проверка промокода
async def promo(promo, user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT promo, status, reward FROM promo WHERE promo = ?", (promo,))
            promo_data = await cursor.fetchone()
            await cursor.close()
            if promo_data is None:
                message = "▶️Такого промокода нет, хитрец)"
            else:
                if promo_data[1] == 0:
                    cursor = await conn.execute("SELECT COUNT(*) FROM promo WHERE status = ?", (user_id,))
                    count = await cursor.fetchone()
                    await cursor.close()
                    if count[0] > 0:
                        message = "▶️Ты уже активировал промокод в этой партии!"
                    else:
                        await conn.execute("UPDATE promo SET status = ? WHERE promo = ?", (user_id, promo))
                        await conn.commit()
                        await conn.execute(f"UPDATE users SET wallet = wallet + {promo_data[2]} WHERE user_id = ?", (user_id,))
                        await conn.commit()
                        message = f"▶️Твоя награда:{promo_data[2]} 💠!"
                else:
                    message = "▶️Этот промокод уже использовали"
            return message
    except Exception as e:
        traceback.print_exc()

#Передача примогемов
async def hand(number, user_id, user_id2):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
            wallet = await cursor.fetchone()
            await cursor.close()
            if wallet[0] >= number:
                await conn.execute(f"UPDATE users SET wallet = wallet - {number} WHERE user_id = ?", (user_id,))
                await conn.execute(f"UPDATE users SET wallet = wallet + {number} WHERE user_id = ?", (user_id2,))
                await conn.commit()
                message = "▶️Успешно!"
            else:
                message = "▶️У тебя недостаточно примогемов!"
            return message
    except Exception as e:
        traceback.print_exc()

async def rank(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.execute("SELECT exp, user_name FROM users WHERE user_id = ?", (user_id,))
            exp = await cursor.fetchone()
            await cursor.close()
            rank_new = exp[0]//1000
            if rank_new > 0:
                exp_ = rank_new * 1000
                await conn.execute(f"UPDATE users SET exp = exp - {exp_}, rank = rank + {rank_new}, wallet = wallet + ({rank_new} * 1000) WHERE user_id = ?", (user_id,))
                await conn.commit()
                message = f"""▶️{exp[1]}
Твой уровень повышен на {rank_new}!
Твоя награда: {rank_new * 1000} 💠!
                """
            else:
                message = "▶️У тебя не хватает опыта!"
            return message
    except Exception as e:
        traceback.print_exc()

async def info_kettle(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            cursor = await conn.cursor()
            await cursor.execute("SELECT * FROM kettle WHERE user_id = ?", (user_id,))
            kettle = await cursor.fetchone()
            await cursor.execute("SELECT user_name FROM users WHERE user_id = ?", (user_id,))
            user_name = await cursor.fetchone()
            await cursor.close()
        return kettle
    except Exception as e:
        traceback.print_exc()

async def up(mod, user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            async with conn.cursor() as cursor:
                if mod == 1:
                    await cursor.execute("SELECT home FROM kettle WHERE user_id = ?", (user_id,))
                    hom = await cursor.fetchone()
                    await cursor.execute("SELECT wallet, user_name FROM users WHERE user_id = ?", (user_id,))
                    wallet = await cursor.fetchone()
                    up_price = (hom[0] + 1 ) * 4000
                    if hom[0] <= 4:
                        if wallet[0] >= up_price:
                            await conn.execute(f"UPDATE users SET wallet = wallet - {up_price} WHERE user_id = ?", (user_id,))
                            await conn.execute(f"UPDATE kettle SET home = home + 1 WHERE user_id = ?", (user_id,))
                            await conn.commit()
                            message = f"▶️{wallet[1]}\Ты прокочал дом на 1 уровень!"
                        else:
                            message = f"▶️{wallet[1]}\nУ тебя не хватает примогемов!\nСтоимость прокачки: {up_price} 💠"
                    else:
                        message = f"▶️{wallet[1]}\nПостройка максимального уровня!"
                    
                if mod == 2:
                    await cursor.execute("SELECT pool FROM kettle WHERE user_id = ?", (user_id,))
                    hom = await cursor.fetchone()
                    await cursor.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
                    wallet = await cursor.fetchone()
                    up_price = (hom[0] + 1 ) * 4000
                    if hom[0] <= 4:
                        if wallet[0] >= up_price:
                            await conn.execute(f"UPDATE users SET wallet = wallet - {up_price} WHERE user_id = ?", (user_id,))
                            await conn.execute(f"UPDATE kettle SET pool = pool + 1 WHERE user_id = ?", (user_id,))
                            await conn.commit()
                            message = f"▶️{wallet[1]}\nТы прокочал обустройвство на 1 уровень!"
                        else:
                            message = f"▶️{wallet[1]}\nУ тебя не хватает примогемов!\nСтоимость прокачки: {up_price} 💠"
                    else:
                        message = f"▶️{wallet[1]}\nПостройка максимального уровня!"
                    
                if mod == 3:
                    await cursor.execute("SELECT fence FROM kettle WHERE user_id = ?", (user_id,))
                    hom = await cursor.fetchone()
                    await cursor.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
                    wallet = await cursor.fetchone()
                    up_price = (hom[0] + 1 ) * 4000
                    if hom[0] <= 4:
                        if wallet[0] >= up_price:
                            await conn.execute(f"UPDATE users SET wallet = wallet - {up_price} WHERE user_id = ?", (user_id,))
                            await conn.execute(f"UPDATE kettle SET fence = fence + 1 WHERE user_id = ?", (user_id,))
                            await conn.commit()
                            message = f"▶️{wallet[1]}\nТы прокочал бассейн на 1 уровень!"
                        else:
                            message = f"▶️{wallet[1]}\nУ тебя не хватает примогемов!\nСтоимость прокачки: {up_price} 💠"
                    else:
                        message = f"▶️{wallet[1]}\nПостройка максимального уровня!"
                    
                if mod == 4:
                    await cursor.execute("SELECT home_improvement FROM kettle WHERE user_id = ?", (user_id,))
                    hom = await cursor.fetchone()
                    await cursor.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
                    wallet = await cursor.fetchone()
                    up_price = (hom[0] + 1 ) * 4000
                    if hom[0] <= 4:
                        if wallet[0] >= up_price:
                            await conn.execute(f"UPDATE users SET wallet = wallet - {up_price} WHERE user_id = ?", (user_id,))
                            await conn.execute(f"UPDATE kettle SET home_improvement = home_improvement + 1 WHERE user_id = ?", (user_id,))
                            await conn.commit()
                            message =f"▶️{wallet[1]}\nТыы прокочал ограждение на 1 уровень!"
                        else:
                            message = f"▶️{wallet[1]}\nУ тебя не хватает примогемов!\nСтоимость прокачки: {up_price} 💠"
                    else:
                        message = f"▶️{wallet[1]}\nПостройка максимального уровня!"
                    
                if mod == 5:
                    await cursor.execute("SELECT scenery FROM kettle WHERE user_id = ?", (user_id,))
                    hom = await cursor.fetchone()
                    await cursor.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
                    wallet = await cursor.fetchone()
                    up_price = (hom[0] + 1 ) * 5000
                    if hom[0] <= 4:
                        if wallet[0] >= up_price:
                            await conn.execute(f"UPDATE users SET wallet = wallet - {up_price} WHERE user_id = ?", (user_id,))
                            await conn.execute(f"UPDATE kettle SET scenery = scenery + 1 WHERE user_id = ?", (user_id,))
                            await conn.commit()
                            message = f"▶️{wallet[1]}\nТыы прокочал пейзаж на 1 уровень!"
                        else:
                            message = f"▶️{wallet[1]}\nУ тебя не хватает примогемов!\nСтоимость прокачки: {up_price} 💠"
                    else:
                        message = f"▶️{wallet[1]}\nПостройка максимального уровня!"
                await cursor.close()
                return message
    except Exception as e:
        traceback.print_exc()

async def blessing(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT home, pool, fence, home_improvement, scenery FROM kettle')
                rows = await cursor.fetchall()
                cursor = await conn.execute(f"SELECT user_name FROM users WHERE user_id = {user_id}")
                user_name = await cursor.fetchone()
                result_sum = sum(sum(row) for row in rows)
                reward = result_sum * 300
                data = datetime.datetime.now().day
                data = data
                print(data)
                await cursor.execute('SELECT hom_time FROM users WHERE user_id = ?',(user_id,))
                time = await cursor.fetchall()
                print(time)
                print(time[0][0])
                if time[0][0] != data:
                    await conn.execute("UPDATE users SET wallet = wallet + ?, hom_time = ? WHERE user_id = ?", (reward, data, user_id))
                    await conn.commit()
                    message = f"▶️{user_name[0]}\nТвоя награда: {reward} примогемов 💠"
                else: 
                    message = f"▶️{user_name[0]}\nТы уже получал сегодня благословеение!\nПриходи завтра!"
            await cursor.close()
            return message
    except Exception as e:
        traceback.print_exc()


async def price(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f'SELECT home, pool, fence, home_improvement, scenery FROM kettle WHERE user_id = {user_id}')
                rows = await cursor.fetchall()
                cursor = await conn.execute(f"SELECT user_name FROM users WHERE user_id = {user_id}")
                user_name = await cursor.fetchone()

                # Home
                if rows[0][0] == 5:
                    hom = "Максимальный уровень"
                if rows[0][0] == 0:
                    hom = 5000  
                else:
                    hom = (rows[0][0] + 1)  * 4000

                # Pool
                if rows[0][1] == 5:
                    pool = "Максимальный уровень"
                if rows[0][1] == 0:
                    pool = 5000
                else:
                    pool = (rows[0][1] + 1) * 4000

                # Fence
                if rows[0][2] == 5:
                    fence = "Максимальный уровень"
                if rows[0][2] == 0:
                    fence = 5000                    
                else:
                    fence = (rows[0][2] + 1) * 4000

                # Home Improvement
                if rows[0][3] == 5:
                    home_imp = "Максимальный уровень"
                if rows[0][3] == 0:
                    home_imp = 5000
                else:
                    home_imp = (rows[0][3] + 1) * 4000

                # Scenery
                if rows[0][4] == 5:
                    scenery = "Максимальный уровень"
                if rows[0][4] == 0:
                    scenery = 5000
                else:
                    scenery = (rows[0][4] + 1) * 5000

                message = f"""▶️ {user_name[0]}
Цена твоей прокачки          
Дом: {hom} 💠
Обустройство: {pool} 💠
Бассейн: {fence} 💠
Ограждение: {home_imp} 💠
Пейзаж: {scenery} 💠

Пример улучшения
/up дом
/up обустройство
/up бассейн
/up ограждение
/up пейзаж"""
                return message
    except Exception as e:
        traceback.print_exc()

async def view(user_id):
    try:
        async with aiosqlite.connect('BD') as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT mod, user_name FROM users WHERE user_id = ?', (user_id,))
                info = await cursor.fetchone()
                if info[0] == 3:
                    mod = 1
                else:
                    mod = info[0] + 1
                await conn.execute("UPDATE users SET mod = ? WHERE user_id = ?", (mod, user_id))
                await conn.commit()
                message = f"▶️{info[1]}\nТеперь вид твоего аккаунта изменен!"
                return message
    except Exception as e:
        traceback.print_exc()

#,kf ,kf ,kf