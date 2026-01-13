import os
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import tweepy
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ================== API Keys ==================
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "your_twitter_bearer_token_here")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token_here")
# ==============================================

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize clients
twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
sentiment_analyzer = SentimentIntensityAnalyzer()
executor = ThreadPoolExecutor(max_workers=2)

# Sentiment analysis
def get_sentiment(text):
    try:
        return sentiment_analyzer.polarity_scores(text)['compound']
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        return 0

# Check Twitter hype
async def get_twitter_hype(token):
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            executor,
            lambda: twitter_client.search_recent_tweets(
                query=f"{token} lang:en -is:retweet",
                max_results=10,
                tweet_fields=["text"]
            )
        )
        tweets = response.data or []
        mentions = len(tweets)
        positive = sum(1 for tweet in tweets if tweet.text and get_sentiment(tweet.text) > 0)
        logger.info(f"Twitter data for {token}: {mentions} mentions, {positive}% positive")
        return mentions, positive / mentions * 100 if mentions > 0 else 0
    except tweepy.RateLimitError:
        logger.warning("Twitter API rate limit reached, waiting 15 minutes...")
        await asyncio.sleep(15 * 60)
        return await get_twitter_hype(token)
    except tweepy.TweepyException as e:
        logger.error(f"Twitter API error: {e}")
        return 0, 0
    except Exception as e:
        logger.error(f"Twitter general error: {e}")
        return 0, 0

# Telegram bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Meme Coin Hype Tracker! Use /hype or /token [name].")

async def hype(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tokens = ["$DOGE", "$SHIB", "$PEPE"]
    result = "🔥 Trending Tokens 🔥\n"
    for token in tokens:
        mentions, positive = await get_twitter_hype(token)
        result += f"{token}: {mentions} X mentions, {positive:.1f}% positive\n"
    await update.message.reply_text(result)

async def token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /token <token_name>")
        return
    token = context.args[0]
    mentions, positive = await get_twitter_hype(token)
    await update.message.reply_text(
        f"{token} Stats:\nX Mentions: {mentions}\nPositive: {positive:.1f}%"
    )

# Main function
async def main():
    logger.info("Bot starting...")
    app = None
    try:
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("hype", hype))
        app.add_handler(CommandHandler("token", token))
        logger.info("Bot is running...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        if app:
            try:
                if app.updater:
                    await app.updater.stop()
                await app.stop()
                await app.shutdown()
                logger.info("Bot shut down")
            except Exception as e:
                logger.error(f"Bot shutdown error: {e}")

if __name__ == "__main__":
    asyncio.run(main())