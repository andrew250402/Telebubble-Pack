from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Dictionary to store bubbles
bubbles = {}

# Intro message for any general input
async def intro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    intro_message = (
        "Welcome to Bubblo, your personal bubble sticker pack! 🎉\n\n"
        "Here’s how you can use me:\n"
        "1. Reply to a bubble (message) and type /add <name> to save it.\n"
        "2. Use /list to see all saved bubble names.\n"
        "3. Use /delete <name> to remove a saved bubble.\n"
        "4. Use /show <name> to display the saved bubble in the chat.\n\n"
        "Try typing /help to see all commands!"
    )
    await update.message.reply_text(intro_message)

# /help command: Show available commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = (
        "Here are the available commands:\n"
        "/add - Reply to a message and use /add <name> to save it as a bubble.\n"
        "/list - List all saved bubbles.\n"
        "/delete <name> - Delete a bubble by name.\n"
        "/show <name> - Display the bubble associated with the given name.\n"
    )
    await update.message.reply_text(help_message)

# /add command: Save a Telegram bubble
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.reply_to_message:
        await update.message.reply_text("You must reply to a message to save it as a bubble. Try again.")
        return

    # Extract the bubble name from the command
    try:
        bubble_name = context.args[0]
    except IndexError:
        await update.message.reply_text("Usage: /add <name>\nPlease provide a name for the bubble.")
        return

    # Check for duplicate names
    if bubble_name in bubbles:
        await update.message.reply_text(f"A bubble with the name '{bubble_name}' already exists. Try another name.")
        return

    # Save the bubble in the dictionary
    message = update.message.reply_to_message
    bubbles[bubble_name] = {"chat_id": message.chat_id, "message_id": message.message_id}
    await update.message.reply_text(f"'{bubble_name}' saved!")

# /list command: List all bubble names
async def list_bubbles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not bubbles:
        await update.message.reply_text("No bubbles saved yet. Use /add to start saving!")
        return

    bubble_names = "\n".join(bubbles.keys())
    await update.message.reply_text(f"Saved bubbles:\n{bubble_names}")

# /delete command: Delete a bubble by name
async def delete_bubble(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /delete <name>")
        return

    bubble_name = context.args[0]
    if bubble_name not in bubbles:
        await update.message.reply_text(f"No bubble found with the name '{bubble_name}'.")
        return

    del bubbles[bubble_name]
    await update.message.reply_text(f"'{bubble_name}' deleted!")

# /show command: Forward the bubble associated with the given name
async def show_bubble(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /show <name>")
        return

    bubble_name = context.args[0]
    bubble = bubbles.get(bubble_name)

    if not bubble:
        await update.message.reply_text(f"No bubble found with the name '{bubble_name}'.")
        return

    # Forward the original bubble to the chat
    await context.bot.forward_message(
        chat_id=update.effective_chat.id,
        from_chat_id=bubble["chat_id"],
        message_id=bubble["message_id"]
    )

# Main function to run the bot
def main():
    TOKEN = "7958290781:AAGQJwxheRBuD9iRp9H9Qj2t8y0FaCFKaDI"
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("list", list_bubbles))
    application.add_handler(CommandHandler("delete", delete_bubble))
    application.add_handler(CommandHandler("show", show_bubble))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, intro))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
