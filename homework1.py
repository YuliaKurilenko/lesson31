from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text='Calories')
async def set_age(message):
    print('Введите свой возраст:')
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    print('Введите свой рост:')
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    print('Введите свой вес:')
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    print('Норма каллорий:')
    await state.update_data(weight=message.text)
    date = await state.get_data()
    result = 10 * int(date['weight']) + 6.25 * int(date['growth']) + 4.92 * int(date['age']) - 161
    await message.answer(f"Ваша норма каллорий:{result}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
