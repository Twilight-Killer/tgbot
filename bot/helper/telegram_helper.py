from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from bot import bot

class Message:
    async def send_msg(chat_id, msg, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=True):
        if btn:
            reply_markup = InlineKeyboardMarkup(btn)
            sent_msg = await bot.send_message(
                chat_id=chat_id,
                text=msg,
                reply_markup=reply_markup,
                disable_web_page_preview=bool(disable_web_preview),
                parse_mode=parse_mode
            )
        else:
            sent_msg = await bot.send_message(
                chat_id=chat_id,
                text=msg,
                disable_web_page_preview=bool(disable_web_preview),
                parse_mode=parse_mode
            )

        return sent_msg

    
    async def send_img(chat_id, img, caption=None, btn=None, parse_mode=ParseMode.HTML):
        if btn:
            reply_markup = InlineKeyboardMarkup(btn)
            sent_msg = await bot.send_photo(
                chat_id=chat_id,
                photo=img,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        else:
            sent_msg = await bot.send_photo(
                chat_id=chat_id,
                photo=img,
                caption=caption,
                parse_mode=parse_mode
            )

        return sent_msg


    async def send_vid(chat_id, video, thumbnail=None, caption=None, btn=None, parse_mode=ParseMode.HTML):
        if btn:
            reply_markup = InlineKeyboardMarkup(btn)
            sent_vid = await bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=caption,
                reply_markup=reply_markup,
                thumbnail=thumbnail,
                height=1080,
                width=1920,
                parse_mode=parse_mode
            )
        else:
            sent_vid = await bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=caption,
                thumbnail=thumbnail,
                height=1080,
                width=1920,
                parse_mode=parse_mode
            )
        return sent_vid


    async def send_audio(chat_id, audio, title, caption=None):
        await bot.send_audio(
            chat_id=chat_id,
            audio=audio,
            title=title,
            caption=caption
        )

    
    async def reply_msg(update: Update, msg, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=True):
        message = update.message

        if message.reply_to_message:
            message_id = message.reply_to_message.message_id
        else:
            message_id = message.message_id

        if btn:
            reply_markup = InlineKeyboardMarkup(btn)
            sent_msg = await update.message.reply_text(
                text=msg,
                disable_web_page_preview=bool(disable_web_preview),
                reply_to_message_id=message_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        else:
            sent_msg = await update.message.reply_text(
                text=msg,
                disable_web_page_preview=bool(disable_web_preview),
                reply_to_message_id=message_id,
                parse_mode=parse_mode
            )
        return sent_msg


    async def edit_msg(update: Update, edit_msg_text, sent_msg_pointer, btn=None, parse_mode=ParseMode.HTML, disable_web_preview=True):
        caption_msg = sent_msg_pointer.caption
        chat_id = update.effective_chat.id
        msg_id = sent_msg_pointer.message_id

        if caption_msg:
            if btn:
                reply_markup = InlineKeyboardMarkup(btn)
                await bot.edit_message_caption(
                    caption=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
            else:
                await bot.edit_message_caption(
                    caption=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    parse_mode=parse_mode
                )
        else:
            if btn:
                reply_markup = InlineKeyboardMarkup(btn)
                await bot.edit_message_text(
                    text=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    reply_markup=reply_markup,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode
                )
            else:
                await bot.edit_message_text(
                    text=edit_msg_text,
                    chat_id=chat_id,
                    message_id=msg_id,
                    disable_web_page_preview=bool(disable_web_preview),
                    parse_mode=parse_mode
                )
    

    async def del_msg(chat_id, del_msg_pointer):
        msg_id = del_msg_pointer.message_id
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)


class Button:
    async def ubutton(btn_name, url, same_line=bool(False)):
        '''
        btn_name & url should be in list [ ]
        eg. await Message.reply_msg(update, "This is a message...", btn + btn2)
        '''
        btn = []
        sbtn = []
        try:
            if len(btn_name) == len(url):
                for b_name, url_link in zip(btn_name, url):
                    if same_line:
                        sbtn.append(InlineKeyboardButton(b_name, url_link))
                    else:
                        btn.append([InlineKeyboardButton(b_name, url_link)])
            else:
                print(f"Error: btn={len(btn_name)} not equal url={len(url)}! Skiping...")

            buttons = btn+[sbtn]
            return buttons
        except Exception as e:
            print(f"Error ubutton: {e}")
    

    async def cbutton(btn_name, callback_name, same_line=bool(False)):
        '''
        btn_name & callback_name should be in list [ ]
        eg. await Message.reply_msg(update, "This is a message...", btn + btn2)
        '''
        btn = []
        sbtn = []
        try:
            if len(btn_name) == len(callback_name):
                for b_name, c_name in zip(btn_name, callback_name):
                    if same_line:
                        sbtn.append(InlineKeyboardButton(b_name, callback_data=c_name))
                    else:
                        btn.append([InlineKeyboardButton(b_name, callback_data=c_name)])
            else:
                print(f"Error: btn={len(btn_name)} not equal callback={len(callback_name)}! Skiping...")

            buttons = btn+[sbtn]
            return buttons
        except Exception as e:
            print(f"Error cbutton: {e}")
