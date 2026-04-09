from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions
import time

import db


# ==========================================================
# 🧠 Admin Check
# ==========================================================

async def is_admin(client, chat_id, user_id):
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


# ==========================================================
# 🔥 Register Function
# ==========================================================

def register_forcejoin(app):

    # ==========================================================
    # 🔧 Set Force Join
    # ==========================================================
    @app.on_message(filters.group & filters.command("forcejoin"))
    async def set_forcejoin(client, message: Message):

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
    @app.on_message(filters.group & filters.command("removeforcejoin"))
    async def remove_forcejoin(client, message: Message):

        if not await is_admin(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        await db.remove_force_channel(message.chat.id)

        await message.reply_text("⚠️ Force join disabled.")


    # ==========================================================
    # 🚨 Enforce Force Join
    # ==========================================================
    @app.on_message(filters.group & ~filters.service, group=0)
    async def check_forcejoin(client, message: Message):

        if not message.from_user:
            return

        user_id = message.from_user.id

        # Skip admins
        try:
            member = await client.get_chat_member(message.chat.id, user_id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        channel_id = await db.get_force_channel(message.chat.id)
        if not channel_id:
            return

        # Check join
        try:
            user = await client.get_chat_member(int(channel_id), user_id)
            if user.status in [
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER
            ]:
                return
        except:
            pass

        # Get channel
        try:
            chat = await client.get_chat(int(channel_id))
        except:
            return

        # Invite link
        if chat.username:
            invite_link = f"https://t.me/{chat.username}"
        else:
            try:
                invite = await client.create_chat_invite_link(chat.id)
                invite_link = invite.invite_link
            except:
                invite_link = "https://t.me"

        # 🔇 MUTE USER (5 minutes)
        until = int(time.time()) + 300

        try:
            await client.restrict_chat_member(
                message.chat.id,
                user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until
            )
        except:
            pass

        # ❌ Delete message
        try:
            await message.delete()
        except:
            pass

        # UI buttons
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Channel To Be Subscribed", url=invite_link)],
            [InlineKeyboardButton("🆗 I Subscribed", callback_data="check_sub")]
        ])

        text = f"""
🚫 {message.from_user.mention} to be accepted in the group, please subscribe to our channel.

Once joined, click the button below.

🔇 Action: Muted for 5 minutes.
"""

        try:
            await message.reply_text(text, reply_markup=buttons)
        except:
            pass


    # ==========================================================
    # 🔁 Recheck Button
    # ==========================================================
    @app.on_callback_query(filters.regex("check_sub"))
    async def check_subscribed(client, callback_query):

        user_id = callback_query.from_user.id
        chat_id = callback_query.message.chat.id

        channel_id = await db.get_force_channel(chat_id)
        if not channel_id:
            return await callback_query.answer("No force join set", show_alert=True)

        try:
            user = await client.get_chat_member(int(channel_id), user_id)

            if user.status in [
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER
            ]:

                # ✅ Unmute
                await client.restrict_chat_member(
                    chat_id,
                    user_id,
                    permissions=ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_add_web_page_previews=True,
                    ),
                )

                return await callback_query.answer("✅ You can chat now!", show_alert=True)

        except:
            pass

        await callback_query.answer("❌ You haven't joined yet!", show_alert=True)