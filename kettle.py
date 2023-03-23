import lib

async def main(user_id):
    try:
        kettle_info = await lib.info_kettle(user_id = user_id)
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

        fence = "Отсутствует" if kettle_info[3] == 0 else "Деревянный забор 🪵" \
                   if kettle_info[3] == 1 else "Каменный забор 🪨" \
                   if kettle_info[3] == 2 else "Горы ⛰️" \
                   if kettle_info[3] == 3 else "Холодные горы 🏔️" \
                   if kettle_info[3] == 4 else "Вулкан 🌋"

        home_improvement = "Отсутствует" if kettle_info[4] == 0 else "Советский ремонт 🪑" \
                   if kettle_info[4] == 1 else "Современная отделка 🧱" \
                   if kettle_info[4] == 2 else "Евро ремонт 🪞" \
                   if kettle_info[4] == 3 else "Дизайнерский ремонт 🛋️" \
                   if kettle_info[4] == 4 else "Кастомный ремонт 🚽" 

        scenery = "Отсутствует" if kettle_info[5] == 0 else "Туман 🌫️" \
                   if kettle_info[5] == 1 else "Пустыня 🏜️" \
                   if kettle_info[5] == 2 else "Гора 🏞️" \
                   if kettle_info[5] == 3 else "Восход 🌅" \
                   if kettle_info[5] == 4 else "Восход за горами 🌄" 

        message = f"""<b>Чайник</b>
 
<b>Дом:</b>  {home}
<b>Обустройство:</b> {home_improvement}
<b>Бассейн:</b>  {pool}
<b>Ограждение:</b>  {fence}
<b>Пейзаж:</b>  {scenery}"""
        return message
    except Exception as e:
        print(e)