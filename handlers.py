from aiogram import types, F, Router, flags
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.callback_answer import CallbackAnswer

import keyboard
import text
import utils
from character import Character

class CreationOrder(StatesGroup):
    name = State()
    clan = State()
    attributes = State()
    skills = State()
    finish = State()


# страницы при просмотре персонажей
        # class ShowCharactersOrder(StatesGroup):
        #     page_1 = State()
        #     __pages = set(page_1)

        #     def new_page(self):
        #         page = State()
        #         self.__pages.add(page)


router = Router()
user_data = dict()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.first_name), reply_markup=keyboard.menu)

@router.message(F.text == 'Меню')
@router.message(F.text == 'Выйти в меню')
@router.callback_query(F.data == 'break') # отмена создания
async def message_handler(msg, state:FSMContext):
    if isinstance(msg, Message):
        await msg.answer(text.menu, reply_markup=keyboard.menu)
    else:
        await msg.message.answer(text.menu, reply_markup=keyboard.menu)
        await msg.answer()
    await state.clear()
    

# показать список персонажей
@router.callback_query(F.data == 'list_of_chars')
async def get_chars(callback: CallbackQuery):
    try:
        await callback.message.answer(text.chars, reply_markup=keyboard.list_of_chars(user_data.get(callback.from_user.id, None)))
    except TypeError:
        await callback.message.answer(text.no_chars)
        await callback.message.answer(text.menu, reply_markup=keyboard.menu)
    await callback.answer()

# вывод списка в виде кнопок
@router.callback_query(F.data.startwith('char_'))
async def show_character(callback: CallbackQuery):
    characters = user_data.get(callback.from_user.id, None)
    char_id = callback.data.split('_')[1]
    character = characters.get(char_id)
    if character:
        await callback.message.answer(character.get_info())
    await callback.answer()

# как это примерно будет выглядеть:
# разные стейты -- это разные этапы создания персонажа
# каждый этап предполагает диалоговое взаимодействие
# с постепенным заполнением "чарника".
# затем происходит сохранение чарника в словарь
# (в будущем в json).
# словарь выдаёт по ключу-id пользователя
# значение -- вложенную коллекцию из персонажей,
# созданных этим пользователем.

# создание нового персонажа
@router.callback_query(F.data == 'new_char')
async def create_char(callback: CallbackQuery, state:FSMContext):
    # приветствие и переход на 1 шаг
    await callback.message.answer(text.creation_welcome, reply_markup=keyboard.welcome_creation)
    if callback.from_user.id in user_data.keys():
        user_data[callback.from_user.id].append(Character())
    else:
        user_data[callback.from_user.id] = [Character()]
    await state.set_state(CreationOrder.name)
    await callback.answer()

# назад
@router.callback_query(F.data == 'back')
async def back_handler(callback: CallbackQuery, state:FSMContext):
    if await state.get_state() == CreationOrder.name:
        await state.clear()
        await create_char(callback, state)
    if await state.get_state() == CreationOrder.clan:
        await state.set_state(CreationOrder.name)
        await choose_name(callback)
    if await state.get_state() == CreationOrder.attributes:
        await state.set_state(CreationOrder.clan)
        await choose_clan(callback)
    if await state.get_state() == CreationOrder.skills:
        await state.set_state(CreationOrder.attributes)
        await select_attributes(callback)
    if await state.get_state() == CreationOrder.finish:
        await state.set_state(CreationOrder.skills)
        await select_skills(callback)
    await callback.answer()

# запрос имени
@router.callback_query(CreationOrder.name, F.data == 'next')
async def choose_name(callback: CallbackQuery):
    await callback.message.answer(text.personal_info_name)
    await callback.answer()

# считывание имени
@router.message(CreationOrder.name, F.text)
async def message_handler(msg: Message, state: FSMContext):
    user_data[msg.from_user.id][-1].name = msg.text.title()
    # await msg.answer(text.thanks, reply_markup=keyboard.next_step_creation)
    char_info = user_data[msg.from_user.id][-1].get_info()
    await msg.answer(char_info + '\n\n', reply_markup=ReplyKeyboardRemove())
    await msg.answer(text.thanks, reply_markup=keyboard.next_step_creation)
    await state.set_state(CreationOrder.clan)
    

