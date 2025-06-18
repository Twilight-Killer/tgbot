import asyncio
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import Forbidden
from bot.utils.decorators.sudo_users import require_sudo

@require_sudo
async def func_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message
    re_msg = message.reply_to_message
    context_args = " ".join(context.args) # contains something if forward is true and contains victim_id >> /send f chat_id
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await chat.delete_messages([message.id, sent_message.id])
        return
    
    if not context_args or not re_msg:
        text = (
            "Use <code>/send ChatID</code> by replying a message!\n"
            "<code>/send f ChatID</code> to forward the replied message to ChatID!\n"
            "<blockquote expandable>Returns reaction on message\n"
            "- Sent: 👍\n"
            "- Forbidden: 👎\n"
            "- Something went wrong: 🤷‍♂ </blockquote>"
        )
        await message.reply_text(text)
        return
    
    forward_confirm = None
    victim_id = context_args
    reaction = "👍"

    splited_text = context_args.split()
    if len(splited_text) == 2:
        forward_confirm, victim_id = splited_text
    
    try:
        if forward_confirm:
            await context.bot.forward_message(victim_id, chat.id, re_msg.id)
        
        else:
            text = re_msg.text_html
            caption = re_msg.caption_html
            photo = re_msg.photo
            audio = re_msg.audio
            video = re_msg.video
            document = re_msg.document
            voice = re_msg.voice
            video_note = re_msg.video_note
            btn = re_msg.reply_markup

            if text:
                await context.bot.send_message(victim_id, text, reply_markup=btn)

            elif photo:
                await context.bot.send_photo(victim_id, photo[-1].file_id, caption, reply_markup=btn)

            elif audio:
                await context.bot.send_audio(victim_id, audio.file_id, title=audio.file_name, caption=caption, reply_markup=btn, filename=audio.file_name)

            elif video:
                await context.bot.send_video(victim_id, video.file_id, caption=caption, reply_markup=btn)

            elif document:
                await context.bot.send_document(victim_id, document.file_id, caption, reply_markup=btn, filename=document.file_name)
            
            elif voice:
                await context.bot.send_voice(victim_id, voice.file_id, caption=caption, reply_markup=btn)
            
            elif video_note:
                await context.bot.send_video_note(victim_id, video_note.file_id, reply_markup=btn)
            
            else:
                await message.reply_text("Replied content isn't added yet. Stay tuned for future update.")
                return
            
    except Forbidden:
        reaction = "👎"
    except:
        reaction = "🤷‍♂"

    await message.set_reaction([ReactionTypeEmoji(reaction)])
