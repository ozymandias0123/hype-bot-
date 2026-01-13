# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Telegram User                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Commands (/track, /check, /list)
                     ▼
┌─────────────────────────────────────────────────────────┐
│                     bot.py                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Command Handlers                                  │  │
│  │  - start_command()                                 │  │
│  │  - track_command()                                 │  │
│  │  - check_command()                                 │  │
│  │  - list_command()                                  │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Delegates to
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 coin_tracker.py                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  CoinTracker                                       │  │
│  │  - add_coin()                                      │  │
│  │  - remove_coin()                                   │  │
│  │  - analyze_coin()                                  │  │
│  │  - format_analysis_message()                       │  │
│  └───────────────────────────────────────────────────┘  │
└──────────┬──────────────────────────────┬───────────────┘
           │                              │
           │ Uses                         │ Uses
           ▼                              ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│   twitter_client.py     │   │  sentiment_analyzer.py  │
│  ┌───────────────────┐  │   │  ┌───────────────────┐  │
│  │ TwitterClient     │  │   │  │ SentimentAnalyzer │  │
│  │ - search_tweets() │  │   │  │ - analyze()       │  │
│  │ - build_query()   │  │   │  │ - categorize()    │  │
│  └───────────────────┘  │   │  │ - aggregate()     │  │
└─────────┬───────────────┘   │  └───────────────────┘  │
          │                   └─────────────────────────┘
          │
          │ Calls
          ▼
┌─────────────────────────┐
│   Twitter/X API         │
│   (tweepy client)       │
└─────────────────────────┘
```

## Module Descriptions

### bot.py
**Purpose**: Main entry point for the Telegram bot

**Responsibilities**:
- Initialize Telegram bot application
- Register command handlers
- Handle user interactions
- Format and send responses to users
- Error handling and logging

**Key Functions**:
- `start_command()`: Welcome message and onboarding
- `track_command()`: Start tracking a coin
- `check_command()`: Get instant sentiment analysis
- `list_command()`: Show tracked coins
- `stop_command()`: Stop tracking a coin

### coin_tracker.py
**Purpose**: Coordinate coin tracking and sentiment analysis

**Responsibilities**:
- Manage tracked coins per chat/user
- Coordinate between Twitter client and sentiment analyzer
- Format analysis results into user-friendly messages
- Handle multiple users/chats

**Key Functions**:
- `add_coin()`: Add a coin to tracking list
- `remove_coin()`: Remove a coin from tracking
- `analyze_coin()`: Get tweets and analyze sentiment
- `format_analysis_message()`: Format results for display

### twitter_client.py
**Purpose**: Interface with Twitter/X API

**Responsibilities**:
- Search for recent tweets about coins
- Build search queries for optimal results
- Handle Twitter API authentication
- Parse and structure tweet data
- Handle rate limiting

**Key Functions**:
- `search_recent_tweets()`: Search for tweets matching query
- `build_coin_query()`: Build optimized search query for a coin

**Dependencies**:
- tweepy: Twitter API client library

### sentiment_analyzer.py
**Purpose**: Analyze sentiment of text content

**Responsibilities**:
- Analyze individual tweets for sentiment
- Categorize sentiment (positive/negative/neutral)
- Aggregate multiple sentiments
- Provide emoji representations

**Key Functions**:
- `analyze()`: Analyze text sentiment (polarity & subjectivity)
- `categorize_sentiment()`: Convert polarity to category
- `get_sentiment_emoji()`: Get emoji for sentiment
- `aggregate_sentiment()`: Combine multiple sentiment scores

**Dependencies**:
- textblob: Natural language processing library

### config.py
**Purpose**: Configuration management

**Responsibilities**:
- Load environment variables
- Validate required configuration
- Provide configuration constants

**Key Variables**:
- API tokens and credentials
- Bot behavior settings (update intervals, tweet limits)

## Data Flow

### Tracking a Coin (/track DOGE)

1. User sends `/track DOGE Dogecoin` to Telegram
2. `bot.py` receives command via `track_command()`
3. Calls `coin_tracker.add_coin(chat_id, "DOGE", "Dogecoin")`
4. Calls `coin_tracker.analyze_coin("DOGE", "Dogecoin")`
5. `CoinTracker` calls `twitter_client.build_coin_query()` to create search query
6. `CoinTracker` calls `twitter_client.search_recent_tweets()` with query
7. `TwitterClient` queries Twitter API and returns tweets
8. For each tweet, `CoinTracker` calls `sentiment_analyzer.analyze()`
9. `SentimentAnalyzer` analyzes text and returns polarity/subjectivity
10. `CoinTracker` aggregates all sentiment scores
11. `CoinTracker` formats results into readable message
12. `bot.py` sends formatted message back to user via Telegram

### Checking a Coin (/check SHIB)

1. User sends `/check SHIB` to Telegram
2. `bot.py` receives command via `check_command()`
3. Follows steps 4-12 from tracking flow
4. Does not add to tracking list (one-time analysis)

## Key Design Decisions

### Separation of Concerns
- Each module has a single, clear responsibility
- Bot logic separate from analysis logic
- Twitter API interactions isolated in dedicated client
- Sentiment analysis independent of data source

### Stateful Tracking
- `CoinTracker` maintains state of tracked coins per chat
- Allows multiple users to track different coins
- In-memory storage (could be extended to database)

### Flexible Sentiment Analysis
- Uses TextBlob for quick, reliable sentiment analysis
- Could be swapped for more advanced NLP models
- Provides both raw scores and user-friendly categories

### Rate Limit Handling
- Twitter client uses `wait_on_rate_limit=True`
- Gracefully handles API errors
- Configurable tweet limits to avoid excessive API usage

### Error Resilience
- Each module handles its own errors
- Bot continues running even if single operation fails
- User-friendly error messages

## Extensibility

### Adding New Features

**Database Persistence**:
- Modify `coin_tracker.py` to use SQLite/PostgreSQL
- Store tracked coins and historical data

**Scheduled Updates**:
- Add background task to check tracked coins periodically
- Send notifications when sentiment changes significantly

**Advanced Sentiment**:
- Replace TextBlob with transformers-based models
- Add emotion detection, entity recognition

**Price Integration**:
- Add coin price data from CoinGecko API
- Correlate sentiment with price movements

**Web Dashboard**:
- Add Flask/FastAPI web interface
- Visualize sentiment trends over time

## Security Considerations

- API keys stored in environment variables, not code
- `.gitignore` prevents committing secrets
- Twitter Bearer Token sufficient for read-only access
- No sensitive user data stored

## Performance

- Twitter API rate limits: ~15 requests per 15 minutes
- TextBlob sentiment analysis: Fast (milliseconds per tweet)
- In-memory storage: Instant access, no database overhead
- Suitable for personal/small team usage
- For large scale, consider:
  - Database for persistence
  - Redis for caching
  - Queue system for background processing
