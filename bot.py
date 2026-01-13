"""
Telegram bot for tracking meme coin hype and sentiment.
"""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from telegram.constants import ParseMode
import config
from coin_tracker import CoinTracker

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize coin tracker
tracker = CoinTracker()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    welcome_message = """
🤖 *Welcome to Hype Bot!*

I track meme coin hype on Twitter/X and analyze sentiment.

*Available Commands:*
/track <symbol> [name] - Track a coin (e.g., /track DOGE Dogecoin)
/stop <symbol> - Stop tracking a coin
/check <symbol> [name] - Get instant analysis
/list - Show tracked coins
/help - Show this help message

Example:
`/track DOGE Dogecoin`
`/check SHIB Shiba Inu`
    """
    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    help_text = """
*Hype Bot Help* 🚀

*Commands:*
• /track <symbol> [name] - Start tracking a meme coin
• /stop <symbol> - Stop tracking a coin
• /check <symbol> [name] - Get instant sentiment analysis
• /list - Show all tracked coins
• /help - Show this help message

*Examples:*
`/track DOGE` - Track Dogecoin
`/track SHIB Shiba Inu` - Track with full name
`/check PEPE` - Get instant analysis
`/stop DOGE` - Stop tracking Dogecoin

*About Sentiment Analysis:*
🚀 Very Positive
😊 Positive
😐 Neutral
😟 Negative
📉 Very Negative

The bot analyzes recent tweets to determine overall sentiment.
    """
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


async def track_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /track command."""
    chat_id = update.effective_chat.id
    
    if not context.args:
        await update.message.reply_text(
            "Please provide a coin symbol.\nExample: `/track DOGE Dogecoin`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    coin_symbol = context.args[0].upper()
    coin_name = ' '.join(context.args[1:]) if len(context.args) > 1 else None
    
    # Add coin to tracking
    tracker.add_coin(chat_id, coin_symbol, coin_name)
    
    # Send initial analysis
    await update.message.reply_text(
        f"🎯 Now tracking ${coin_symbol}!\n\nFetching initial analysis...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Get and send analysis
    analysis = tracker.analyze_coin(coin_symbol, coin_name)
    message = tracker.format_analysis_message(analysis)
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /stop command."""
    chat_id = update.effective_chat.id
    
    if not context.args:
        await update.message.reply_text(
            "Please provide a coin symbol.\nExample: `/stop DOGE`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    coin_symbol = context.args[0].upper()
    
    if tracker.remove_coin(chat_id, coin_symbol):
        await update.message.reply_text(
            f"✅ Stopped tracking ${coin_symbol}",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            f"❌ ${coin_symbol} was not being tracked",
            parse_mode=ParseMode.MARKDOWN
        )


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /check command for instant analysis."""
    if not context.args:
        await update.message.reply_text(
            "Please provide a coin symbol.\nExample: `/check DOGE Dogecoin`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    coin_symbol = context.args[0].upper()
    coin_name = ' '.join(context.args[1:]) if len(context.args) > 1 else None
    
    await update.message.reply_text(
        f"🔍 Analyzing ${coin_symbol}...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    analysis = tracker.analyze_coin(coin_symbol, coin_name)
    message = tracker.format_analysis_message(analysis)
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /list command."""
    chat_id = update.effective_chat.id
    coins = tracker.get_tracked_coins(chat_id)
    
    if not coins:
        await update.message.reply_text(
            "📭 You're not tracking any coins yet.\n\nUse `/track <symbol>` to start!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    message = "📋 *Tracked Coins:*\n\n"
    for coin in coins:
        symbol = coin['symbol']
        name = coin['name']
        if name:
            message += f"• ${symbol} ({name})\n"
        else:
            message += f"• ${symbol}\n"
    
    message += f"\n_Total: {len(coins)} coins_"
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Start the bot."""
    # Validate configuration
    try:
        config.validate_config()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please set up your .env file with required API keys.")
        return
    
    # Create application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("track", track_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(CommandHandler("check", check_command))
    application.add_handler(CommandHandler("list", list_command))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting Hype Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
