# Quick Start Guide

## 1. Get API Credentials

### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token provided

### Twitter API (Required)
1. Visit https://developer.twitter.com/
2. Sign up for a developer account
3. Create a new App in the Developer Portal
4. Go to "Keys and tokens" tab
5. Copy your "Bearer Token"

## 2. Setup

```bash
# Clone the repository
git clone https://github.com/ozymandias0123/hype-bot-.git
cd hype-bot-

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your credentials
nano .env
```

## 3. Configure .env

Minimum required configuration:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAABearerToken...
```

## 4. Run the Bot

```bash
python bot.py
```

You should see:
```
INFO - Starting Hype Bot...
```

## 5. Use the Bot

1. Open Telegram and search for your bot
2. Start a chat with your bot
3. Send `/start` to see available commands
4. Try tracking a coin: `/track DOGE Dogecoin`

## Common Commands

- `/track DOGE` - Track Dogecoin
- `/check SHIB Shiba Inu` - Get instant sentiment analysis
- `/list` - See all tracked coins
- `/stop DOGE` - Stop tracking Dogecoin

## Troubleshooting

### "Missing required environment variables"
- Make sure `.env` file exists
- Verify TELEGRAM_BOT_TOKEN and TWITTER_BEARER_TOKEN are set
- Check there are no extra spaces or quotes

### "Connection error" or "Rate limit"
- Check your internet connection
- Verify Twitter API credentials are correct
- You may have hit Twitter API rate limits (wait 15 minutes)

### Bot doesn't respond
- Verify the bot is running (`python bot.py`)
- Check Telegram bot token is correct
- Make sure bot is not blocked

## Running as a Service (Optional)

### Using systemd (Linux)

Create `/etc/systemd/system/hype-bot.service`:

```ini
[Unit]
Description=Hype Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/hype-bot-
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /path/to/hype-bot-/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable hype-bot
sudo systemctl start hype-bot
sudo systemctl status hype-bot
```

### Using screen (Simple)

```bash
screen -S hype-bot
python bot.py
# Press Ctrl+A then D to detach
# Reattach with: screen -r hype-bot
```

## Next Steps

- Customize `UPDATE_INTERVAL` in `.env` for different update frequencies
- Adjust `MAX_TWEETS_PER_UPDATE` to analyze more or fewer tweets
- Check Twitter API documentation for advanced query options
