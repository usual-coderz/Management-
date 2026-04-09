from pyrogram import filters
from pyrogram.types import ChatMemberUpdated, Message
from pyrogram.enums import ChatMemberStatus
from config import LOGS_GC


# ==========================================================
# 🔥 Register Logs
# ==========================================================

def register_logs(app):

    # ======================================================
    # 👥 Member Updates Logs
    # ======================================================
    @app.on_chat_member_updated()
    async def member_logs(client, cmu: ChatMemberUpdated):

        if not cmu.new_chat_member:
            return

        chat = cmu.chat
        user = cmu.new_chat_member.user
        old = cmu.old_chat_member.status if cmu.old_chat_member else None
        new = cmu.new_chat_member.status
        actor = cmu.from_user

        # ==================================================
        # ➕ User Joined / Added
        # ==================================================
        if old in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED] and new == ChatMemberStatus.MEMBER:

            if not actor or actor.id == user.id:
                text = f"""
➕ **User Joined**

👤 {user.mention}
🆔 `{user.id}`

📥 Self joined / link
🏠 Chat: {chat.title}
🆔 `{chat.id}`
"""
            else:
                text = f"""
➕ **User Added**

👤 {user.mention}
🆔 `{user.id}`

👮 Added by: {actor.mention}
🆔 `{actor.id}`

🏠 Chat: {chat.title}
"""

            await client.send_message(LOGS_GC, text)


        # ==================================================
        # 👋 User Left
        # ==================================================
        elif old == ChatMemberStatus.MEMBER and new == ChatMemberStatus.LEFT:

            text = f"""
👋 **User Left**

👤 {user.mention}
🆔 `{user.id}`

🏠 Chat: {chat.title}
"""
            await client.send_message(LOGS_GC, text)


        # ==================================================
        # 🚫 User Kicked / Banned
        # ==================================================
        elif new == ChatMemberStatus.BANNED:

            if actor and actor.id != user.id:
                text = f"""
🚫 **User Kicked / Banned**

👤 {user.mention}
🆔 `{user.id}`

👮 By: {actor.mention}
🆔 `{actor.id}`

🏠 Chat: {chat.title}
"""
            else:
                text = f"""
🚫 **User Removed**

👤 {user.mention}
🆔 `{user.id}`

🏠 Chat: {chat.title}
"""

            await client.send_message(LOGS_GC, text)


    # ======================================================
    # 🤖 Start Logs (Private)
    # ======================================================
    @app.on_message(filters.private & filters.command("start"))
    async def start_log(client, message: Message):

        user = message.from_user

        text = f"""
🤖 **Bot Started**

👤 {user.mention}
🆔 `{user.id}`

📛 Name: {user.first_name}
"""

        await client.send_message(LOGS_GC, text)