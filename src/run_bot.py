import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
import asyncio

from database import create_table, get_answers_from_db, save_answer

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_states = {}  # Храним состояние пользователя (какой вопрос задавать)
QUESTIONS = [
    'Ну че там, брат?',
    'Нормально всё?',
    'Ну давай, я погнал',
]


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('Сәлеметсіз бе! Опрос пройди по возможности')
    await message.answer(QUESTIONS[0])
    user_states[message.from_user.id] = 0  # Устанавливаем начальное состояние


@dp.message(Command('get_answers'))
async def get_answers(message: Message):
    await message.answer(get_answers_from_db())


@dp.message(F.text)
async def collect_answer(message: Message):
    user_id = message.from_user.id
    state = user_states.get(user_id, None)

    if state is None:
        await message.answer('Нажмите /start, чтобы начать опрос.')
        return

    save_answer(user_id, QUESTIONS[state], message.text)
    print(f'Ответ сохранен: {message.text}')  # Выводим ответ в консоль

    if state + 1 < len(QUESTIONS):
        user_states[user_id] += 1  # Переходим к следующему вопросу
        await message.answer(QUESTIONS[user_states[user_id]])  # Задаем следующий вопрос
    else:
        await message.answer('Спасибо за ваши ответы!')  # Завершаем опрос
        user_states[user_id] = None


async def main():
    logging.basicConfig(level=logging.INFO)
    create_table()  # Убедимся, что таблица создана
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
