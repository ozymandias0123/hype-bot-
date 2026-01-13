# Meme Coin Hype Tracker Bot

A Telegram bot that tracks meme coin hype on Twitter/X and performs sentiment analysis.

## Features

- 🔍 Search for token mentions on Twitter/X
- 📊 Sentiment analysis using VADER
- 🤖 Telegram bot interface

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/hype` | Show trending tokens ($DOGE, $SHIB, $PEPE) |
| `/token <name>` | Get stats for a specific token |

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install tweepy python-telegram-bot vaderSentiment
   ```
3. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
4. Run the bot:
   ```bash
   python love.py
   ```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `TWITTER_BEARER_TOKEN` | Twitter API Bearer Token |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token from @BotFather |

## License

MIT
