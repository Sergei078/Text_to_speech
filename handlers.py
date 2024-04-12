from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
import os
from FSM import FSMFillForm
from speechkit import text_to_speech
from button import menu_kb
from database import tokens_add, tokens_user, Database, message_add
import logging

load_dotenv()

logging.basicConfig(filename=os.getenv('file_error'), level=logging.ERROR, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

router = Router()


@router.message(Command('log'))
async def logging_info(message: Message):
    file = FSInputFile(os.getenv('file_error'))
    await message.answer_document(file)


@router.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=menu_kb, resize_keyboard=True)
    db_user = Database()
    try:
        if not await db_user.check_user_exists(message.chat.id):
            await db_user.add_user(message.chat.id)
        await message.answer(f'<b>Привет, {message.chat.first_name}👋\n\n</b>'
                             '<i>🗣Я могу озвучить текст\n'
                             'который ты мне напишешь.\n\n</i>',
                             parse_mode='html', reply_markup=keyboard)
    except Exception as e:
        logging.error(str(e))


@router.message(F.text == 'Озвучить текст🗣')
async def text_input(message: Message, state: FSMContext):
    await state.set_state(FSMFillForm.fill_text)
    await message.answer('Введи свой текст:', reply_markup=ReplyKeyboardRemove())


@router.message(FSMFillForm.fill_text)
async def generating_voice_messages(message: Message, state: FSMContext):
    try:
        await state.update_data(text=message.text)
        data = await state.get_data()
        tekens_control = len((data['text']))
        keyboard = ReplyKeyboardMarkup(keyboard=menu_kb, resize_keyboard=True)
        user_id = message.chat.id
        if tekens_control <= 150:
            info_db_tokens = tokens_user()
            tokens_db = await info_db_tokens.tts_symbols_user(user_id)
            await info_db_tokens.close()
            if tokens_db is None or tokens_db > 0:
                save_text = message_add()
                await save_text.add_text(data['text'], user_id)
                await save_text.close()
                info_db_tokens1 = tokens_user()
                tokens_db1 = await info_db_tokens1.tts_symbols_user(user_id)
                result = tokens_db1 - tekens_control
                await info_db_tokens1.close()
                save_tokens = tokens_add()
                await save_tokens.add_tts_symbols(result, user_id)
                await save_tokens.close()
                await message.answer(f'Ожидай ответа⏳')
                await text_to_speech(data['text'])
                audio = FSInputFile(os.getenv('file'))
                await message.answer_voice(audio, reply_markup=keyboard)
            else:
                await message.answer('<i>Символы закончились❗️</i>', parse_mode='html', reply_markup=keyboard)
        else:
            await message.answer('<i>Вы превисили допускаемое\n'
                                 'значение❗️</i>', parse_mode='html', reply_markup=keyboard)
        await state.clear()
    except Exception as e:
        logging.error(str(e))
        await state.clear()


@router.message(F.text == 'Баланс💳')
async def balance(message: Message):
    try:
        user_id = message.chat.id
        info_db_tokens = tokens_user()
        tokens_db = await info_db_tokens.tts_symbols_user(user_id)
        await info_db_tokens.close()
        if tokens_db is None:
            tokens_db = 0
        await message.answer(f'<b>Количестов символов:</b> {tokens_db}', parse_mode='html')
    except Exception as e:
        logging.error(str(e))