# запрос клана
@router.callback_query(CreationOrder.clan, F.data == 'next')
async def choose_clan(callback: CallbackQuery):
    await callback.message.answer(text.personal_info_clan, reply_markup=keyboard.list_of_clans())
    await callback.answer()

# считывание клана
@router.message(CreationOrder.clan, F.text)
async def message_handler(msg: Message, state: FSMContext):
    user_data[msg.from_user.id][-1].clan = msg.text.title()
    char_info = user_data[msg.from_user.id][-1].get_info()
    await msg.answer(char_info + '\n\n', reply_markup=ReplyKeyboardRemove())
    await msg.answer(text.thanks, reply_markup=keyboard.next_step_creation)
    await state.set_state(CreationOrder.attributes)

# запрос атрибутов
@router.callback_query(CreationOrder.attributes, F.data == 'next')
async def select_attributes(callback: CallbackQuery):
    await callback.message.answer(text.mechanical_info_attributes)
    await callback.message.answer(user_data[callback.from_user.id][-1].get_info(), reply_markup=keyboard.select_attributes())
    await callback.answer()

# считывание атрибутов
@router.callback_query(F.data.startswith('attr_'))
async def pick_values(callback: CallbackQuery, callback_answer: CallbackAnswer, state: FSMContext):
    attribute = callback.data.split('_')[1]
    if user_data[callback.from_user.id][-1].attributes[attribute] <= 5:
        user_data[callback.from_user.id][-1].attributes[attribute] += 1
    else:
        callback_answer.cache_time = 10
        await callback.answer(text='Достигнуто максимальное значение атрибута!')
    if sum(user_data[callback.from_user.id][-1].attributes.values) == 22:
        await callback.message.edit_text(user_data[callback.from_user.id][-1].get_info() + text.thanks, reply_markup=keyboard.next_step_creation)
        await state.set_state(CreationOrder.skills)
    else:
        await callback.message.edit_text(user_data[callback.from_user.id][-1].get_info(), reply_markup=keyboard.select_attributes())
    await callback.answer()

# @router.message(CreationOrder.attributes, F.text)
# async def message_handler(msg: Message, state: FSMContext):
#     user_data[msg.from_user.id][-1].attributes = {attribute : value 
#                                                   for (attribute, value) in zip(
#                                                       ('сила', 'харизма', 'интеллект',
#                                                        'ловкость', "манипулирование", "смекалка",
#                                                        "выносливость", "самообладание", "решительность"),
#                                                       (map(int, msg.text.split())))}
#     char_info = user_data[msg.from_user.id][-1].get_info()
#     await msg.answer(char_info + '\n\n', reply_markup=ReplyKeyboardRemove())
#     await msg.answer(text.thanks, reply_markup=keyboard.next_step_creation)
#     await state.set_state(CreationOrder.skills)

# запрос навыков
@router.callback_query(CreationOrder.skills, F.data == 'next')
async def select_skills(callback: CallbackQuery):
    await callback.message.answer(text.mechanical_info_skills)
    await callback.message.answer(user_data[callback.from_user.id][-1].get_info(), reply_markup=keyboard.select_skills())
    await callback.answer()

# считывание навыков
@router.callback_query(F.data.startswith('skill_'))
async def pick_values(callback: CallbackQuery, callback_answer: CallbackAnswer, state: FSMContext):
    skill = callback.data.split('_')[1]
    if user_data[callback.from_user.id][-1].skills[skill] <= 4:
        user_data[callback.from_user.id][-1].skills[skill] += 1
    else:
        callback_answer.cache_time = 10
        await callback.answer(text='Достигнуто максимальное значение атрибута!')
    if sum(user_data[callback.from_user.id][-1].skills.values) == 22:
        await callback.message.edit_text(user_data[callback.from_user.id][-1].get_info() + text.thanks, reply_markup=keyboard.next_step_creation)
        await state.set_state(CreationOrder.skills)
    else:
        await callback.message.edit_text(user_data[callback.from_user.id][-1].get_info(), reply_markup=keyboard.select_skills())
    await callback.answer()    

# конец создания
@router.callback_query(CreationOrder.finish, F.data == 'done')
async def message_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(user_data[callback.from_user.id][-1].get_info(), reply_markup=keyboard.ReplyKeyboardRemove())
    await state.clear()



# @router.callback_query(F.data == 'export_chars')
# @router.callback_query(F.data == 'import_char')
