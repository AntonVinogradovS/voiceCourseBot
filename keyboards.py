from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

inlineKbOne = InlineKeyboardMarkup().add(InlineKeyboardButton(text = 'Посмотреть программу курса', callback_data="program"))
mainKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text= 'Записаться', request_contact=True)).add(KeyboardButton(text= 'Оплатить'))
adminKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text= 'Запись')).add(KeyboardButton(text= 'Оплата'))
def f(id):
    confirmationKeyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text = 'Подтвердить оплату', callback_data=f'proof {id}'))
    return confirmationKeyboard

# def f2(id):
#     priceKeyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text = '25000 рублей', callback_data=f'25 {id}')).add(InlineKeyboardButton(text = '47000 рублей', callback_data=f'47 {id}'))
#     return priceKeyboard
priceKeyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text = '25000 рублей', callback_data=f'25000')).add(InlineKeyboardButton(text = '47000 рублей', callback_data=f'47000'))
fromTheCourse = InlineKeyboardMarkup().add(InlineKeyboardButton(text = 'Кому полезен  курс?', callback_data=f'from'))