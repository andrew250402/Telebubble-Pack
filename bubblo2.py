from telegram import Update, ChatMemberUpdated
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, ContextTypes, filters
import os

# Dictionary to store bubbles
bubbles = {}

# Fun and witty intro message
async def intro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    intro_message = (
        "🫧 Welcome to *Bubblo* – your ultimate telebubble companion, now with a fun twist! 🎉\n\n"
        "✨ Turn your favorite messages into reusable fun emotes that bring life to your chats!\n\n"
        "Here’s how you can use me:\n"
        "1️⃣ Reply to a bubble (message) and type /add <name> to save it.\n"
        "2️⃣ Use /list to see all saved bubble names.\n"
        "3️⃣ Use /delete <name> to remove a saved bubble.\n"
        "4️⃣ Use /send <name> to display the saved bubble in the chat.\n"
        "5️⃣ Simply type '<bubble_name>!!!!' in the chat to trigger a saved bubble automatically.\n\n"
        "Let’s make chatting fun and bubbly! 💬🫧"
    )
    await update.message.reply_text(intro_message, parse_mode="Markdown")

# /help command: Show available commands with a fun twist
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = (
        "🫧 *Here’s how Bubblo works!*\n\n"
        "✨ Save your favorite messages as ‘bubbles’ and reuse them as fun emotes in any chat! Here are my commands:\n"
        "• /add <name> - Reply to a message and save it as a bubble.\n"
        "• /list - View all your saved bubbles.\n"
        "• /delete <name> - Delete a bubble by name.\n"
        "• /send <name> - Display the saved bubble in the chat.\n\n"
        "🎉 *Magic with !!!!*\n"
        "If you type a bubble name followed by `!!!!` (e.g., `cringe!!!!`), Bubblo will automatically display the bubble for you! No need to type commands – it’s that easy! 🫧\n\n"
        "Let’s turn boring chats into fun and bubbly conversations! 🫧💬"
    )
    await update.message.reply_text(help_message, parse_mode="Markdown")

# /add command: Save a Telegram bubble
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.reply_to_message:
        await update.message.reply_text("🫧 You must reply to a message to save it as a bubble. Try again.")
        return

    # Extract the bubble name from the command
    try:
        bubble_name = context.args[0]
    except IndexError:
        await update.message.reply_text("🫧 Usage: /add <name>\nPlease provide a name for the bubble.")
        return

    # Check for duplicate names
    if bubble_name in bubbles:
        await update.message.reply_text(f"🫧 A bubble with the name '{bubble_name}' already exists. Try another name.")
        return

    # Save the bubble in the dictionary
    message = update.message.reply_to_message
    bubbles[bubble_name] = {"chat_id": message.chat_id, "message_id": message.message_id}
    await update.message.reply_text(f"🫧 '{bubble_name}' saved!")

# /list command: List all bubble names
async def list_bubbles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not bubbles:
        await update.message.reply_text("🫧 No bubbles saved yet. Use /add to start saving!")
        return

    bubble_names = "\n".join(bubbles.keys())
    await update.message.reply_text(f"🫧 Saved bubbles:\n{bubble_names}")

# /delete command: Delete a bubble by name
async def delete_bubble(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("🫧 Usage: /delete <name>")
        return

    bubble_name = context.args[0]
    if bubble_name not in bubbles:
        await update.message.reply_text(f"🫧 No bubble found with the name '{bubble_name}'.")
        return

    del bubbles[bubble_name]
    await update.message.reply_text(f"🫧 '{bubble_name}' deleted!")

# /send command: Forward the bubble associated with the given name
async def send_bubble(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("🫧 Usage: /send <name>")
        return

    bubble_name = context.args[0]
    bubble = bubbles.get(bubble_name)

    if not bubble:
        await update.message.reply_text(f"🫧 No bubble found with the name '{bubble_name}'.")
        return

    # Forward the original bubble to the chat
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=bubble["chat_id"],
        message_id=bubble["message_id"]
    )

# Detect messages and respond based on content
async def detect_loud_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text

    # Check for specific patterns
    if "!!!!" in message_text:
        # Extract the bubble name before "!!!!"
        bubble_name = message_text.replace("!!!!", "").strip()
        
        # If the bubble name exists, simulate /send command
        if bubble_name in bubbles:
            bubble = bubbles[bubble_name]
            await context.bot.forward_message(
                chat_id=update.effective_chat.id,
                from_chat_id=bubble["chat_id"],
                message_id=bubble["message_id"]
            )

# Trigger help when the bot is added to a group
async def on_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.my_chat_member.new_chat_member.status == "member":
        await intro(update, context)

# Main function to run the bot
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("list", list_bubbles))
    application.add_handler(CommandHandler("delete", delete_bubble))
    application.add_handler(CommandHandler("send", send_bubble))
    
    # Add a MessageHandler to detect specific patterns
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_loud_messages))
    
    # Add a ChatMemberHandler to detect when the bot is added to a group
    application.add_handler(ChatMemberHandler(on_bot_added, ChatMemberHandler.MY_CHAT_MEMBER))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
