from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import lib
import asyncio
import datetime
import aioschedule as schedule
import twist
import traceback
import kettle
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = "5409304847:AAGtNYiN8p_GtHzvYZLQB6S6oGG2sMAwHv0"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["reg", "рег"])
async def reg_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.full_name
        if await lib.is_user_registered(user_id=user_id):
            text = "А кто у нас такой умный?\nНе, друг. Я тебя уже знаю)"
        else:
            await lib.login_user(user_id=user_id, user_name=user_name)
            text = "Приятно познакомиться!\nНапиши /help для дальнейшего взаимодействия"
        await message.reply(text)
    except Exception as error: 
        traceback.print_exc()
        await bot.send_message(chat_id=1167542251, text=f"{error}\nreg_handler")


@dp.message_handler(commands=["acc", "акк"])
async def acc_handler(message: types.Message):
    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text="🫖", callback_data="kettle")
                keyboard.row(button1)
                button2 = types.InlineKeyboardButton(text="🟪", callback_data="epic")
                button3 = types.InlineKeyboardButton(text="🟨", callback_data="leg")
                keyboard.row(button2, button3)
                button4 = types.InlineKeyboardButton(text="Вид", callback_data="view")
                button5 = types.InlineKeyboardButton(text="Баннер", callback_data="banner")
                keyboard.row(button4, button5)
                await message.reply(acc_message, parse_mode='HTML', reply_markup=keyboard)
            else:
                await message.reply("Этот пользователь еще не зарегистрирован!")
        else:
            user_id = message.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                acc_message = await lib.acc(user_id)
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text="🫖", callback_data="kettle")
                keyboard.row(button1)
                button2 = types.InlineKeyboardButton(text="🟪", callback_data="epic")
                button3 = types.InlineKeyboardButton(text="🟨", callback_data="leg")
                keyboard.row(button2, button3)
                button4 = types.InlineKeyboardButton(text="Вид", callback_data="view")
                button5 = types.InlineKeyboardButton(text="Баннер", callback_data="banner")
                keyboard.row(button4, button5)
                await message.reply(acc_message, parse_mode='HTML', reply_markup=keyboard)
            else:
                await reg_handler(message)
                await acc_handler(message)
    except Exception as e:
        traceback.print_exc()
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.callback_query_handler(lambda c: c.data == 'banner')
async def banner_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await bot.answer_callback_query(callback_query.id)
            message = callback_query.message
            banner_msg = await lib.banner()
            banner_day = message.date.day
            await lib.examination_banner(banner_day = banner_day)
            with open("banner.jpg", "rb") as file:
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text="Крутка", callback_data="twist")
                keyboard.row(button1)
                await bot.send_photo(chat_id=message.chat.id, photo=file, caption=banner_msg, reply_to_message_id=message.message_id, reply_markup=keyboard)
        else:
            await bot.answer_callback_query(callback_query.id, text='Вы должны зарегистрироваться, чтобы использовать эту функцию!')
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.callback_query_handler(lambda c: c.data == 'view')
async def view_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await bot.answer_callback_query(callback_query.id)
            message = callback_query.message
            user_id = callback_query.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                await bot.send_message(chat_id=callback_query.message.chat.id, text=await lib.view(user_id = user_id), parse_mode='HTML')
            else:
                await reg_handler(message)
                await view_callback_handler(callback_query)
        else:
            await bot.answer_callback_query(callback_query.id, text='Вы должны зарегистрироваться, чтобы использовать эту функцию!')
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.callback_query_handler(lambda c: c.data == 'leg')
async def leg_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await bot.answer_callback_query(callback_query.id)
            message = callback_query.message
            user_id = callback_query.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                epic_message = await lib.leg(user_id)
                await bot.send_message(chat_id=callback_query.message.chat.id,text=epic_message, parse_mode='HTML')
            else:
                await reg_handler(message)
                await leg_handler(message)
        else:
            await bot.answer_callback_query(callback_query.id, text='Вы должны зарегистрироваться, чтобы использовать эту функцию!')
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.callback_query_handler(lambda c: c.data == 'epic')
async def epic_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await bot.answer_callback_query(callback_query.id)
            message = callback_query.message
            user_id = callback_query.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                epic_message = await lib.epic(user_id)
                await bot.send_message(chat_id=callback_query.message.chat.id,text=epic_message, parse_mode='HTML')
            else:
                await reg_handler(message)
                await epic_handler(message)
        else:
            await bot.answer_callback_query(callback_query.id, text='Вы должны зарегистрироваться, чтобы использовать эту функцию!')
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.callback_query_handler(lambda c: c.data == 'kettle')
async def kettle_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="🔨", callback_data="price")
            button2 = types.InlineKeyboardButton(text="🙏", callback_data="blessing")
            button3 = types.InlineKeyboardButton(text="🌞", callback_data="daily")
            button4 = types.InlineKeyboardButton(text="🌕", callback_data="moon")
            keyboard.row(button1, button2, button3, button4)
            button5 = types.InlineKeyboardButton(text="🆙", callback_data="rank")
            keyboard.row(button5)
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(chat_id=callback_query.message.chat.id, text=await kettle.main(user_id=user_id), parse_mode='HTML', reply_markup=keyboard)
        else:
            await bot.answer_callback_query(callback_query.id, text='Вы должны зарегистрироваться, чтобы использовать эту функцию!')
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.message_handler(commands=["kettle", "чайник"])
async def kettle_handler(message: types.Message):
    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            mod = 1
        else:
            user_id = message.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="🔨", callback_data="price")
            button2 = types.InlineKeyboardButton(text="🙏", callback_data="blessing")
            button3 = types.InlineKeyboardButton(text="🌞", callback_data="daily")
            button4 = types.InlineKeyboardButton(text="🌕", callback_data="moon")
            keyboard.row(button1, button2, button3, button4)
            button5 = types.InlineKeyboardButton(text="🆙", callback_data="rank")
            keyboard.row(button5)
            await message.reply(text=await kettle.main(user_id=user_id), parse_mode="HTML", reply_markup=keyboard)
        else:
            if mod == 1:
                await message.reply(text='Этот пользователь еще не зарегестрировался!')
            else:
                await reg_handler(message)
                await kettle_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.callback_query_handler(lambda c: c.data == "moon")
