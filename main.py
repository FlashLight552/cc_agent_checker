import logging
import asyncio
import requests
import time

from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor


API_TOKEN = 'BOT TOKEN HERE'
chat_id = 'YOUR_CHAT_ID'
url = 'https://example.com/admins_all'
message_text = 'Работать негры!'


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def get_admins_all():
    # Виконуємо запит до сторінки та отримуємо її HTML-код
    response = requests.get(url)
    html = response.text

    # Розбираємо HTML-код з використанням бібліотеки BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    # Знаходимо всіх агентів в розділі Admins All
    agents_all = soup.select('div.agent')

    return agents_all


async def check_queue():
    counter = 0
    while True:
        agents_all = get_admins_all()
        current_hour = time.localtime().tm_hour
        if 10 <= current_hour < 18 and len(agents_all) < 3:
            counter += 1
            asyncio.sleep(60)
        if counter == 5:
            await bot.send_message(chat_id=chat_id, text=message_text)    
            counter = 0  


async def on_startup(_):
    asyncio.create_task(check_queue())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)