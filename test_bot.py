"""
Basic tests for the Hype Bot modules.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sentiment_analyzer import SentimentAnalyzer

# Only import CoinTracker if dependencies are available
try:
    from coin_tracker import CoinTracker
    COIN_TRACKER_AVAILABLE = True
except ImportError:
    COIN_TRACKER_AVAILABLE = False
    print("⚠️  CoinTracker tests skipped (missing dependencies)")


def test_sentiment_analyzer():
    """Test sentiment analyzer basic functionality."""
    print("Testing SentimentAnalyzer...")
    analyzer = SentimentAnalyzer()
    
    # Test positive sentiment
    result = analyzer.analyze("This coin is amazing! To the moon! 🚀")
    assert result['polarity'] > 0, "Expected positive polarity"
    assert analyzer.categorize_sentiment(result['polarity']) == 'positive'
    print("✓ Positive sentiment test passed")
    
    # Test negative sentiment
    result = analyzer.analyze("This coin is terrible. It's crashing hard!")
    assert result['polarity'] < 0, "Expected negative polarity"
    assert analyzer.categorize_sentiment(result['polarity']) == 'negative'
    print("✓ Negative sentiment test passed")
    
    # Test neutral sentiment
    result = analyzer.analyze("The price is stable.")
    category = analyzer.categorize_sentiment(result['polarity'])
    assert category in ['neutral', 'positive', 'negative'], "Expected valid category"
    print("✓ Neutral sentiment test passed")
    
    # Test emoji mapping
    emoji = analyzer.get_sentiment_emoji(0.7)
    assert emoji == '🚀', f"Expected rocket emoji for high positive, got {emoji}"
    print("✓ Emoji mapping test passed")
    
    # Test aggregate
    sentiments = [
        {'polarity': 0.5, 'subjectivity': 0.5},
        {'polarity': -0.3, 'subjectivity': 0.4},
        {'polarity': 0.2, 'subjectivity': 0.6}
    ]
    aggregate = analyzer.aggregate_sentiment(sentiments)
    assert aggregate['total_count'] == 3
    assert aggregate['positive_count'] == 2
    assert aggregate['negative_count'] == 1
    print("✓ Aggregate sentiment test passed")
    
    print("✅ All SentimentAnalyzer tests passed!\n")


def test_coin_tracker():
    """Test coin tracker basic functionality."""
    if not COIN_TRACKER_AVAILABLE:
        print("⏭️  Skipping CoinTracker tests (dependencies not installed)\n")
        return
    
    print("Testing CoinTracker...")
    tracker = CoinTracker()
    
    # Test adding coins
    tracker.add_coin(12345, "DOGE", "Dogecoin")
    coins = tracker.get_tracked_coins(12345)
    assert len(coins) == 1
    assert coins[0]['symbol'] == 'DOGE'
    assert coins[0]['name'] == 'Dogecoin'
    print("✓ Add coin test passed")
    
    # Test adding duplicate
    tracker.add_coin(12345, "doge", "Dogecoin")
    coins = tracker.get_tracked_coins(12345)
    assert len(coins) == 1, "Should not add duplicate"
    print("✓ Duplicate prevention test passed")
    
    # Test adding multiple coins
    tracker.add_coin(12345, "SHIB", "Shiba Inu")
    coins = tracker.get_tracked_coins(12345)
    assert len(coins) == 2
    print("✓ Multiple coins test passed")
    
    # Test removing coin
    removed = tracker.remove_coin(12345, "DOGE")
    assert removed is True
    coins = tracker.get_tracked_coins(12345)
    assert len(coins) == 1
    assert coins[0]['symbol'] == 'SHIB'
    print("✓ Remove coin test passed")
    
    # Test removing non-existent coin
    removed = tracker.remove_coin(12345, "NOTREAL")
    assert removed is False
    print("✓ Remove non-existent coin test passed")
    
    # Test multiple chat IDs
    tracker.add_coin(67890, "PEPE", "Pepe")
    coins_chat1 = tracker.get_tracked_coins(12345)
    coins_chat2 = tracker.get_tracked_coins(67890)
    assert len(coins_chat1) == 1
    assert len(coins_chat2) == 1
    assert coins_chat1[0]['symbol'] != coins_chat2[0]['symbol']
    print("✓ Multiple chat IDs test passed")
    
    print("✅ All CoinTracker tests passed!\n")


def test_message_formatting():
    """Test message formatting."""
    if not COIN_TRACKER_AVAILABLE:
        print("⏭️  Skipping formatting tests (dependencies not installed)\n")
        return
    
    print("Testing message formatting...")
    tracker = CoinTracker()
    
    # Create mock analysis data
    analysis = {
        'symbol': 'DOGE',
        'name': 'Dogecoin',
        'sentiment': {
            'average_polarity': 0.5,
            'average_subjectivity': 0.5,
            'positive_count': 7,
            'negative_count': 2,
            'neutral_count': 1,
            'total_count': 10
        },
        'tweets': [
            {
                'text': 'Dogecoin to the moon! This is amazing!',
                'author': {'username': 'cryptofan', 'name': 'Crypto Fan'},
                'metrics': {'likes': 100, 'retweets': 50, 'replies': 10},
                'sentiment': {'polarity': 0.8, 'subjectivity': 0.6}
            }
        ]
    }
    
    message = tracker.format_analysis_message(analysis)
    assert '$DOGE' in message
    assert 'Dogecoin' in message
    assert 'POSITIVE' in message
    assert '7' in message  # positive count
    assert '2' in message  # negative count
    print("✓ Message formatting test passed")
    
    # Test empty analysis
    analysis_empty = {
        'symbol': 'TEST',
        'name': None,
        'sentiment': None,
        'tweets': []
    }
    message = tracker.format_analysis_message(analysis_empty)
    assert 'No recent activity' in message
    print("✓ Empty analysis formatting test passed")
    
    print("✅ All formatting tests passed!\n")


if __name__ == '__main__':
    print("=" * 50)
    print("Running Hype Bot Tests")
    print("=" * 50)
    print()
    
    try:
        test_sentiment_analyzer()
        test_coin_tracker()
        test_message_formatting()
        
        print("=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
