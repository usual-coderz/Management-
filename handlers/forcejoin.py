from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus

import db


# ==========================================================
# 🧠 Admin Check
# ==========================================================

async def is_admin(client, chat_id, user_id):
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


# ==========================================================
# 🔧 Set Force Join
# ==========================================================

@Client.on_message(filters.group & filters.command("forcejoin"))
async def set_forcejoin(client: Client, message: Message):

    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Only admin can use this command.")

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply_text(
            "⚙️ Usage:\n/forcejoin @channelusername OR channel_id"
        )

    try:
        chat = await client.get_chat(parts[1])
    except Exception as e:
        return await message.reply_text(f"❌ Invalid channel: {e}")

    await db.set_force_channel(message.chat.id, str(chat.id))

    await message.reply_text(
        f"✅ Force join enabled for **{chat.title}**"
    )


# ==========================================================
# ❌ Remove Force Join
# ==========================================================

@Client.on_message(filters.group & filters.command("removeforcejoin"))
async def remove_forcejoin(client: Client, message: Message):

    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Only admin can use this command.")

    await db.remove_force_channel(message.chat.id)

    await message.reply_text("⚠️ Force join disabled.")


# ==========================================================
# 🚨 Enforce Force Join
# ==========================================================

@Client.on_message(filters.group & ~filters.service, group=0)
async def check_forcejoin(client: Client, message: Message):

    if not message.from_user:
        return

    # Skip admins
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return
    except:
        return

    channel_id = await db.get_force_channel(message.chat.id)
    if not channel_id:
        return

    try:
        user = await client.get_chat_member(int(channel_id), message.from_user.id)

        if user.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ]:
            return

    except:
        pass

    # Get channel info
    try:
        chat = await client.get_chat(int(channel_id))
    except:
        return

    # Generate invite link
    invite_link = None

    if chat.username:
        invite_link = f"https://t.me/{chat.username}"
    else:
        try:
            invite = await client.create_chat_invite_link(chat.id)
            invite_link = invite.invite_link
        except:
            invite_link = "https://t.me"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Join Channel", url=invite_link)]
    ])

    try:
        await message.reply_text(
            f"🚫 **Join Required!**\n\n👉 Please join **{chat.title}** to chat here.",
            reply_markup=buttons
        )
        await message.delete()
    except:
        pass