async def moon_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        moon = callback_query.from_user.is_premium
        if await lib.is_user_registered(user_id=user_id):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.message.chat.id, await lib.moon(user_id=user_id, moon=moon))
        else:
            await reg_handler(callback_query.message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")



@dp.callback_query_handler(lambda c: c.data == "rank")
async def rank_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.message.chat.id, await lib.rank(user_id=user_id))
        else:
            await reg_handler(callback_query.message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.callback_query_handler(lambda c: c.data == 'daily')
async def daily_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(chat_id=callback_query.message.chat.id, text=await lib.daily(user_id=user_id))
        else:
            await reg_handler(callback_query.message)
            await bot.answer_callback_query(callback_query.message.chat.id, text="Вы не зарегистрированы.")
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.callback_query_handler(lambda c: c.data == "blessing")
async def blessing_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.message.chat.id, await lib.blessing(user_id=user_id))
        else:
            await reg_handler(callback_query.message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.message_handler(commands=["rank", "ранг"])
async def rank_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text = await lib.rank(user_id = user_id))
        else:
            await reg_handler(message)
            await rank_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.callback_query_handler(text='price')
async def price_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            price = await lib.price(user_id=user_id)
            await bot.send_message(chat_id=callback_query.message.chat.id, text=price)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.message_handler(commands=["rank", "ранг"])
async def rank_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text = await lib.rank(user_id = user_id))
        else:
            await reg_handler(message)
            await rank_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")



@dp.message_handler(commands=["price", "цена"])
async def price_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text = await lib.price(user_id = user_id))
    except Exception as e:
        traceback.print_exc()


