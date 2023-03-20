import aiosqlite
import random
import string
import asyncio

async def generate_promo_codes(number_of_codes):
    promos = set()
    while len(promos) < number_of_codes:
        word = random.choice(['Genshin', 'Golding', 'Eva', 'twist', 'Traveler', 'Paimon', 'Amber', 'Kaeya', 'Lisa', 'Jean', 'Diluc', 'Venti', 'Barbara', 'Razor', 'Bennett', 'Xiangling', 'Chongyun', 'Keqing', 'Mona', 'Qiqi', 'Klee', 'Albedo', 'Sucrose', 'Fischl', 'Beidou', 'Ningguang', 'Zhongli', 'Xingqiu', 'Diona', 'Ganyu', 'Xiao', 'Hu Tao', 'Rosaria', 'Yanfei', 'Eula', 'Kazuha', 'Ayaka'])
        code = word + '-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        promos.add(code)
    return list(promos)

async def populate_database():
    number_of_promos = int(input("How many promo codes do you want to generate? "))
    promos = await generate_promo_codes(number_of_promos)
    rewards = [random.randint(300, 1400) for _ in range(number_of_promos)]
    
    async with aiosqlite.connect('BD') as conn:
        await conn.execute("DELETE FROM promo")
        for promo, reward in zip(promos, rewards):
            await conn.execute("INSERT INTO promo (promo, reward, status) VALUES (?, ?, ?)", (promo, reward, 0))
        cursor = await conn.execute("SELECT promo FROM promo")
        all_promos = await cursor.fetchall()
        all_promos = [promo[0] for promo in all_promos]
        for promo in all_promos:
            print(promo)
        
        await conn.commit()

async def main():
    await populate_database()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
