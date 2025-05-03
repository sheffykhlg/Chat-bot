from pyrogram import Client, filters
from pyrogram.types import Message

# Temporary dictionary to store replies
user_replies = {}

# /addreply command to add custom replies for keywords
@Client.on_message(filters.command("addreply") & filters.private)
async def add_reply(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Usage: `/addreply keyword | your reply here`", quote=True)

    try:
        keyword, reply = message.text.split(" | ", 1)
        user_replies[keyword.lower()] = reply
        await message.reply_text(f"✅ Reply for keyword '{keyword}' added successfully!", quote=True)
    except ValueError:
        await message.reply_text("❗ Please use the correct format: `/addreply keyword | your reply`", quote=True)

# /delreply command to delete replies for a keyword
@Client.on_message(filters.command("delreply") & filters.private)
async def del_reply(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Usage: `/delreply keyword`", quote=True)

    keyword = message.text.split(" ")[1].lower()
    if keyword in user_replies:
        del user_replies[keyword]
        await message.reply_text(f"🗑️ Reply for keyword '{keyword}' deleted.", quote=True)
    else:
        await message.reply_text(f"⚠️ No reply set for the keyword '{keyword}'", quote=True)

# /listreplies command to list all saved replies
@Client.on_message(filters.command("listreplies") & filters.private)
async def list_replies(client, message: Message):
    if user_replies:
        replies = "\n".join([f"🔑 {key} → {value}" for key, value in user_replies.items()])
        await message.reply_text(f"Here are your saved replies:\n{replies}", quote=True)
    else:
        await message.reply_text("❗ No replies set yet. Use /addreply to set some.", quote=True)

# Auto-reply based on keyword
@Client.on_message(filters.private)
async def auto_reply(client, message: Message):
    user_message = message.text.lower()
    for keyword, reply in user_replies.items():
        if keyword in user_message:
            await message.reply(reply)
            return