@dp.message_handler(commands=["leg", "леги"])
async def leg_handler(message: types.Message):
    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                leg_message = await lib.leg(user_id)
                await message.reply(text=leg_message, parse_mode='HTML')
            else:
                await message.reply("Этот пользователь еще не зарегестрирован!")
        else:
            user_id = message.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                leg_message = await lib.leg(user_id)
                await message.reply(text=leg_message, parse_mode='HTML')
            else:
                await reg_handler(message)
                await leg_handler(message)
    except:
        traceback.print_exc()
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.message_handler(commands=["epic", "эпики"])
async def epic_handler(message: types.Message):
    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                leg_message = await lib.epic(user_id)
                await message.reply(text=leg_message, parse_mode='HTML')
            else:
                await message.reply("Этот пользователь еще не зарегестрирован!")
        else:
            user_id = message.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                leg_message = await lib.epic(user_id)
                await message.reply(text=leg_message, parse_mode='HTML')
            else:
                await reg_handler(message)
                await leg_handler(message)
    except:
        traceback.print_exc()
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.message_handler(commands=["nick", "ник"])
async def nick_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        args = message.text.split()[1:]
        user_name = ' '.join(args)
        if await lib.is_user_registered(user_id=user_id):
            if len(user_name) <= 15:
                await lib.name(user_name=user_name, user_id=user_id)
                await message.reply("Ник успешно изменен")
            else:
                await message.reply("Ник должен быть короче 15 символов")
        else:
            await reg_handler(message)
            await nick_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.message_handler(commands=["status", "статус"])
async def status_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        args = message.text.split()[1:]
        user_status = ' '.join(args)
        if await lib.is_user_registered(user_id=user_id):
            if len(user_status) <= 50:
                await lib.status(user_status=user_status, user_id=user_id)
                await message.reply("Статус успешно изменен")
            else:
                await message.reply("Статус должен быть короче 50 символов")
        else:
            await reg_handler(message)
            await stasus_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.message_handler(commands=["daily", "еже"])
async def daily_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text=await lib.daily(user_id=user_id))
            await acc_handler(message)
        else:
            await reg_handler(message)
            await daily_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.message_handler(commands=["moon", "луна"])
async def moon_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        moon = message.from_user.is_premium
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text= await lib.moon(user_id = user_id, moon = moon))
        else:
            await reg_handler(message)
            await moon_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.message_handler(commands=["blessing", "благословение"])
async def blessing_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text=await lib.blessing(user_id=user_id))
            await acc_handler(message)
        else:
            await reg_handler(message)
            await blessing_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.message_handler(commands=["banner", "баннер"])
async def banner_handler(message: types.Message):
    try:
        banner_msg = await lib.banner()
        banner_day = message.date.day
        await lib.examination_banner(banner_day = banner_day)
        with open("banner.jpg", "rb") as file:
            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Крутка", callback_data="twist")
            keyboard.row(button1)
            await bot.send_photo(chat_id=message.chat.id, photo=file, caption=banner_msg, reply_to_message_id=message.message_id, reply_markup=keyboard)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.callback_query_handler(lambda callback_query: callback_query.data in ["twist"])
async def twist_callback_handler(callback_query: types.CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await bot.answer_callback_query(callback_query.id)
            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Крутка", callback_data="twist")
            keyboard.row(button1)
            await bot.send_message(chat_id=callback_query.message.chat.id, text=await twist.twist(user_id=user_id), parse_mode="HTML", reply_markup=keyboard)
        else:
            await reg_handler(callback_query.message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")


@dp.message_handler(commands=["twist", "крутка"])
async def twist_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text= await twist.twist(user_id = user_id), parse_mode = "HTML")
            await acc_handler(message)
        else:
            await reg_handler(message)
            await twist_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.message_handler(commands=["bones", "кости"])
async def bones_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        bid = message.text.split()[1] if len(message.text.split()) > 1 else None
        if bid is None:
            await message.reply(text="Введи число после команды!")
            return
        try:
            number = int(bid)
        except ValueError:
            await message.reply(text="Введи число после команды!")
            return
        if number < 0:
            await message.reply(text = "Число должно быть положительным!")
            return
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text=await lib.bones(user_id=user_id, number=number), parse_mode="HTML")
            await acc_handler(message)
        else:
            await reg_handler(message)
            await bones_handler(message)
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.message_handler(commands=["promo", "промо"])
async def promo_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        args = message.text.split()[1:]
        promo = ' '.join(args)
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(await lib.promo(promo = promo, user_id = user_id))
        else:
            await reg_handler(message)
            await promo_handler(message) 
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")

