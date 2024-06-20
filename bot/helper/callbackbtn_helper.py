import json
from urllib.parse import urlparse
from telegram import Update
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import global_search
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.functions.power_users import _power_users
from bot.update_db import update_database
from bot.modules.github import GitHub


async def func_callbackbtn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat

    async def popup(msg):
        await query.answer(msg, True)
    
    async def del_query():
        try:
            await query.message.delete()
        except Exception as e:
            logger.error(e)
    
    data_center = await LOCAL_DATABASE.find_one("data_center", chat.id)
    if not data_center:
        await popup(f"{chat.id} wasn't found in data center!")
        await del_query()
        return
    
    user_id = data_center.get("user_id")
    if not user_id:
        await popup(f"Error: {user_id} not found!")
        await del_query()
        return
    
    if user.id != user_id:
        await popup("Access Denied!")
        return
    
    if query.data in ["query_back", "query_close"]:
        with open(f"back_btn/{chat.id}.txt", "rb") as f:
            btn = f.read()
            
        await Message.edit_msg(update, "EDITED", query.message, btn)
        return
    
    dc_collection_name = data_center.get("collection_name")
    dc_db_find = data_center.get("db_find")
    dc_db_vlaue = data_center.get("db_vlaue")
    db = await global_search(dc_collection_name, dc_db_find, dc_db_vlaue)
    if db[0] == False:
        await Message.reply_msg(update, db[1])
        return
    
    find_chat = db[1]
    
    if chat.type == "private":
        if query.data in [
            "query_bot_pic",
            "query_welcome_img",
            "query_images",
            "query_support_chat",
            "query_server_url",
            "query_sudo",
            "query_shrinkme_api",
            "query_omdb_api",
            "query_weather_api",
            "query_restore_db"
        ]:
            power_users = await _power_users()
            if user.id in power_users:
                if query.data == "query_bot_pic":
                    data_center["edit_data_key"] = "bot_pic"
                    bot_pic = find_chat.get("bot_pic")

                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        f"Bot pic: <code>{bot_pic}</code>\n\n"
                        "<i><b>Note</b>: Send an image url/link to set bot pic!</i>"
                    )

                    btn_name_row1 = ["Edit Value", "Remove Value"]
                    btn_data_row1 = ["query_edit_value", "query_rm_value"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_back", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "query_welcome_img":
                    data_center["edit_data_key"] = "welcome_img"
                    welcome_img = find_chat.get("welcome_img")

                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        f"Welcome img: {welcome_img}\n\n"
                        "<i><b>Note</b>: Should bot show image on start?</i>"
                    )

                    btn_name_row1 = ["Yes", "No"]
                    btn_data_row1 = ["true", "false"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_bot_settings_menu", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "query_images":
                    data_center["edit_data_key"] = "images"
                    images = find_chat.get("images")

                    if images:
                        if len(str(images)) > 4096:
                            storage, counter = "", 0
                            for image in images:
                                counter += 1
                                if counter == len(images):
                                    storage += f"{image}"
                                else:
                                    storage += f"{image}, "
                            images = storage
                            with open("tmp.txt", "w") as f:
                                f.write(images)
                            with open("tmp.txt", "rb") as f:
                                tmp_file = f.read()
                            await Message.send_doc(chat.id, tmp_file, "tmp.txt", "images links")
                            images = "Text file sent below!"
                        else:
                            storage, counter = "", 0
                            for i in images:
                                counter += 1
                                if counter == len(images):
                                    storage += f"{i}"
                                else:
                                    storage += f"{i}, "
                            images = storage
                    
                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        f"images: <code>{images}</code>\n\n"
                        "<i><b>Note</b>: Single image or Upload multiple image link separated by comma!</i>"
                    )

                    btn_name_row1 = ["Edit Value", "Remove Value"]
                    btn_data_row1 = ["query_edit_value", "query_rm_value"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_bot_settings_menu", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "query_support_chat":
                    data_center["edit_data_key"] = "support_chat"
                    support_chat = find_chat.get("support_chat")

                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        f"Support Chat (link): <code>{support_chat}</code>\n"
                    )

                    btn_name_row1 = ["Edit Value", "Remove Value"]
                    btn_data_row1 = ["query_edit_value", "query_rm_value"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_bot_settings_menu", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "query_server_url":
                    data_center["edit_data_key"] = "server_url"
                    server_url = find_chat.get("server_url")

                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        f"Server url: <code>{server_url}</code>\n\n"
                        "<i><b>Note</b>: Bot will fall asleep if you deployed the bot on render (free) and don't set this value...</i>"
                    )

                    btn_name_row1 = ["Edit Value", "Remove Value"]
                    btn_data_row1 = ["query_edit_value", "query_rm_value"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_bot_settings_menu", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "query_sudo":
                    data_center["edit_data_key"] = "sudo_users"
                    sudo_users = find_chat.get("sudo_users")

                    if sudo_users:
                        storage, counter = "", 0
                        for i in sudo_users:
                            counter += 1
                            if counter == len(sudo_users):
                                storage += f"{i}"
                            else:
                                storage += f"{i}, "
                        sudo_users = storage

                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        f"$udo users: <code>{sudo_users}</code>\n\n"
                        "<i><b>Note</b>: The power user! Sudo users have owner function access!\nAdd user_id eg. <code>2134776547</code></i>"
                    )

                    btn_name_row1 = ["Edit Value", "Remove Value"]
                    btn_data_row1 = ["query_edit_value", "query_rm_value"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_bot_settings_menu", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "query_shrinkme_api":
                    data_center["edit_data_key"] = "shrinkme_api"
                    shrinkme_api = find_chat.get("shrinkme_api")

                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        f"Shrinkme API: <code>{shrinkme_api}</code>\n\n"
                        "<i><b>Note</b>: This api for /short command!</i>"
                    )

                    btn_name_row1 = ["Edit Value", "Remove Value"]
                    btn_data_row1 = ["query_edit_value", "query_rm_value"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_bot_settings_menu", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "query_omdb_api":
                    data_center["edit_data_key"] = "omdb_api"
                    omdb_api = find_chat.get("omdb_api")

                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        f"OMDB API: <code>{omdb_api}</code>\n\n"
                        "<i><b>Note</b>: This api for /movie command!</i>"
                    )

                    btn_name_row1 = ["Edit Value", "Remove Value"]
                    btn_data_row1 = ["query_edit_value", "query_rm_value"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_bot_settings_menu", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "query_weather_api":
                    data_center["edit_data_key"] = "weather_api"
                    weather_api = find_chat.get("weather_api")

                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        f"Weather API: <code>{weather_api}</code>\n\n"
                        "<i><b>Note</b>: This api for /weather command!</i>"
                    )

                    btn_name_row1 = ["Edit Value", "Remove Value"]
                    btn_data_row1 = ["query_edit_value", "query_rm_value"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_bot_settings_menu", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "query_restore_db":
                    msg = (
                        "<u><b>Bot Settings</b></u>\n\n"
                        "Which data will be deleted? ⚠\n"
                        "- All bot setting\n\n"
                        "Which data won't be deleted?\n"
                        "- Bot users/groups data\n\n"
                        f"<i><b>Note</b>: This will erase all bot data/settings from database and restore data/settings from <code>config.env</code></i>"
                    )

                    btn_name_row1 = ["⚠ Restore Database"]
                    btn_data_row1 = ["confirm_restore_db"]

                    btn_name_row2 = ["Back", "Close"]
                    btn_data_row2 = ["query_bot_settings_menu", "query_close"]

                    row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
                    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

                    btn = row1 + row2

                    await Message.edit_msg(update, msg, query.message, btn)
                
                elif query.data == "confirm_restore_db":
                    await MongoDB.delete_all_doc("bot_docs")
                    res = await update_database()
                    msg = "Database data has been restored successfully from <code>config.env</code>!" if res else "Something went wrong!"
                    await Message.send_msg(data_center.get("chat_id"), msg)

                elif query.data == "query_bot_settings_menu":
                    btn = data_center.get("back_btn")
                    await Message.edit_msg(update, "<u><b>Bot Settings</b></u>", query.message, btn)



















































    #     if  query.data == "group_management":
    #         msg = (
    #             "Group Moderation Commands -\n\n"
    #             "/id » Show chat/user id\n"
    #             "/invite » Generate/Get invite link\n"
    #             "/promote » Promote a member\n"
    #             "/demote » Demote a member\n"
    #             "/pin » Pin message loudly\n"
    #             "/unpin » Unpin a pinned message or all pinned messages\n"
    #             "/ban » Ban a member\n"
    #             "/unban » Unban a member\n"
    #             "/kick » Kick a member\n"
    #             "/kickme » The easy way to out\n"
    #             "/mute » Mute a member (member will be unable to send messages etc.)\n"
    #             "/unmute » Unmute a member (member will be able to send messages etc.)\n"
    #             "/del » Delete replied message with notifying/telling something to the member!\n"
    #             "/purge » Delete every messages from replied message to current message!\n"
    #             "/lock » Lock the chat (no one can send messages etc.)\n"
    #             "/unlock » Unlock the chat (back to normal)\n"
    #             "/filters | /filter | /remove » To see/set/remove custom message/command\n"
    #             "/adminlist » See chat admins list\n"
    #             "/settings » Settings of chat (welcome, antibot, translate etc.)\n\n"
    #             "<i><b>Note</b>: Type commands to get more details about the command function!</i>"
    #         )

    #         btn_name = ["Back", "Close"]
    #         btn_data = ["help_menu", "query_close"]
    #         btn = await Button.cbutton(btn_name, btn_data, True)

    #         await Message.edit_msg(update, msg, query.message, btn)

















































    # if chat.type == "private":
    #     data_to_find = "db_user_data"
    # else:
    #     data_to_find = "db_group_data"

    
    




















    # # youtube ------------------------------------------------------------------------ Youtube
    # if  query.data == "mp4":
    #     context.user_data["content_format"] = data

    # elif query.data == "mp3":
    #     context.user_data["content_format"] = data
    
    # # -------------------------------------------------------------- Group management
    # elif query.data == "unpin_all":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     chat_id = context.chat_data.get("chat_id")
    #     if not chat_id:
    #         await popup("Error: chat_id not found!")
    #         await query.message.delete()
    #         return
        
    #     try:
    #         await bot.unpin_all_chat_messages(chat_id)
    #         await Message.send_msg(chat_id, "All pinned messages has been unpinned successfully!")
    #         await query.message.delete()
    #     except Exception as e:
    #         logger.error(e)
    
    # elif query.data == "filters":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     chat_id = context.chat_data.get("chat_id")
    #     if not chat_id:
    #         await popup("Error: chat_id not found!")
    #         await query.message.delete()
    #         return
        
    #     try:
    #         try:
    #             find_group = context.chat_data["db_group_data"]
    #         except Exception as e:
    #             logger.error(e)
    #             find_group = None
            
    #         if not find_group:
    #             find_group = await MongoDB.find_one("groups", "chat_id", chat_id)
    #             if find_group:
    #                 context.chat_data["db_group_data"] = find_group

    #         if find_group:
    #             filters = find_group.get("filters")
    #             msg = f"Chat filters -\n"
    #             if filters:
    #                 for keyword in filters:
    #                     msg += f"- {keyword}\n"
    #             else:
    #                 msg += "- No filters"

    #             btn_name = ["Close"]
    #             btn_data = ["query_close"]
    #             btn = await Button.cbutton(btn_name, btn_data)

    #             await Message.edit_msg(update, msg, query.message, btn)
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
    #     except Exception as e:
    #         logger.error(e)
    
    # # Group management ----------------------------------------------------------------- help starts
    # el
    
    # elif query.data == "ai":
    #     msg = (
    #         "Artificial intelligence functions -\n\n"
    #         "/imagine » Generate AI image\n"
    #         "/gpt » Ask any question to ChatGPT\n\n"
    #         "<i><b>Note</b>: Type commands to get more details about the command function!</i>"
    #     )

    #     btn_name = ["Back", "Close"]
    #     btn_data = ["help_menu", "query_close"]
    #     btn = await Button.cbutton(btn_name, btn_data, True)

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "misc_func":
    #     msg = (
    #         "Misc functions -\n\n"
    #         "/movie » Get any movie info by name/imdb_id\n"
    #         "/tr » Translate any language\n"
    #         "/decode » Decode - base64 to text\n"
    #         "/encode » Encode - text to base64\n"
    #         "/short » Short any url\n"
    #         "/ping » Ping any url\n"
    #         "/calc » Calculate any math (supported syntex: +, -, *, /)\n"
    #         "/webshot » Take Screenshot of any website\n"
    #         "/weather » Get weather info of any city\n"
    #         "/ytdl » Download youtube video\n"
    #         "/yts » Search video on youtube\n"
    #         "/qr » To generate a QR code\n"
    #         "/itl » To convert image into link\n"
    #         "/id » Show chat/user id\n"
    #         "/settings » Settings of chat\n\n"
    #         "<i><b>Note</b>: Type commands to get more details about the command function!</i>"
    #     )

    #     btn_name = ["Back", "Close"]
    #     btn_data = ["help_menu", "query_close"]
    #     btn = await Button.cbutton(btn_name, btn_data, True)

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "owner_func":
    #     msg = (
    #         "Bot owner functions -\n\n"
    #         "/broadcast » Broadcast message to bot users\n"
    #         "/db » Get bot database\n"
    #         "/bsetting » Get bot settings\n"
    #         "/shell » Use system shell\n"
    #         "/log » Get log file (for error handling)\n"
    #         "/restart » Restart the bot\n"
    #         "/sys » Get system info\n\n"
    #         "<i><b>Note</b>: Type commands to get more details about the command function!</i>"
    #     )

    #     btn_name = ["Back", "Close"]
    #     btn_data = ["help_menu", "query_close"]
    #     btn = await Button.cbutton(btn_name, btn_data, True)

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "github_stats":
    #     github_repo = await MongoDB.get_data("bot_docs", "github_repo")
    #     latest_commit = await GitHub.get_latest_commit("bishalqx980", "tgbot")
    #     if latest_commit:
    #         try:
    #             l_c_sha = latest_commit.get("sha")
    #             l_c_commit = latest_commit.get("commit") # not for use
    #             l_c_message = l_c_commit.get("message")
    #             l_c_author = l_c_commit.get("author") # not for use
    #             l_c_aname = l_c_author.get("name")
    #             l_c_date = l_c_author.get("date")
    #             l_c_link = f"https://github.com/bishalqx980/tgbot/commit/{l_c_sha}"

    #             msg = (
    #                 f"<b>» Original repo [ <a href='{l_c_link}'>latest commit</a> ]</b>\n"
    #                 f"<b>Last update:</b> <code>{l_c_date}</code>\n"
    #                 f"<b>Commit:</b> <code>{l_c_message}</code>\n"
    #                 f"<b>Committed by:</b> <code>{l_c_aname}</code>\n"
    #             )
    #         except:
    #             msg = latest_commit
    #     else:
    #         msg = "Error..."

    #     if github_repo:
    #         try:
    #             parse_url = urlparse(github_repo)
    #             split_all = parse_url.path.strip("/").split("/")
    #             username, repo_name = split_all
    #             bot_repo_commit = await GitHub.get_latest_commit(username, repo_name)
    #             if latest_commit:
    #                 b_r_sha = bot_repo_commit.get("sha")
    #                 b_r_commit = bot_repo_commit.get("commit") # not for use
    #                 b_r_message = b_r_commit.get("message")
    #                 b_r_author = b_r_commit.get("author") # not for use
    #                 b_r_aname = b_r_author.get("name")
    #                 b_r_date = b_r_author.get("date")
    #                 b_r_link = f"https://github.com/{username}/{repo_name}/commit/{b_r_sha}"
                    
    #                 msg = (
    #                     msg + f"\n<b>» Bot repo [ <a href='{b_r_link}'>commit</a> ]</b>\n"
    #                     f"<b>Last update:</b> <code>{b_r_date}</code>\n"
    #                     f"<b>Commit:</b> <code>{b_r_message}</code>\n"
    #                     f"<b>Committed by:</b> <code>{b_r_aname}</code>\n"
    #                 )

    #                 if l_c_sha != b_r_sha:
    #                     msg += "\n<i>The bot repo isn't updated to the latest commit! ⚠</i>"
    #                 else:
    #                     msg += "\n<i>The bot repo is updated to the latest commit...</i>"
    #             else:
    #                 msg = "Error..."
    #         except Exception as e:
    #             logger.error(e)
        
    #     btn_name = ["Back", "Close"]
    #     btn_data = ["help_menu", "query_close"]
    #     btn = await Button.cbutton(btn_name, btn_data, True)

    #     await Message.edit_msg(update, msg, query.message, btn)

    # elif query.data == "help_menu":
    #     db = await MongoDB.info_db()
    #     for i in db:
    #         if i[0] == "users":
    #             total_users = i[1]
    #             break
    #         else:
    #             total_users = "❓"
        
    #     active_status = await MongoDB.find("users", "active_status")
    #     active_users = active_status.count(True)
    #     inactive_users = active_status.count(False)

    #     msg = (
    #         f"Hi {user.mention_html()}! Welcome to the bot help section...\n"
    #         f"I'm a comprehensive Telegram bot designed to manage groups and perform various functions...\n\n"
    #         f"/start - to start the bot\n"
    #         f"/help - to see this message\n\n"
    #         f"T.users: {total_users} | "
    #         f"A.users: {active_users} | "
    #         f"Inactive: {inactive_users}"
    #     )

    #     btn_name_row1 = ["Group Management", "Artificial intelligence"]
    #     btn_data_row1 = ["group_management", "ai"]

    #     btn_name_row2 = ["misc", "Bot owner"]
    #     btn_data_row2 = ["misc_func", "owner_func"]

    #     btn_name_row3 = ["GitHub", "Close"]
    #     btn_data_row3 = ["github_stats", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
    #     row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

    #     btn = row1 + row2 + row3

    #     await Message.edit_msg(update, msg, query.message, btn)
    # # ---------------------------------------------------------------------------- help ends
    # # bot settings ------------------------------------------------------------- bsettings starts
    # el
    # # ---------------------------------------------------------------------------- bsettings ends
    # # chat setting -------------------------------------------------------------- Chat settings starts
    # elif query.data == "lang":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return
        
    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     try:
    #         _bot = context.bot_data["db_bot_data"]
    #     except Exception as e:
    #         logger.error(e)
    #         find = await MongoDB.find("bot_docs", "_id")
    #         _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
    #         context.bot_data["db_bot_data"] = _bot
        
    #     lang = find_chat.get("lang")
    #     context.chat_data["edit_data_name"] = "lang"

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Language code: <code>{lang}</code>\n\n"
    #         "<i><b>Note</b>: Get your country language code from the below link!\neg. English language code is <code>en</code></i>"
    #     )

    #     btn_name_row1 = ["Language code's"]
    #     btn_url_row1 = ["https://telegra.ph/Language-Code-12-24"]

    #     btn_name_row2 = ["Edit Value"]
    #     btn_data_row2 = ["edit_value"]

    #     btn_name_row3 = ["Back", "Close"]
    #     btn_data_row3 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.ubutton(btn_name_row1, btn_url_row1)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
    #     row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

    #     btn = row1 + row2 + row3

    #     await Message.edit_msg(update, msg, query.message, btn)

    # elif query.data == "auto_tr":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     auto_tr = find_chat.get("auto_tr")

    #     context.chat_data["edit_data_name"] = "auto_tr"

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Auto translate: <code>{auto_tr}</code>\n\n"
    #         "<i><b>Note</b>: This will automatically translate chat conversation into chat default language!</i>"
    #     )

    #     btn_name_row1 = ["Enable", "Disable"]
    #     btn_data_row1 = ["true", "false"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)

    # elif query.data == "set_echo":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     echo = find_chat.get("echo")

    #     context.chat_data["edit_data_name"] = "echo"

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Echo: <code>{echo}</code>\n\n"
    #         "<i><b>Note</b>: This will repeat user message!</i>"
    #     )

    #     btn_name_row1 = ["Enable", "Disable"]
    #     btn_data_row1 = ["true", "false"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "welcome_msg":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     welcome_msg = find_chat.get("welcome_msg")

    #     context.chat_data["edit_data_name"] = "welcome_msg"

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Welcome user: <code>{welcome_msg}</code>\n\n"
    #         "<i><b>Note</b>: This will welcome the new chat member!</i>"
    #     )

    #     btn_name_row1 = ["Enable", "Disable"]
    #     btn_data_row1 = ["true", "false"]

    #     btn_name_row2 = ["Set custom message"]
    #     btn_data_row2 = ["set_custom_msg"]

    #     btn_name_row3 = ["Back", "Close"]
    #     btn_data_row3 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
    #     row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

    #     btn = row1 + row2 + row3

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "set_custom_msg":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     custom_welcome_msg = find_chat.get("custom_welcome_msg")

    #     context.chat_data["edit_data_name"] = "custom_welcome_msg"

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Welcome message\n--------------------\n<code>{custom_welcome_msg}</code>\n\n"
    #         "<i><b>Note</b>: This message will be send as greeting message in the chat when a user join!</i>"
    #     )

    #     btn_name_row1 = ["Set default message", "Set custom message"]
    #     btn_data_row1 = ["remove_value", "edit_value"]

    #     btn_name_row2 = ["Text formatting"]
    #     btn_data_row2 = ["text_formats"]

    #     btn_name_row3 = ["Back", "Close"]
    #     btn_data_row3 = ["welcome_msg", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2)
    #     row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

    #     btn = row1 + row2 + row3

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "text_formats":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     chat_id = context.chat_data.get("chat_id")
    #     if not chat_id:
    #         await popup("Error: chat_id not found!")
    #         await query.message.delete()
    #         return
        
    #     msg = (
    #         "<blockquote>Formatting</blockquote>\n"
    #         "<code>{first}</code>: The user's firstname\n"
    #         "<code>{last}</code>: The user's lastname\n"
    #         "<code>{fullname}</code>: The user's fullname\n"
    #         "<code>{username}</code>: The user's username\n"
    #         "<code>{mention}</code>: To mention the user\n"
    #         "<code>{id}</code>: The user's ID\n"
    #         "<code>{chatname}</code>: Chat title\n\n"
    #         "Example: <code>Hi {mention}, welcome to {chatname}</code>\n"
    #     )

    #     btn_name = ["query_close"]
    #     btn_data = ["query_close"]
        
    #     btn = await Button.cbutton(btn_name, btn_data)
        
    #     await Message.send_msg(chat_id, msg, btn)

    # elif query.data == "goodbye_msg":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     goodbye_msg = find_chat.get("goodbye_msg")

    #     context.chat_data["edit_data_name"] = "goodbye_msg"

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Goodbye user: <code>{goodbye_msg}</code>\n\n"
    #         "<i><b>Note</b>: This will send a farewell message to chat when a user left!\n</i>"
    #     )

    #     btn_name_row1 = ["Enable", "Disable"]
    #     btn_data_row1 = ["true", "false"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)

    # elif query.data == "antibot":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     antibot = find_chat.get("antibot")

    #     context.chat_data["edit_data_name"] = "antibot"

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Antibot: <code>{antibot}</code>\n\n"
    #         "<i><b>Note</b>: This will prevent other bot from joining in chat!</i>"
    #     )

    #     btn_name_row1 = ["Enable", "Disable"]
    #     btn_data_row1 = ["true", "false"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "del_cmd":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     del_cmd = find_chat.get("del_cmd")

    #     context.chat_data["edit_data_name"] = "del_cmd"

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Delete cmd: <code>{del_cmd}</code>\n\n"
    #         "<i><b>Note</b>: This will delete bot commands when you will send a command in chat!</i>"
    #     )

    #     btn_name_row1 = ["Enable", "Disable"]
    #     btn_data_row1 = ["true", "false"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "log_channel":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     context.chat_data["edit_data_name"] = "log_channel"

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     log_channel = find_chat.get("log_channel")

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Log channel: <code>{log_channel}</code>\n\n"
    #         "<i><b>Note</b>: This will log every actions occurred in your chat (ban, kick, mute, etc.) using bot!\nAdd the bot in a channel as admin where you want to log, then you will get a message with chat_id from bot, pass the chat_id using edit value!</i>"
    #     )

    #     btn_name_row1 = ["Edit Value", "Remove Value"]
    #     btn_data_row1 = ["query_edit_value", "query_rm_value"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "links_behave":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     all_links = find_chat.get("all_links")
    #     allowed_links = find_chat.get("allowed_links")
    #     if allowed_links:
    #         storage, counter = "", 0
    #         for i in allowed_links:
    #             counter += 1
    #             if counter == len(allowed_links):
    #                 storage += f"{i}"
    #             else:
    #                 storage += f"{i}, "
    #         allowed_links = storage

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"All links: <code>{all_links}</code>\n"
    #         f"Allowed links: <code>{allowed_links}</code>\n\n"
    #         "<i><b>Note</b>: Select whether it will delete or convert the links into base64 or do nothing if links in message!</i>\n\n"
    #         "<i>Allowed links » these links won't be deleted!</i>\n"
    #         "<i>Delete links » replace the links with `forbidden link`</i>\n\n"
    #         "<i>Echo/Auto translate won't work if message contains link!</i>"
    #     )

    #     btn_name_row1 = ["All links", "Allowed links"]
    #     btn_data_row1 = ["all_links", "allowed_links"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)

    # elif query.data == "all_links":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     context.chat_data["edit_data_name"] = "all_links"

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     all_links = find_chat.get("all_links")

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"All links: <code>{all_links}</code>\n\n"
    #         "<i><b>Note</b>: Select whether bot will delete the message or convert link into base64 or do nothing!</i>"
    #     )

    #     btn_name_row1 = ["Delete", "Convert", "Nothing"]
    #     btn_data_row1 = ["d_links", "c_links", "none_links"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["links_behave", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "allowed_links":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     context.chat_data["edit_data_name"] = "allowed_links"

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     allowed_links = find_chat.get("allowed_links")
    #     if allowed_links:
    #         storage, counter = "", 0
    #         for i in allowed_links:
    #             counter += 1
    #             if counter == len(allowed_links):
    #                 storage += f"{i}"
    #             else:
    #                 storage += f"{i}, "
    #         allowed_links = storage

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"Allowed links: <code>{allowed_links}</code>\n\n"
    #         "<i><b>Note</b>: Send domain name of allowed links eg. <code>google.com</code> multiple domain will be separated by comma!</i>"
    #     )

    #     btn_name_row1 = ["Edit Value", "Remove Value"]
    #     btn_data_row1 = ["query_edit_value", "query_rm_value"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["links_behave", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "d_links":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     chat_id = context.chat_data.get("chat_id")
    #     if not chat_id:
    #         await popup("Error: chat_id not found!")
    #         await query.message.delete()
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname") # set from main.py
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return
        
    #     find_data = context.chat_data.get("find_data") # set from main.py
    #     match_data = context.chat_data.get("match_data") # set from main.py
    #     edit_data_name = context.chat_data.get("edit_data_name") # set from query data
    #     edit_data_value = "delete"

    #     if not edit_data_name:
    #         await popup("I don't know which data to update! Please go back and then try again!")
    #         return

    #     try:
    #         await MongoDB.update_db(edit_cname, find_data, match_data, edit_data_name, edit_data_value)
    #         await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {edit_data_value}")

    #         db_chat_data = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         context.chat_data[data_to_find] = db_chat_data
    #     except Exception as e:
    #         logger.error(e)
    #         await Message.send_msg(chat_id, f"Error: {e}")
    
    # elif query.data == "c_links":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     chat_id = context.chat_data.get("chat_id")
    #     if not chat_id:
    #         await popup("Error: chat_id not found!")
    #         await query.message.delete()
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname") # set from main.py
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return
        
    #     find_data = context.chat_data.get("find_data") # set from main.py
    #     match_data = context.chat_data.get("match_data") # set from main.py
    #     edit_data_name = context.chat_data.get("edit_data_name") # set from query data
    #     edit_data_value = "convert"

    #     if not edit_data_name:
    #         await popup("I don't know which data to update! Please go back and then try again!")
    #         return

    #     try:
    #         await MongoDB.update_db(edit_cname, find_data, match_data, edit_data_name, edit_data_value)
    #         await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {edit_data_value}")

    #         db_chat_data = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         context.chat_data[data_to_find] = db_chat_data
    #     except Exception as e:
    #         logger.error(e)
    #         await Message.send_msg(chat_id, f"Error: {e}")
    
    # elif query.data == "none_links":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     chat_id = context.chat_data.get("chat_id")
    #     if not chat_id:
    #         await popup("Error: chat_id not found!")
    #         await query.message.delete()
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname") # set from main.py
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return
        
    #     find_data = context.chat_data.get("find_data") # set from main.py
    #     match_data = context.chat_data.get("match_data") # set from main.py
    #     edit_data_name = context.chat_data.get("edit_data_name") # set from query data
    #     edit_data_value = None

    #     if not edit_data_name:
    #         await popup("I don't know which data to update! Please go back and then try again!")
    #         return

    #     try:
    #         await MongoDB.update_db(edit_cname, find_data, match_data, edit_data_name, edit_data_value)
    #         await popup(f"Database updated!\n\nData: {edit_data_name}\nValue: {edit_data_value}")

    #         db_chat_data = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         context.chat_data[data_to_find] = db_chat_data
    #     except Exception as e:
    #         logger.error(e)
    #         await Message.send_msg(chat_id, f"Error: {e}")
    
    # elif query.data == "ai_status":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return

    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")

    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     ai_status = find_chat.get("ai_status")

    #     context.chat_data["edit_data_name"] = "ai_status"

    #     msg = (
    #         "<u><b>Chat Settings</b></u>\n\n"
    #         f"AI status: <code>{ai_status}</code>\n\n"
    #         "<i><b>Note</b>: Enable / Disbale AI functions in chat!</i>"
    #     )

    #     btn_name_row1 = ["Enable", "Disable"]
    #     btn_data_row1 = ["true", "false"]

    #     btn_name_row2 = ["Back", "Close"]
    #     btn_data_row2 = ["c_setting_menu", "query_close"]

    #     row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #     row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #     btn = row1 + row2

    #     await Message.edit_msg(update, msg, query.message, btn)
    
    # elif query.data == "c_setting_menu":
    #     access = await _check_whois()
    #     if not access:
    #         return
        
    #     edit_cname = context.chat_data.get("edit_cname")
    #     if not edit_cname:
    #         await popup("An error occurred! send command again then try...")
    #         await query.message.delete()
    #         return
        
    #     find_data = context.chat_data.get("find_data")
    #     match_data = context.chat_data.get("match_data")
        
    #     try:
    #         find_chat = context.chat_data[data_to_find]
    #     except Exception as e:
    #         logger.error(e)
    #         find_chat = None
        
    #     if not find_chat:
    #         find_chat = await MongoDB.find_one(edit_cname, find_data, match_data)
    #         if find_chat:
    #             context.chat_data[data_to_find] = find_chat
    #         else:
    #             await popup("⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
    #             await query.message.delete()
    #             return
        
    #     if data_to_find == "db_group_data":
    #         title = find_chat.get("title")
    #         lang = find_chat.get("lang")

    #         echo = find_chat.get("echo")
    #         auto_tr = find_chat.get("auto_tr")
    #         welcome_msg = find_chat.get("welcome_msg")
    #         goodbye_msg = find_chat.get("goodbye_msg")
    #         antibot = find_chat.get("antibot")
    #         ai_status = find_chat.get("ai_status")
    #         del_cmd = find_chat.get("del_cmd")
    #         all_links = find_chat.get("all_links")
    #         allowed_links = find_chat.get("allowed_links")
    #         if allowed_links:
    #             storage, counter = "", 0
    #             for i in allowed_links:
    #                 counter += 1
    #                 if counter == len(allowed_links):
    #                     storage += f"{i}"
    #                 else:
    #                     storage += f"{i}, "
    #             allowed_links = storage

    #         log_channel = find_chat.get("log_channel")

    #         msg = (
    #             f"<u><b>Chat Settings</b></u>\n\n"
    #             f"• Title: {title}\n"
    #             f"• ID: <code>{chat.id}</code>\n\n"

    #             f"• Lang: <code>{lang}</code>\n"
    #             f"• Echo: <code>{echo}</code>\n"
    #             f"• Auto tr: <code>{auto_tr}</code>\n"
    #             f"• Welcome user: <code>{welcome_msg}</code>\n"
    #             f"• Goodbye user: <code>{goodbye_msg}</code>\n"
    #             f"• Antibot: <code>{antibot}</code>\n"
    #             f"• AI status: <code>{ai_status}</code>\n"
    #             f"• Delete cmd: <code>{del_cmd}</code>\n"
    #             f"• All links: <code>{all_links}</code>\n"
    #             f"• Allowed links: <code>{allowed_links}</code>\n"
    #             f"• Log channel: <code>{log_channel}</code>\n"
    #         )

    #         btn_name_row1 = ["Language", "Auto translate"]
    #         btn_data_row1 = ["lang", "auto_tr"]

    #         btn_name_row2 = ["Echo", "Anti bot"]
    #         btn_data_row2 = ["set_echo", "antibot"]

    #         btn_name_row3 = ["Welcome", "Goodbye"]
    #         btn_data_row3 = ["welcome_msg", "goodbye_msg"]

    #         btn_name_row4 = ["Delete cmd", "Log channel"]
    #         btn_data_row4 = ["del_cmd", "log_channel"]

    #         btn_name_row5 = ["Links", "AI"]
    #         btn_data_row5 = ["links_behave", "ai_status"]

    #         btn_name_row6 = ["query_close"]
    #         btn_data_row6 = ["query_close"]

    #         row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #         row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
    #         row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
    #         row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
    #         row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)
    #         row6 = await Button.cbutton(btn_name_row6, btn_data_row6)

    #         btn = row1 + row2 + row3 + row4 + row5 + row6

    #     elif data_to_find == "db_user_data":
    #         user_mention = find_chat.get("mention")
    #         lang = find_chat.get("lang")
    #         echo = find_chat.get("echo")
    #         auto_tr = find_chat.get("auto_tr")

    #         msg = (
    #             f"<u><b>Chat Settings</b></u>\n\n"
    #             f"• User: {user_mention}\n"
    #             f"• ID: <code>{user.id}</code>\n\n"

    #             f"• Lang: <code>{lang}</code>\n"
    #             f"• Echo: <code>{echo}</code>\n"
    #             f"• Auto tr: <code>{auto_tr}</code>\n\n"
    #         )

    #         btn_name_row1 = ["Language", "Auto translate"]
    #         btn_data_row1 = ["lang", "auto_tr"]

    #         btn_name_row2 = ["Echo", "query_close"]
    #         btn_data_row2 = ["set_echo", "query_close"]

    #         row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    #         row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

    #         btn = row1 + row2

    #     else:
    #         await query.message.delete()
    #         return
        
    #     await Message.edit_msg(update, msg, query.message, btn)
