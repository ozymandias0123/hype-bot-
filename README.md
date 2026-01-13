# Hype Bot 🚀

A Telegram bot that tracks meme coin hype on Twitter/X and performs sentiment analysis using natural language processing.

## Features

- 📊 **Real-time Sentiment Analysis**: Analyzes tweets about meme coins to determine market sentiment
- 🔍 **Twitter/X Integration**: Searches and monitors recent tweets about specified coins
- 🤖 **Telegram Bot Interface**: Easy-to-use commands for tracking and analyzing coins
- 📈 **Sentiment Metrics**: Provides detailed sentiment breakdown (positive/negative/neutral)
- 🎯 **Multi-coin Tracking**: Track multiple meme coins simultaneously
- 📱 **Instant Analysis**: Get on-demand sentiment reports for any coin

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Twitter/X API credentials (from [Twitter Developer Portal](https://developer.twitter.com/))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ozymandias0123/hype-bot-.git
cd hype-bot-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file with your API credentials:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
```

## Configuration

### Getting API Keys

#### Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided

#### Twitter/X API Keys
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new project and app
3. Generate Bearer Token
4. Copy credentials to `.env` file

### Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (required)
- `TWITTER_BEARER_TOKEN`: Twitter API bearer token (required)
- `TWITTER_API_KEY`: Twitter API key (optional)
- `TWITTER_API_SECRET`: Twitter API secret (optional)
- `TWITTER_ACCESS_TOKEN`: Twitter access token (optional)
- `TWITTER_ACCESS_SECRET`: Twitter access token secret (optional)
- `UPDATE_INTERVAL`: Update interval in seconds (default: 300)
- `MAX_TWEETS_PER_UPDATE`: Maximum tweets to analyze (default: 10)

## Usage

### Starting the Bot

Run the bot with:
```bash
python bot.py
```

### Bot Commands

- `/start` - Welcome message and quick start guide
- `/help` - Show all available commands and usage
- `/track <symbol> [name]` - Start tracking a meme coin
- `/stop <symbol>` - Stop tracking a coin
- `/check <symbol> [name]` - Get instant sentiment analysis
- `/list` - Show all tracked coins

### Examples

Track Dogecoin:
```
/track DOGE Dogecoin
```

Get instant analysis for Shiba Inu:
```
/check SHIB Shiba Inu
```

Stop tracking a coin:
```
/stop DOGE
```

List all tracked coins:
```
/list
```

## Sentiment Analysis

The bot uses TextBlob for sentiment analysis, which provides:

- **Polarity Score**: Ranges from -1 (very negative) to +1 (very positive)
- **Sentiment Categories**: 
  - 🚀 Very Positive (> 0.5)
  - 😊 Positive (0.1 to 0.5)
  - 😐 Neutral (-0.1 to 0.1)
  - 😟 Negative (-0.5 to -0.1)
  - 📉 Very Negative (< -0.5)

## Project Structure

```
hype-bot-/
├── bot.py                  # Main Telegram bot application
├── coin_tracker.py         # Coin tracking and coordination logic
├── twitter_client.py       # Twitter/X API client
├── sentiment_analyzer.py   # Sentiment analysis module
├── config.py              # Configuration and environment loading
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## How It Works

1. **User Interaction**: Users send commands to the Telegram bot
2. **Twitter Search**: Bot searches Twitter/X for recent tweets about the specified coin
3. **Sentiment Analysis**: Each tweet is analyzed for sentiment using TextBlob NLP
4. **Aggregation**: Sentiments are aggregated to provide overall statistics
5. **Report**: Formatted report is sent back to the user via Telegram

## Limitations

- Twitter API free tier has rate limits (check Twitter's documentation)
- Sentiment analysis is based on text only (doesn't consider context or sarcasm)
- Only analyzes recent tweets (last 7 days for Twitter API v2)
- Requires active internet connection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This bot is for informational purposes only. It does not provide financial advice. Always do your own research before making investment decisions.
