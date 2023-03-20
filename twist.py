import lib

async def twist(user_id):
    try:
        info = await lib.info_twist(user_id = user_id)
        if info[1] >= 1600:
            message = await lib.twist(user_id = user_id)
        else:
            message = "У тебя не хватает примогемов! 💠\nЕсли что-то не понятно - пиши /помощь"
        return message
    except Exception as e:
        print(e)