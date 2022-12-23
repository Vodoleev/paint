from telebot import types
from PIL import Image, ImageDraw
import os
import copy

#########################################
cell_size = 21  # в пикселях
canvas_size = 31  # в клетках
quality_img = 80 # качество выводимого изображения
#########################################


def get_standard_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    color1 = types.InlineKeyboardButton(text="🟥", callback_data='red')
    color2 = types.InlineKeyboardButton(text="🟩", callback_data='green')
    color3 = types.InlineKeyboardButton(text="🟦", callback_data='blue')
    color4 = types.InlineKeyboardButton(text="🟧", callback_data='orange')
    color5 = types.InlineKeyboardButton(text="🟪", callback_data='purple')
    color6 = types.InlineKeyboardButton(text="⬛️", callback_data='black')

    v = types.InlineKeyboardButton(text="️ ", callback_data='void')
    cl = types.InlineKeyboardButton(text="️🗑", callback_data='clear')
    sv = types.InlineKeyboardButton(text="️💾", callback_data='save')
    gif = types.InlineKeyboardButton(text="gif", callback_data='gif')
    t = types.InlineKeyboardButton(text="⬆️", callback_data='top')
    l = types.InlineKeyboardButton(text="⬅️", callback_data='left')
    c = types.InlineKeyboardButton(text="⚪️", callback_data='white')
    r = types.InlineKeyboardButton(text="➡️", callback_data='right')
    b = types.InlineKeyboardButton(text="⬇️", callback_data='bottom')

    keyboard.add(color1, color2, color3)
    keyboard.add(color4, color5, color6)
    keyboard.add(cl, gif, sv)
    keyboard.add(v, t, v)
    keyboard.add(l, c, r)
    keyboard.add(v, b, v)
    return keyboard


class User:
    def __init__(self, bot, chat):
        self.bot = bot
        self.chat_id = chat
        self.last_message = 0
        self.canvas = Image.new('RGB', (canvas_size * cell_size, canvas_size * cell_size), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.canvas)
        self.coord = [canvas_size // 2, canvas_size // 2]
        self.square_animation = []
        '''
        for i in range(canvas_size):
            for j in range(canvas_size):
                self.draw.rectangle(
                    (i * cell_size, j * cell_size, i * cell_size + cell_size, j * cell_size + cell_size),
                    fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                    outline=(255, 255, 255))
        '''

    async def send_photo(self):
        save_canvas = copy.copy(self.canvas)
        draw = ImageDraw.Draw(save_canvas)
        draw.rectangle((self.coord[0] * cell_size + cell_size // 3, self.coord[1] * cell_size + cell_size // 3,
                        self.coord[0] * cell_size + 2 * cell_size // 3,
                        self.coord[1] * cell_size + 2 * cell_size // 3),
                       fill=(0, 0, 0),
                       outline=(255, 255, 255))
        save_canvas.save('./img/{}.png'.format(id(self)), quality=quality_img)
        await self.bot.send_photo(photo=open('./img/{}.png'.format(id(self)), 'rb'),
                                  reply_markup=get_standard_keyboard(), chat_id=self.chat_id)
        os.remove('./img/{}.png'.format(id(self)))

    async def edit_photo(self, call_id):
        save_canvas = copy.copy(self.canvas)
        draw = ImageDraw.Draw(save_canvas)
        draw.rectangle((self.coord[0] * cell_size + cell_size // 3, self.coord[1] * cell_size + cell_size // 3,
                        self.coord[0] * cell_size + 2 * cell_size // 3,
                        self.coord[1] * cell_size + 2 * cell_size // 3),
                       fill=(0, 0, 0),
                       outline=(255, 255, 255))
        save_canvas.save('./img/{}.png'.format(id(self)), quality=quality_img)

        try:
            photo = open('./img/{}.png'.format(id(self)), 'rb')
            await self.bot.edit_message_media(chat_id=self.chat_id, message_id=self.last_message,
                                              media=types.InputMedia(type='photo', media=photo),
                                              reply_markup=get_standard_keyboard())
            '''
            await self.bot.edit_message_media(
                media=types.InputMedia(type='photo', media=open('./img/{}.png'.format(id(self)), 'rb'), caption=''),
                chat_id=self.chat_id,
                message_id=self.last_message,
                reply_markup=get_standard_keyboard())
            '''

        except Exception as e:
            await self.bot.answer_callback_query(call_id)

        os.remove('./img/{}.png'.format(id(self)))

    async def move_left(self):
        if self.coord[0] > 0:
            self.coord[0] -= 1

    async def move_right(self):
        if self.coord[0] < canvas_size - 1:
            self.coord[0] += 1

    async def move_top(self):
        if self.coord[1] > 0:
            self.coord[1] -= 1

    async def move_bottom(self):
        if self.coord[1] < canvas_size - 1:
            self.coord[1] += 1

    def clear_canvas(self):
        self.square_animation = []
        self.coord = [canvas_size // 2, canvas_size // 2]
        self.canvas = Image.new('RGB', (canvas_size * cell_size, canvas_size * cell_size), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.canvas)

    def change_color(self, color):
        self.square_animation.append(copy.copy(self.canvas))
        self.draw.rectangle(
            (self.coord[0] * cell_size, self.coord[1] * cell_size, self.coord[0] * cell_size + cell_size,
             self.coord[1] * cell_size + cell_size),
            fill=color,
            outline=(255, 255, 255))

    async def save(self):
        self.canvas.save('./img/{}.png'.format(id(self)), quality=100)
        await self.bot.send_document(self.chat_id, open('./img/{}.png'.format(id(self)), 'rb'))
        os.remove('./img/{}.png'.format(id(self)))

    async def gif(self):
        self.square_animation.append(copy.copy(self.canvas))
        self.square_animation[0].save(
            './img/{}.gif'.format(id(self)), save_all=True, append_images=self.square_animation[1:]
        )
        await self.bot.send_document(self.chat_id, open('./img/{}.gif'.format(id(self)), 'rb'))
        os.remove('./img/{}.gif'.format(id(self)))
