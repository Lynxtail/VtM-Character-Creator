from aiogram import types, F, Router, flags
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

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


router = Router()
user_data = dict()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.first_name), reply_markup=keyboard.menu)

@router.message(F.text == 'Меню')
@router.message(F.text == 'Выйти в меню')
async def message_handler(msg: Message):
    await msg.answer(text.menu, reply_markup=keyboard.menu)

@router.callback_query(F.data == 'list_of_chars')
async def get_chars(callback: CallbackQuery):
    # await state.set_state()
    await callback.message.answer(text.chars, reply_markup=keyboard.list_of_chars(user_data.get(callback.from_user.id, None)))
    await callback.answer()

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

@router.callback_query(F.data == 'new_char')
async def create_char(callback: CallbackQuery, state:FSMContext):
    # приветствие и переход на 1 шаг
    await callback.message.answer(text.creation_welcome, reply_markup=keyboard.next_step)
    if callback.from_user.id in user_data.keys():
        user_data[callback.from_user.id].append(Character())
    else:
        user_data[callback.from_user.id] = [Character()]
    await state.set_state(CreationOrder.name)
    await callback.answer()

# запрос имени
@router.callback_query(CreationOrder.name, F.data == 'next')
async def message_handler(callback: CallbackQuery):
    await callback.message.answer(text.personal_info_name)

# считывание имени
@router.message(CreationOrder.name, F.text)
async def message_handler(msg: Message, state: FSMContext):
    user_data[msg.from_user.id][-1].name = msg.text.title()
    await msg.answer(text.thanks, reply_markup=keyboard.next_step)
    await state.set_state(CreationOrder.clan)

# запрос клана
@router.callback_query(CreationOrder.clan, F.data == 'next')
async def message_handler(callback: CallbackQuery):
    await callback.message.answer(text.personal_info_clan)

# считывание клана
@router.message(CreationOrder.clan, F.text)
async def message_handler(msg: Message, state: FSMContext):
    user_data[msg.from_user.id][-1].clan = msg.text.title()
    await msg.answer(text.thanks, reply_markup=keyboard.next_step)
    await state.set_state(CreationOrder.attributes)

# запрос атрибутов
@router.callback_query(CreationOrder.attributes, F.data == 'next')
async def message_handler(callback: CallbackQuery):
    await callback.message.answer(text.mechanical_info_attributes)

# для атрибутов и навыков ниже
# нужно реализовать мини-викторину
# с инлайн-кнопками, повышающие
# нужные значения
# считывание атрибутов
@router.message(CreationOrder.attributes, F.text)
async def message_handler(msg: Message, state: FSMContext):
    user_data[msg.from_user.id][-1].attributes = msg.text
    await msg.answer(text.thanks, reply_markup=keyboard.next_step)
    await state.set_state(CreationOrder.skills)

# запрос навыков
@router.callback_query(CreationOrder.skills, F.data == 'next')
async def message_handler(callback: CallbackQuery):
    await callback.message.answer(text.mechanical_info_skills)

# считывание навыков
@router.message(CreationOrder.skills, F.text)
async def message_handler(msg: Message, state: FSMContext):
    user_data[msg.from_user.id][-1].skills = msg.text
    await msg.answer(text.thanks, reply_markup=keyboard.done)
    await state.set_state(CreationOrder.finish)

@router.callback_query(CreationOrder.finish, F.data == 'done')
async def message_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(user_data[callback.from_user.id][-1].get_info(), reply_markup=keyboard.ReplyKeyboardRemove())
    await state.clear()



# @router.callback_query(F.data == 'export_chars')
# @router.callback_query(F.data == 'import_char')
