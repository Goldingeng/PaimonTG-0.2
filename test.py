import asyncio
import aiosqlite
import datetime
import traceback

async def blessing():
    try:
        user_id = 686897095
        async with aiosqlite.connect('BD') as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT home, pool, fence, home_improvement, scenery FROM kettle')
                rows = await cursor.fetchall()
                result_sum = sum(sum(row) for row in rows)
                reward = result_sum * 500
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
                    message = f"▶️Успешно!\nТвоя награда: {reward} примогемов 💠"
                else: 
                    message = "▶️Ты уже получал сегодня благословеение!\nПриходи завтра!"
            await cursor.close()
            return message
    except Exception as e:
        traceback.print_exc()

async def main():
    message = await blessing()
    print(message)

asyncio.run(main())
