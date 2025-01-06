import os
import requests
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.database.local_database import LOCAL_DATABASE


async def func_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    e_msg = update.effective_message
    prompt = " ".join(context.args)

    if not prompt:
        await Message.reply_message(update, "Use <code>!imagine prompt</code>")
        return
    
    sent_msg = await Message.reply_message(update, "Generating...")

    # temporarily added imagine api
    imagine_api = await LOCAL_DATABASE.get_data("bot_docs", "imagine_api")
    try:
        r = requests.get(f"{imagine_api}{prompt}")
    except Exception as e:
        logger.error(e)
    
    if not r.content:
        await Message.edit_message(update, "Oops, something went wrong...", sent_msg)
        return
    
    os.makedirs("downloads", exist_ok=True)
    file_name = "downloads/tmp_imagine.png"
    
    with open(file_name, "wb") as f:
        f.write(r.content)

    await Message.send_image(chat.id, file_name, reply_message_id=e_msg.id)
    await Message.delete_message(chat.id, sent_msg)

    try:
        os.remove(file_name)
    except Exception as e:
        logger.error(e)
