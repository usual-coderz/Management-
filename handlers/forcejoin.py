from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.enums import ChatMemberStatus
import asyncio
import db


# ==========================================================
# 🧠 Admin Check
# ==========================================================

async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False


# ==========================================================
# 🔥 Register Function
# ==========================================================

def register_forcejoin(app):

    # ==========================================================
    # 🚨 Enforce Force Join
    # ==========================================================
    @app.on_message(filters.group & ~filters.service, group=0)
    async def check_forcejoin(client, message: Message):

        if not message.from_user:
            return

        user_id = message.from_user.id

        # Skip admins
        if await is_admin(client, message.chat.id, user_id):
            return

        channel_id = await db.get_force_channel(message.chat.id)
        if not channel_id:
            return

        # Check already joined
        try:
            member = await client.get_chat_member(int(channel_id), user_id)
            if member.status in [
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

        # 🔇 MUTE USER
        try:
            await client.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                )
            )
        except Exception as e:
            print("MUTE ERROR:", e)

        # ❌ Delete user message
        try:
            await message.delete()
        except:
            pass

        # 🔘 Button UI
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔔 Join", url=invite_link)]
        ])

        text = f"""
{message.from_user.mention},You have to join this channel So you are able to message here.
"""

        # Send message
        sent = await client.send_message(
            message.chat.id,
            text,
            reply_markup=buttons
        )

        # ======================================================
        # ⏳ AUTO DELETE AFTER 45 SEC
        # ======================================================
        async def auto_delete():
            await asyncio.sleep(45)
            try:
                await sent.delete()
            except:
                pass

        app.loop.create_task(auto_delete())

        # ======================================================
        # 🤖 AUTO VERIFY LOOP
        # ======================================================
        async def auto_verify():
            for _ in range(15):  # check every 3 sec (total ~45 sec)
                await asyncio.sleep(3)

                try:
                    member = await client.get_chat_member(int(channel_id), user_id)

                    if member.status in [
                        ChatMemberStatus.MEMBER,
                        ChatMemberStatus.ADMINISTRATOR,
                        ChatMemberStatus.OWNER
                    ]:
                        # ✅ UNMUTE
                        await client.restrict_chat_member(
                            message.chat.id,
                            user_id,
                            permissions=ChatPermissions(
                                can_send_messages=True,
                                can_send_media_messages=True,
                                can_send_other_messages=True,
                                can_add_web_page_previews=True,
                            ),
                        )

                        try:
                            await sent.delete()
                        except:
                            pass

                        break

                except:
                    continue

        app.loop.create_task(auto_verify())