from pyrogram import Client, filters, idle
from pyrogram.types import Message
from config import Config

# Config file se credentials le rahe hain
api_id = Config.API_ID
api_hash = Config.API_HASH
bot_token = Config.BOT_TOKEN

# Pyrogram Client create kar rahe hain
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Yahan hum replies temporarily save kar rahe hain
user_replies = {}

# Start command pe simple reply karega
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply("Hello! I am your bot. How can I assist you?")

# Command: /addreply keyword | reply
@app.on_message(filters.command("addreply") & filters.private)
async def add_reply(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Usage: `/addreply keyword | your reply here`", quote=True)
    try:
        keyword, reply = message.text.split(" | ", 1)
        user_replies[keyword.lower()] = reply
        await message.reply_text(f"✅ Reply for keyword '{keyword}' added successfully!", quote=True)
    except ValueError:
        await message.reply_text("❗ Please use the correct format: `/addreply keyword | your reply`", quote=True)

# Command: /delreply keyword
@app.on_message(filters.command("delreply") & filters.private)
async def del_reply(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Usage: `/delreply keyword`", quote=True)

    keyword = message.text.split(" ")[1].lower()
    if keyword in user_replies:
        del user_replies[keyword]
        await message.reply_text(f"🗑️ Reply for keyword '{keyword}' deleted.", quote=True)
    else:
        await message.reply_text(f"⚠️ No reply set for the keyword '{keyword}'", quote=True)

# Command: /listreplies
@app.on_message(filters.command("listreplies") & filters.private)
async def list_replies(client, message: Message):
    if user_replies:
        replies = "\n".join([f"🔑 {key} → {value}" for key, value in user_replies.items()])
        await message.reply_text(f"Here are your saved replies:\n{replies}", quote=True)
    else:
        await message.reply_text("❗ No replies set yet. Use /addreply to set some.", quote=True)

# Auto reply jab bhi koi message aaye jisme keyword ho
@app.on_message(filters.private)
async def auto_reply(client, message: Message):
    user_message = message.text.lower()
    for keyword, reply in user_replies.items():
        if keyword in user_message:
            await message.reply(reply)
            return

# Bot start karte hain
print("Bot started...")
app.run()
