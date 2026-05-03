from app.services.trading import calculate_rsi, normalize

def test_rsi_oversold():
    prices = [100, 98, 96, 94, 92, 90, 88, 86, 84, 82, 80, 78, 76, 74, 72]
    rsi = calculate_rsi(prices)
    assert rsi < 30

def test_rsi_overbought():
    prices = [100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128]
    rsi = calculate_rsi(prices)
    assert rsi > 70

def test_coin_normalize():
    assert normalize("BTC") == "bitcoin"
    assert normalize("ETH") == "ethereum"
    assert normalize("SOL") == "solana"
