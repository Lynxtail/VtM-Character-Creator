from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu = [
    [InlineKeyboardButton(text='Мои персонажи', callback_data='list_of_chars'),
     InlineKeyboardButton(text='Новый персонаж', callback_data='new_char')],
    # [InlineKeyboardButton(text='Экспорт персонажей', callback_data='export_chars'),
    #  InlineKeyboardButton(text='Импорт персонажа', callback_data='import_char')]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='В меню')]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='menu')]])

# def next(step:int):
#     return InlineKeyboardMarkup(inline_keyboard=InlineKeyboardButton(text='Далее', callback_data=f'{step}'))

# next_step = InlineKeyboardMarkup(inline_keyboard=InlineKeyboardButton(text='Далее', callback_data='next'))
next_step = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Мои персонажи', callback_data='list_of_chars')]])
# done = InlineKeyboardMarkup(inline_keyboard=InlineKeyboardButton(text='Завершить', callback_data='done'))

# для динамических клавиатур
def list_of_chars(characters: dict):
    builder = InlineKeyboardBuilder()
    for i, item in enumerate(characters):
        builder.button(text=f'{item.name}', callback_data=f"char_{i}")
    builder.adjust(2)
    return builder.as_markup()

def creation_steps():
    builder = InlineKeyboardBuilder()
    for i in range(4):
        builder.button(text=f'{i}', callback_data=f"step_{i}")
    return builder.as_markup()
