import logging, qrcode, os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Keyboards.default import qrcode_btn

TOKEN = "7183171518:AAF3U7nVBvjqDCOtXcVIjtP2044oW_UwpmM"

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


class QrCode(StatesGroup):
    text = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(f"Hello {message.from_user.first_name}")
    await message.answer("Send me text for <b>QrCode</b>")
    await QrCode.text.set()

@dp.message_handler(text='Generate QrCode')
async def text(message: types.Message):
    await message.answer("Send me text for <b>QrCode</b>")
    await QrCode.text.set()


@dp.message_handler(state=QrCode.text, content_types=types.ContentTypes.TEXT)
async def text(message: types.Message, state: FSMContext):
    text = str(message.text)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    await message.answer_photo(photo=open("qrcode.png", "rb"), caption="QrCode Img 📸",reply_markup=qrcode_btn)
    os.remove("qrcode.png")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
