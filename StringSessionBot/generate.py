from data import Data
from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from pyrogram1 import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)


ask_ques = "Pʟᴇᴀsᴇ Cʜᴏᴏsᴇ Tʜᴇ Pʏᴛʜᴏɴ Lɪʙʀᴀʀʏ Yᴏᴜ Wᴀɴᴛ Tᴏ Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ Fᴏʀ:"
buttons_ques = [
    [
        InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ", callback_data="pyrogram1"),
        InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ ᴠ2 [New]", callback_data="pyrogram"),
    ],
    [
        InlineKeyboardButton("Pʏʀᴏɢʀᴀᴍ Bᴏᴛ", callback_data="pyrogram_bot"),
        InlineKeyboardButton("Tᴇʟᴇᴛʜᴏɴ Bᴏᴛ", callback_data="telethon_bot"),
    ],
]


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = "Telethon"
    else:
        ty = "Pyrogram"
        if not old_pyro:
            ty += " v2"
    if is_bot:
        ty += " Bot"
    await msg.reply(f"Sᴛᴀʀᴛɪɴɢ {ty} Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛɪᴏɴ...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, 'Pʟᴇᴀsᴇ Sᴇɴᴅ Yᴏᴜʀ `API_ID`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('Nᴏᴛ A Vᴀʟɪᴅ API_ID (ᴡʜɪᴄʜ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ).Pʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Sᴇssɪᴏɴ Aɢᴀɪɴ .', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'Pʟᴇᴀsᴇ Sᴇɴᴅ Yᴏᴜʀ `API_HASH`', filters=filters.text)
    if await cancelled(api_hash_msg):
        return
    api_hash = api_hash_msg.text
    if not is_bot:
        t = "Nᴏᴡ Pʟᴇᴀsᴇ Sᴇɴᴅ Yᴏᴜʀ `PHONE_NUMBER` Aʟᴏɴɢ Wɪᴛʜ Tʜᴇ Cᴏᴜɴᴛʀʏ Cᴏᴅᴇ. \nExᴀᴍᴘʟᴇ : `+19876543210`'"
    else:
        t = "Nᴏᴡ Pʟᴇᴀsᴇ Sᴇɴᴅ Yᴏᴜʀ `BOT_TOKEN` \nExᴀᴍᴘʟᴇ : `12345:abcdefghijklmnopqrstuvwxyz`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("sᴇɴᴅɪɴɢ - ᴏᴛᴘ...")
    else:
        await msg.reply("Lᴏɢɢɪɴɢ As Bᴏᴛ Usᴇʀ...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply('`API_ID` Aɴᴅ `API_HASH` Cᴏᴍʙɪɴᴀᴛɪᴏɴ Is Iɴᴠᴀʟɪᴅ. Pʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Sᴇssɪᴏɴ Aɢᴀɪɴ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        await msg.reply('`PHONE_NUMBER` Is Iɴᴠᴀʟɪᴅ. Pʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Sᴇssɪᴏɴ Aɢᴀɪɴ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "Please check for an OTP in official telegram account. If you got it, send OTP here after reading the below format. \nIf OTP is `12345`, **please send it as** `1 2 3 4 5`.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply('Tɪᴍᴇ Lɪᴍɪᴛ Rᴇᴀᴄʜᴇᴅ Oғ 10 Mɪɴᴜᴛᴇs. Pʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Sᴇssɪᴏɴ Aɢᴀɪɴ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply('OTP Is Iɴᴠᴀʟɪᴅ. Pʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Sᴇssɪᴏɴ Aɢᴀɪɴ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply('OTP Is Exᴘɪʀᴇᴅ. Pʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Sᴇssɪᴏɴ Aɢᴀɪɴ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
            try:
                two_step_msg = await bot.ask(user_id, 'Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Hᴀs Eɴᴀʙʟᴇᴅ Tᴡᴏ-Sᴛᴇᴘ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ. Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ Tʜᴇ Pᴀssᴡᴏʀᴅ.', filters=filters.text, timeout=300)
            except TimeoutError: 
                await msg.reply('Tɪᴍᴇ Lɪᴍɪᴛ Rᴇᴀᴄʜᴇᴅ Oғ 5 Mɪɴᴜᴛᴇs. Pʟᴇᴀsᴇ Aᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Sᴇssɪᴏɴ Aɢᴀɪɴ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
                await two_step_msg.reply('Iɴᴠᴀʟɪᴅ Pᴀssᴡᴏʀᴅ Pʀᴏᴠɪᴅᴇᴅ. Pʟᴇᴀsᴇ Sᴛᴀʀᴛ Gᴇɴᴇʀᴀᴛɪɴɢ Sᴇssɪᴏɴ Aɢᴀɪɴ.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**{ty.upper()} *Sᴛʀɪɴɢ Sᴇssɪᴏɴ * \n\n`{string_session}` \n\nGᴇɴᴇʀᴀᴛᴇᴅ Bʏ @Stringmaker_bot"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "Sᴜᴄᴄᴇssғᴜʟʟʏ Gᴇɴᴇʀᴀᴛᴇᴅ {} Sᴛʀɪɴɢ Sᴇssɪᴏɴ. \n\nPʟᴇᴀsᴇ Cʜᴇᴄᴋ Yᴏᴜʀ Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs! \n\nBʏ @EDWARD_CHATS".format("telethon" if telethon else "pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("Cᴀɴᴄᴇʟʟᴇᴅ Tʜᴇ Pʀᴏᴄᴇss!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("Rᴇsᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("Cᴀɴᴄᴇʟʟᴇᴅ Tʜᴇ Gᴇɴᴇʀᴀᴛɪᴏɴ Pʀᴏᴄᴇss!", quote=True)
        return True
    else:
        return False
