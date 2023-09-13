from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

menu = [
    [InlineKeyboardButton(text='Мои персонажи', callback_data='list_of_chars'),
     InlineKeyboardButton(text='Новый персонаж', callback_data='new_char')],
    # [InlineKeyboardButton(text='Экспорт персонажей', callback_data='export_chars'),
    #  InlineKeyboardButton(text='Импорт персонажа', callback_data='import_char')]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='В меню')]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='menu')]])

previous_step = InlineKeyboardButton(text='Назад', callback_data='back')
next_step = InlineKeyboardButton(text='Далее', callback_data='next')
done = InlineKeyboardButton(text='Завершить', callback_data='done')
break_creation = InlineKeyboardButton(text='Главное меню', callback_data='break')

welcome_creation = InlineKeyboardMarkup(inline_keyboard=[[previous_step, next_step]])
next_step_creation = InlineKeyboardMarkup(inline_keyboard=[[previous_step, next_step], [break_creation]])
done_creation = InlineKeyboardMarkup(inline_keyboard=[[previous_step, done], [break_creation]])


# для динамических клавиатур
def list_of_chars(characters: dict):
    builder = InlineKeyboardBuilder()
    for i, item in enumerate(characters):
        builder.button(text=f'{item.name}', callback_data=f"char_{i}")
    builder.adjust(2)
    return builder.as_markup()

def list_of_clans():
    clans = ("Бруха", "Гангрел", "Малкавиан", "Тореадор", 
            "Носферату", "Вентру", "Тремер", "Цимисх",
            "Ласомбра", "Равнос", "Бану Хаким", "Каитифф",
            "Слабая Кровь", "Салюбри", "Министри")
    builder = ReplyKeyboardBuilder()
    for item in clans:
        builder.button(text=item)
    builder.adjust(4)
    return builder.as_markup(one_time_keyboard=True)

def creation_steps():
    builder = InlineKeyboardBuilder()
    for i in range(4):
        builder.button(text=f'{i}', callback_data=f"step_{i}")
    return builder.as_markup()
