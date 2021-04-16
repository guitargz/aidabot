import asyncio
from aiogram import Bot, Dispatcher, executor, types

MY_CHANNEL = '@aida_enelpi' 

async def start_handler(event: types.Message):
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )

async def main():
    bot = Bot(token="1722872904:AAGqv6VDMDbPj_XZX3_UJ7i8fqjMHrAgj8k")
    dp = Dispatcher(bot)
    await asyncio.sleep(200)
    while True:
        #open styleGAN
        photo = "results/Demo_today.png"
        photos = open(photo, 'rb')
        #open GPT-2
        caption_file = "results/Demo_today.txt"
        captions_file = open(caption_file, 'rb')
        caption = captions_file.readline().decode('utf-8')
        captions_file.close()
        #post to TG
        try:
            #disp = Dispatcher(bot=bot)
            #disp.register_message_handler(start_handler, commands={"start", "restart"})
            #await bot.send_message(MY_CHANNEL, caption)
            await bot.send_photo(MY_CHANNEL, photos, caption)
            #await disp.start_polling()
        finally:
            await bot.close()
        #wait
        await asyncio.sleep(21600)

if __name__ == "__main__":
    asyncio.run(main())