@dp.message_handler(commands=["hand", "передать"])
async def hand_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        bid = message.text.split()[1] if len(message.text.split()) > 1 else None
        if bid is None:
            await message.reply(text="Введи число после команды!")
            return
        try:
            number = int(bid)
        except ValueError:
            await message.reply(text="Введи число после команды!")
            return
        if number < 0:
            await message.reply(text = "Число должно быть положительным!")
            return
        if message.reply_to_message:
            user_id2 = message.reply_to_message.from_user.id
            if await lib.is_user_registered(user_id=user_id):
                if await lib.is_user_registered(user_id=user_id2):
                    await message.reply(text=await lib.hand(user_id=user_id, number=number, user_id2=user_id2), parse_mode="HTML")
                else:
                    await message.reply(text="Пользователь еще не зарегистрирован!\nТы не можешь передать примогемы тому, кого нет)")
            else:
                await reg_handler(message)
                await hand_handler(message)
        else:
            message.reply(text = "Ответь на сообщение человека, кому хочешь передать примогемы!")
    except Exception as e:
        await bot.send_message(chat_id=1167542251, text=f"Error: {e}")
#23:30 19 Марта - ты сходишь с ума...



@dp.message_handler(commands=["up", "улучшить"])
async def up_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        args = message.text.split()[1:]
        text = ' '.join(args)
        mod = 0  # установка значения по умолчанию
        if await lib.is_user_registered(user_id=user_id):
            if text == "дом":
                mod = 1
            elif text == "обустройство":  # добавление проверки на соответствие текста
                mod = 2
            elif text == "бассейн":
                mod = 3
            elif text == "ограждение":
                mod = 4
            elif text == "пейзаж":
                mod = 5
            else:
                await message.reply("Неверный тип улучшения.")
                return
            await message.reply(text=await lib.up(user_id=user_id, mod=mod))
        else: 
            await reg_handler(message)
            await up_handler(message)
    except Exception as e:
        traceback.print_exc()

@dp.message_handler(commands=["price", "цена"])
async def price_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text = await lib.price(user_id = user_id))
    except Exception as e:
        traceback.print_exc()

@dp.message_handler(commands=["view", "вид"])
async def view_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if await lib.is_user_registered(user_id=user_id):
            await message.reply(text = await lib.view(user_id = user_id))
        else:
            await reg_handler(message)
            await view_handler(message)
    except Exception as e:
        traceback.print_exc()

@dp.message_handler(commands=["start", "помощь", "help"])
async def view_handler(message: types.Message):
    try:
        await message.reply(text ="""║ ――――――――――――――――
║<b>👋Привет!👋</b>
║Данный бот - симулятор круток из
║Genshin.🧮
║Что бы начать им пользоваться - 
║напиши /рег 
║А дальше разберешься.😎
║Вот список всех комманд:
║――――――――――――――――
║<b>/акк /acc</b> 
║показывает твой аккаунт
║――――――――――――――――
║<b>/эпики /epic</b>
║показывает ваших эпик персонажей
║――――――――――――――――
║<b>/леги /leg</b>
║показывает ваших лег персонажей
║――――――――――――――――
║<b>/крутка /twist</b> 
║крутка (база)
║――――――――――――――――
║<b>/вид /view</b>
║смена вида аккаунта
║――――――――――――――――
║<b>/еже /daily</b>
║ежечасовые примогемы
║――――――――――――――――
║<b>/благословение /blessing</b> 
║примогемы за прокачку чайника
║――――――――――――――――
║<b>/луна /moon</b>
║примогемы за тг премиум
║――――――――――――――――
║<b>/передать /hand</b> 
║передача примогемов, например /hand 1000
║――――――――――――――――
║<b>/кости /bones</b>
║игра 50/50, например /bones 300
║――――――――――――――――
║<b>/промо /promo</b>
║ввод промокод, например /promo qwerty 
║Промокоды публикуются здесь: 
║https://t.me/bannersim
║――――――――――――――――
║<b>/баннер /banner</b>
║баннер на сегодня
║――――――――――――――――
║<b>/чайник /kettle</b> 
║твой чайник
║――――――――――――――――
║<b>/ранг /rank</b>
║повышение вашего ранга, 
║если опыта >1000
║――――――――――――――――
║<b>/цена price</b>
║цена прокачки чайник
║――――――――――――――――
║<b>/улучшить /up</b>
║прокачка компонента чайника
║например /up дом
║――――――――――――――――
║<b>/ник /nick, /статус /status</b>
║просто смена ник 
║статуса /статус "сам статус'
║ ――――――――――――――――"""
, parse_mode="HTML")
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(executor.start_polling(dp))

