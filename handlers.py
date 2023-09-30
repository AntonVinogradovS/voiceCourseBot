from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery, MediaGroup, InputMediaDocument
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from texts import welcomeMessage, programMessage, programMessage2, finishMessage
from keyboards import inlineKbOne, mainKeyboard, adminKeyboard, f, priceKeyboard, fromTheCourse
from database import sql_write_sing, sql_read_sing, sql_write_pay, sql_read_pay, sql_delete_pay

async def cmdStart(message: types.Message):
    await message.answer(text=welcomeMessage, reply_markup=inlineKbOne)

async def programCourse(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text=programMessage, reply_markup=mainKeyboard)
    await bot.send_message(chat_id=callback_query.from_user.id, text=programMessage2,parse_mode=types.ParseMode.HTML, reply_markup=fromTheCourse)

async def fromCourse(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text=finishMessage)


class FSMUser(StatesGroup):
    q1 = State()
    q2 = State()

async def singUp(message: types.Message, state: FSMContext):
    numberPhone = message.contact.phone_number
    await FSMUser.q1.set()
    async with state.proxy() as data:
        data['q0'] = numberPhone
    await message.answer(text = "Укажите фамилию и имя")

async def FSname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['q1'] = message.text
    await FSMUser.next()
    await message.answer(text = "Укажите почту")

async def email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['q2'] = message.text
    await state.finish()
    await sql_write_sing(message.from_user.id, list(data.values()))
    print(message.from_user.id)
    await bot.send_chat_action(chat_id=message.from_user.id, action=types.ChatActions.UPLOAD_DOCUMENT)
    with open('checklist.pdf', 'rb') as pdf_file:
        # Отправьте PDF-файл пользователю
        await bot.send_document(message.chat.id, pdf_file)
    #await message.answer(text=finishMessage, reply_markup=mainKeyboard)


class FSMPay(StatesGroup):
    s1 = State()
    s2 = State()


async def payCheck(message: types.Message):
    await message.answer("Цена курса на месяц - 25000 рублей\nПолная стоимость курса - 47000 рублей.\nРеквизиты для оплаты: 5469380089601016")
    await message.answer("Выберите интересующий вас тариф.",reply_markup=priceKeyboard)
    await FSMPay.s1.set()

async def finishPay1(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['s1'] = callback_query.data
    await FSMPay.next()
    await bot.send_message(chat_id=callback_query.from_user.id, text='Отлично! Прикрепите скриншот оплаты. После подтверждения менеджером, вам придет ссылка на курс.')

async def finishPay2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['s2'] = message.photo[0].file_id
    await state.finish()
    await sql_write_pay(message.from_user.id, message.from_user.username, list(data.values()))
    await message.answer('Ожидайте подтверждения.')

ADMIN = [1313463136, 609250699, 891018303]
async def adminInput(message: types.Message):
    if message.from_user.id in ADMIN:
        await message.answer("Вы администратор бота", reply_markup=adminKeyboard)

async def adminCheckSingUp(message: types.Message):
    res = await sql_read_sing()
    for i in res:
        phone, name, email = i[1].split('\n')
        await message.answer(f'Имя: {name}\nНомер: {phone}\nПочта: {email}')


async def adminCheckPay(message: types.Message):
    res = await sql_read_pay()
    for i in res:
        await bot.send_photo(chat_id=message.from_user.id, photo=i[2], caption="@"+i[1]+'\n'+i[-1]+' рублей', reply_markup=f(i[0]))

async def payGood(callback_query: types.CallbackQuery):
    tmp = callback_query.data.replace('proof ', '')

    chat_url = 'https://t.me/+m4GrN22jF-k4Mzgy'  # Здесь укажите ID вашего закрытого чата
    user_id_to_add = tmp
    await bot.send_message(user_id_to_add, f'Оплата подтверждена! \nЧтобы добавиться в чат курса, вступите в наш закрытый чат\n{chat_url}')
    await sql_delete_pay(user_id_to_add)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)



def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmdStart, commands=['start'])
    dp.register_callback_query_handler(programCourse, lambda c: c.data == "program")
    dp.register_callback_query_handler(fromCourse, lambda c: c.data == "from")
    #dp.register_message_handler(course, text = 'О курсе')
    dp.register_message_handler(singUp, content_types=types.ContentType.CONTACT)
    dp.register_callback_query_handler(finishPay1, state=FSMPay.s1)
    dp.register_message_handler(finishPay2, content_types=['photo'], state=FSMPay.s2)

    dp.register_message_handler(FSname, state=FSMUser.q1)
    dp.register_message_handler(email, state=FSMUser.q2)
    dp.register_message_handler(adminInput, commands=['admin'])
    dp.register_message_handler(adminCheckSingUp, text = 'Запись')
    dp.register_message_handler(adminCheckPay, text = 'Оплата')
    dp.register_message_handler(payCheck, text = 'Оплатить')
    dp.register_callback_query_handler(payGood, lambda x: x.data and x.data.startswith('proof '))
    #dp.register_message_handler(finishPay, content_types=types.ContentType.PHOTO)
    
