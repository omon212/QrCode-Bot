from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

qrcode_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Generate QrCode")
        ]
    ]
)