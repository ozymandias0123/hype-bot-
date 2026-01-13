# Example Usage

## Bot Conversation Examples

### Starting the Bot

```
User: /start

Bot: 🤖 Welcome to Hype Bot!

I track meme coin hype on Twitter/X and analyze sentiment.

Available Commands:
/track <symbol> [name] - Track a coin (e.g., /track DOGE Dogecoin)
/stop <symbol> - Stop tracking a coin
/check <symbol> [name] - Get instant analysis
/list - Show tracked coins
/help - Show this help message

Example:
/track DOGE Dogecoin
/check SHIB Shiba Inu
```

### Tracking a Coin

```
User: /track DOGE Dogecoin

Bot: 🎯 Now tracking $DOGE!

Fetching initial analysis...

📊 $DOGE (Dogecoin) 🚀

Sentiment Analysis (10 tweets)
Overall: POSITIVE (0.42)

✅ Positive: 7
😐 Neutral: 2
❌ Negative: 1

Recent Tweets:
1. 🚀 DOGE to the moon! Bullish AF! This is going to explode! #Dogecoin $DOGE
   👤 @cryptotrader ❤️ 245 🔄 89

2. 😊 $DOGE holding strong at support levels. Looking good for a bounce...
   👤 @chartmaster ❤️ 156 🔄 34

3. 😊 Just bought more $DOGE. The community is amazing! #ToTheMoon
   👤 @hodler4life ❤️ 99 🔄 25
```

### Checking Another Coin

```
User: /check SHIB Shiba Inu

Bot: 🔍 Analyzing $SHIB...

📊 $SHIB (Shiba Inu) 😐

Sentiment Analysis (10 tweets)
Overall: NEUTRAL (0.05)

✅ Positive: 4
😐 Neutral: 4
❌ Negative: 2

Recent Tweets:
1. 😊 $SHIB forming a nice pattern on the 4h chart. Could see a breakout soon...
   👤 @techanalyst ❤️ 178 🔄 45

2. 😐 $SHIB volume is low today. Not much happening in the market right now.
   👤 @cryptonews ❤️ 67 🔄 12

3. 😟 $SHIB losing momentum. Might be time to take some profits here...
   👤 @daytrader ❤️ 89 🔄 23
```

### Listing Tracked Coins

```
User: /list

Bot: 📋 Tracked Coins:

• $DOGE (Dogecoin)
• $SHIB (Shiba Inu)
• $PEPE

Total: 3 coins
```

### Stopping Tracking

```
User: /stop SHIB

Bot: ✅ Stopped tracking $SHIB
```

### When No Tweets Found

```
User: /check NEWCOIN

Bot: 🔍 Analyzing $NEWCOIN...

No recent activity found for NEWCOIN
```

## Sentiment Indicators Explained

The bot uses emojis to quickly convey sentiment:

- 🚀 **Very Positive** (polarity > 0.5): Strong bullish sentiment, lots of excitement
- 😊 **Positive** (polarity 0.1 to 0.5): Generally positive, optimistic outlook
- 😐 **Neutral** (polarity -0.1 to 0.1): Mixed or neutral sentiment, no clear direction
- 😟 **Negative** (polarity -0.5 to -0.1): Somewhat bearish, concerns present
- 📉 **Very Negative** (polarity < -0.5): Strong bearish sentiment, major concerns

## Sample Sentiment Scores

### Positive Tweets
```
"This coin is absolutely amazing! To the moon! 🚀🚀🚀"
Polarity: 0.85 → 🚀 Very Positive

"Looking good today, nice steady growth"
Polarity: 0.35 → 😊 Positive
```

### Neutral Tweets
```
"The price is $0.0001 right now"
Polarity: 0.0 → 😐 Neutral

"Volume increased by 10% today"
Polarity: 0.05 → 😐 Neutral
```

### Negative Tweets
```
"Not looking great, might dump soon"
Polarity: -0.25 → 😟 Negative

"This is a disaster, total rugpull! SCAM!"
Polarity: -0.75 → 📉 Very Negative
```

## Pro Tips

1. **Track popular coins** like DOGE, SHIB, PEPE for best results
2. **Use full names** for better search results: `/track DOGE Dogecoin`
3. **Check regularly** - sentiment can change quickly
4. **Compare multiple coins** to see relative market sentiment
5. **Look at tweet volume** - more tweets = more reliable sentiment

## Note on Accuracy

- Sentiment analysis is based on text content only
- Does not detect sarcasm or complex context
- Best used as one indicator among many
- Always do your own research (DYOR)
- Not financial advice!
