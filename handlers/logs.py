from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from config import LOGS_GC


# ==========================================================
# 🔥 Register Logs
# ==========================================================

def register_logs(app: Client):

    # ======================================================
    # 🤖 START LOG (PRIVATE)
    # ======================================================
    @app.on_message(filters.private & filters.command("start"))
    async def start_log(client: Client, message: Message):

        user = message.from_user

        name = user.first_name
        username = f"@{user.username}" if user.username else "No Username"

        text = f"""
{name} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.

ᴜsᴇʀ ɪᴅ : {user.id}
ᴜsᴇʀɴᴀᴍᴇ : {username}
"""

        await client.send_message(LOGS_GC, text)


    # ======================================================
    # 👥 MEMBER UPDATE LOGS
    # ======================================================
    @app.on_chat_member_updated()
    async def member_logs(client: Client, cmu: ChatMemberUpdated):

        if not cmu.new_chat_member:
            return

        chat = cmu.chat
        user = cmu.new_chat_member.user
        old = cmu.old_chat_member.status if cmu.old_chat_member else None
        new = cmu.new_chat_member.status
        actor = cmu.from_user

        # ==================================================
        # ➕ USER JOIN / ADD
        # ==================================================
        if old in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED] and new == ChatMemberStatus.MEMBER:

            if not actor or actor.id == user.id:
                text = f"""
➕ ᴜsᴇʀ ᴊᴏɪɴᴇᴅ

👤 {user.mention}
🆔 {user.id}

📥 ᴊᴏɪɴᴇᴅ ᴠɪᴀ ʟɪɴᴋ
🏠 {chat.title}
"""
            else:
                text = f"""
➕ ᴜsᴇʀ ᴀᴅᴅᴇᴅ

👤 {user.mention}
🆔 {user.id}

👮 ᴀᴅᴅᴇᴅ ʙʏ: {actor.mention}
🆔 {actor.id}

🏠 {chat.title}
"""

            await client.send_message(LOGS_GC, text)


        # ==================================================
        # 👋 USER LEFT
        # ==================================================
        elif old == ChatMemberStatus.MEMBER and new == ChatMemberStatus.LEFT:

            text = f"""
👋 ᴜsᴇʀ ʟᴇғᴛ

👤 {user.mention}
🆔 {user.id}

🏠 {chat.title}
"""
            await client.send_message(LOGS_GC, text)


        # ==================================================
        # 🚫 USER BANNED / KICKED
        # ==================================================
        elif new == ChatMemberStatus.BANNED:

            if actor and actor.id != user.id:
                text = f"""
🚫 ᴜsᴇʀ ʙᴀɴɴᴇᴅ

👤 {user.mention}
🆔 {user.id}

👮 ʙʏ: {actor.mention}
🆔 {actor.id}

🏠 {chat.title}
"""
            else:
                text = f"""
🚫 ᴜsᴇʀ ʀᴇᴍᴏᴠᴇᴅ

👤 {user.mention}
🆔 {user.id}

🏠 {chat.title}
"""

            await client.send_message(LOGS_GC, text)


    # ======================================================
    # 🤖 BOT ADDED IN GROUP
    # ======================================================
    @app.on_message(filters.new_chat_members)
    async def bot_added(client: Client, message: Message):

        if client.me.id not in [u.id for u in message.new_chat_members]:
            return

        chat = message.chat
        user = message.from_user

        text = f"""
✫ ɴᴇᴡ ɢʀᴏᴜᴘ

🆔 {chat.id}
📛 {chat.title}
🔗 @{chat.username if chat.username else "Private"}

➕ ᴀᴅᴅᴇᴅ ʙʏ: {user.mention if user else "Unknown"}
"""

        await client.send_message(LOGS_GC, text)


    # ======================================================
    # ❌ BOT REMOVED FROM GROUP
    # ======================================================
    @app.on_message(filters.left_chat_member)
    async def bot_removed(client: Client, message: Message):

        if message.left_chat_member.id != client.me.id:
            return

        chat = message.chat
        user = message.from_user

        text = f"""
✫ ʟᴇғᴛ ɢʀᴏᴜᴘ

🆔 {chat.id}
📛 {chat.title}

❌ ʀᴇᴍᴏᴠᴇᴅ ʙʏ: {user.mention if user else "Unknown"}
"""

        await client.send_message(LOGS_GC, text)