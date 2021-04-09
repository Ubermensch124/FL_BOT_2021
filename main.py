import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from selenium_work import check_new, get_screen
from Check_new import get_new


API_TOKEN = '1756814334:AAFzsJsWwEdrZ4oYYH0Y8hO8uwg6P69dx_8'


class Information(object):
    CONSTANT_LIST = check_new()
    CONSTANT_CATEGORY_ME = []
    C = []


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    add = State()
    delete = State()


class konst(object):
    async def cn(self, url, id):
        last = ''
        print(url)
        while True:
            news = get_new(url)
            if news.split('\n')[0] == last:
                await asyncio.sleep(60)
                continue
            else:
                last = news.split('\n')[0]
                await bot.send_message(
                    id,
                    md.text(
                        news
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
                await asyncio.sleep(60)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    # добавляем айдишник человека в БД
    await message.answer("Привет, используй функцию /add, чтобы добавить отслеживаемую категорию\n/cancel, "
                         "чтобы отменить отслеживание")


@dp.message_handler(commands='add')
async def choose(message: types.Message):
    await Form.add.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for i in Information.CONSTANT_LIST:
        markup.add(i)

    await message.answer("Какую категорию предпочитаете?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in Information.CONSTANT_LIST, state=Form.add)
async def choose_false(message: types.Message):
    return await message.answer("Пожалуйста, выберите вариант из выпадающей клавиатуры")


@dp.message_handler(state=Form.add)
async def choose_ok(message: types.Message, state: FSMContext):
    await state.update_data(add=message.text)
    markup = types.ReplyKeyboardRemove()

    USER_INFO = await state.get_data()

    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Теперь ты отслеживаешь: ', md.bold(USER_INFO['add']))
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )
    number_for_url = str(Information.CONSTANT_LIST.get(USER_INFO['add']))
    url = f'https://www.fl.ru/rss/all.xml?category={number_for_url}'

    c = konst()
    Information.CONSTANT_CATEGORY_ME.append((c, USER_INFO['add']))
    Information.C.append(USER_INFO['add'])
    print(Information.CONSTANT_CATEGORY_ME)
    await state.finish()
    await c.cn(url, message.chat.id)


@dp.message_handler(commands='info')
async def info(message: types.Message):
    if len(Information.CONSTANT_CATEGORY_ME) > 0:
        string = ', '.join([i[1] for i in Information.CONSTANT_CATEGORY_ME])
        await message.answer(f'Вы отслеживаете следующие категории: {string}')
    else:
        await message.answer(f'Вы отслеживаете следующие категории: категории отсутсвуют')


@dp.message_handler(commands='delete')
async def delete(message: types.Message):
    if len(Information.CONSTANT_CATEGORY_ME) <= 0:
        await message.answer('Вы пока не отслеживаете ни одну категорию')
    else:
        await Form.delete.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        for i in Information.CONSTANT_CATEGORY_ME:
            markup.add(i[1])

        await message.answer("Какую категорию хотите удалить?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in Information.C, state=Form.delete)
async def choose_false(message: types.Message):
    return await message.answer("Пожалуйста, выберите вариант из выпадающей клавиатуры")


@dp.message_handler(state=Form.delete)
async def choose_ok(message: types.Message, state: FSMContext):
    await state.update_data(delete=message.text)
    markup = types.ReplyKeyboardRemove()

    USER_INFO = await state.get_data()

    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Теперь ты не отслеживаешь: ', md.bold(USER_INFO['delete']))
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )

    Information.CONSTANT_CATEGORY_ME.pop([i[1] for i in Information.CONSTANT_CATEGORY_ME].index(USER_INFO['delete']))
    Information.C.pop(Information.C.index(USER_INFO['delete']))

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
