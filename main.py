import asyncio
import time
from telebot.async_telebot import AsyncTeleBot
from lib import *

TOKEN = '...'

bot = AsyncTeleBot(TOKEN)
users = {}


@bot.message_handler(commands=['start'])
async def start(message):
    if not (message.chat.id in users):
        users[message.chat.id] = User(bot, message.chat.id)
    user = users[message.chat.id]
    await user.send_photo()


@bot.callback_query_handler(lambda call: True)
async def menu(call: types.CallbackQuery):
    if not (call.message.chat.id in users):
        users[call.message.chat.id] = User(bot, call.message.chat.id)
    user = users[call.message.chat.id]
    user.last_message = call.message.message_id
    message_text = call.data
    if message_text == "top":
        await user.move_top()
    elif message_text == "left":
        await user.move_left()
    elif message_text == "right":
        await user.move_right()
    elif message_text == "bottom":
        await user.move_bottom()
    elif message_text == "red":
        user.change_color((255, 0, 0))
    elif message_text == "green":
        user.change_color((0, 255, 0))
    elif message_text == "blue":
        user.change_color((0, 0, 255))
    elif message_text == "white":
        user.change_color((255, 255, 255))
    elif message_text == "orange":
        user.change_color((255, 165, 0))
    elif message_text == "purple":
        user.change_color((139, 0, 255))
    elif message_text == "black":
        user.change_color((0, 0, 0))
    elif message_text == "clear":
        user.clear_canvas()
    elif message_text == "save":
        await user.save()
    elif message_text == "gif":
        await user.gif()
    await user.edit_photo(call.id)


async def main():
    await asyncio.gather(bot.infinity_polling(timeout=120))


# Run
if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except Exception:
            time.sleep(1)
