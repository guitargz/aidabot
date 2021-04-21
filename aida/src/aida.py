import asyncio
from aiogram import Bot, Dispatcher, executor, types
import redis
import os

MY_CHANNEL = os.environ['MY_CHANNEL'] 

async def start_handler(event: types.Message):
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )

async def get_caption(r, p):
    #Wait for GPT-2 to subscribe
    while r.pubsub_numsub('gpt-2-request')[0][1] < 1:
        print(r.pubsub_numsub('gpt-2-request'))
        await asyncio.sleep(10)

    r.publish('gpt-2-request', 1)
    while True:
        message = p.get_message()
        if message:
            if message['channel']==b'gpt-2-caption':
                return message['data'].decode('utf-8')
        await asyncio.sleep(10)

async def get_photos(r, p):
    #Wait for StyleGAN to subscribe
    while r.pubsub_numsub('stylegan-request')[0][1] < 1:
        print(r.pubsub_numsub('stylegan-request'))
        await asyncio.sleep(10)

    r.publish('stylegan-request', 1)
    while True:
        message = p.get_message()
        if message:
            if message['channel']==b'stylegan-photos':
                return message['data']
        await asyncio.sleep(10)

async def main():
    print(MY_CHANNEL)
    #read password
    pass_file = "/run/secrets/bot_token"
    password_file = open(pass_file, 'rb')
    password = password_file.readline().decode('utf-8')
    password_file.close()

    #Subscribe to the Redis queue
    r = redis.Redis(host='redis', port=6379, db=0)
    p_photos = r.pubsub(ignore_subscribe_messages=True)
    p_photos.subscribe('stylegan-photos')
    p_caption = r.pubsub(ignore_subscribe_messages=True)
    p_caption.subscribe('gpt-2-caption')

    while True:
        bot = Bot(token=password)
        #dp = Dispatcher(bot)
     
        #Get content from the Redis queue
        photos, caption = await asyncio.gather(
            get_photos(r, p_photos),
            get_caption(r, p_caption)
        )

        #Post to Telegram
        try:
            #disp = Dispatcher(bot=bot)
            #disp.register_message_handler(start_handler, commands={"start", "restart"})
            await bot.send_photo(MY_CHANNEL, photos, caption)
            #await disp.start_polling()
        finally:
            await bot.close()
        #wait
        await asyncio.sleep(21600)

if __name__ == "__main__":
    asyncio.run(main())