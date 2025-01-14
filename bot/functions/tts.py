import os
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.gtts import tts

async def func_tts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    lang_code = " ".join(context.args) or "en"
    re_msg = update.message.reply_to_message

    if not re_msg:
        await Message.reply_message(update, "Reply any text to convert it into a voice message! E.g. Reply any message with <code>!tts en</code> to get english accent voice.")
        return
    
    sent_msg = await Message.reply_message(update, "Processing...")
    response = await tts(re_msg.text, lang_code)

    if not response:
        await Message.edit_message(update, "Oops, something went wrong...", sent_msg)
        return
    
    await Message.send_audio(chat.id, response, f"Voice {re_msg.id} [ {lang_code} ].mp3", reply_message_id=re_msg.id)
    await Message.delete_message(chat.id, sent_msg)

    # Removing the audio file
    try:
        os.remove(response)
    except Exception as e:
        logger.error(e)