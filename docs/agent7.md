# Hyperliquid Online Trading System

A sophisticated online machine learning trading system for derivatives trading on Hyperliquid. Leverages River's streaming algorithms for continuous model adaptation, real-time feature engineering, and risk-aware position sizing.

## Features

- **Online Machine Learning**: Adaptive Random Forest models that learn from streaming data in real-time
- **Real-Time Feature Engineering**: Dynamic technical indicators (SMA, EMA, RSI, Bollinger Bands, momentum) computed on-the-fly
- **Hyperliquid Integration**: Direct integration with Hyperliquid API for mark prices, funding rates, order books, and historical data
- **Advanced Risk Management**: Kelly-criterion-inspired position sizing, dynamic stop-losses based on volatility
- **Backtesting Engine**: Full historical backtesting with proper prequential evaluation (never peek at future data)
- **Warm-Start Training**: Pre-train models on historical data before live trading
- **Continuous Learning**: Models automatically update as trades complete with real outcomes

## Requirements

- Python 3.9+
- river (online machine learning)
- pandas
- numpy
- requests

## Installation

1. Install dependencies:
   ```bash
   pip install river pandas numpy requests
   ```

2. Verify Hyperliquid API connectivity:
   ```python
   # Test connection
   import requests
   response = requests.post("https://api.hyperliquid.xyz/info", 
                           json={"type": "metaAndAssetCtxs"})
   print(response.status_code)  # Should be 200
   ```

## Architecture Overview

### Core Components

**MarketDataHandler**
- Fetches real-time data from Hyperliquid (mark prices, funding rates, open interest)
- Retrieves historical candles for backtesting and warm-start training
- Manages order book snapshots (L2 data)
- Handles symbol normalization (e.g., "BTC-USD" → "BTC")

**OnlineFeatureEngine**
- Streaming feature extraction using sliding windows
- Computes 16+ technical indicators per candle:
  - Simple and exponential moving averages
  - RSI approximation
  - Bollinger Bands positioning
  - Momentum (5-period and 10-period)
  - Volatility measures
  - Volume ratios
  - Funding rate statistics

**OnlineTradingModel**
- Dual-model architecture:
  - **Classifier**: Predicts price direction (binary: up/down)
  - **Regressor**: Estimates expected returns (continuous)
- Uses Adaptive Random Forest (ARF) for non-stationary market conditions
- Prequential evaluation: tests on data before learning from it
- Tracks accuracy and MAE with windowed metrics

**RiskManager**
- Calculates optimal position sizes using modified Kelly criterion
- Dynamic stop-loss placement based on volatility (default: 2x volatility)
- Risk-reward ratio-based take-profit targets (default: 2.5x)
- Position size caps and portfolio-level risk limits

**OnlineStrategyEngine**
- Converts model predictions into trade signals
- Filters low-confidence predictions (< 55% confidence)
- Generates reasoning for each signal
- Risk metrics calculation and logging

**OnlineBacktester**
- Walk-forward backtesting with prequential evaluation
- No look-ahead bias (model only sees past data)
- Simulates realistic trade entry/exit using generated signals
- Tracks equity curve and PnL per trade

## Data Types & Enums

### OrderSide
- `BUY` - Long position
- `SELL` - Short position

### OrderType
- `MARKET` - Execute at market price
- `LIMIT` - Execute at specified price

### SignalStrength
- `STRONG_BUY` - Highest conviction bullish (confidence > 80%)
- `BUY` - Bullish signal
- `NEUTRAL` - No clear direction
- `SELL` - Bearish signal
- `STRONG_SELL` - Highest conviction bearish (confidence > 80%)

## Usage

### Basic Setup & Warm-Start

```python
from hyperliquid_trading_system import HyperliquidOnlineTradingSystem, OnlineBacktester
from datetime import datetime, timedelta

# Initialize system
symbols = ["BTC-USD", "ETH-USD"]
account_balance = 10000
system = HyperliquidOnlineTradingSystem(symbols, account_balance)

# Warm-start with historical data (30 days)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

for symbol in symbols:
    metrics = system.warm_start(symbol, start_date, end_date)
    print(f"{symbol} Model Metrics:", metrics)
```

### Backtesting

```python
backtester = OnlineBacktester(system)

# Run backtest on recent 7 days
bt_start = datetime.now() - timedelta(days=7)
bt_end = datetime.now()

for symbol in symbols:
    stats, trades, equity_curve = backtester.run_backtest(
        symbol, 
        bt_start, 
        bt_end, 
        initial_balance=10000
    )
    print(f"Return: {stats['return']:.2%}")
    print(f"Trades: {len(trades)}")
```

### Live Signal Generation

```python
# Fetch real-time data
market_data = system.market_data_handler.fetch_realtime_data("BTC-USD")

# Process latest candle
candle = {
    'close': market_data.mark_price,
    'volume': market_data.volume_24h,
    'funding_rate': market_data.funding_rate
}

signal = system.process_new_candle("BTC-USD", candle)

if signal:
    print(f"Signal: {signal.signal.value}")
    print(f"Side: {signal.side.value}")
    print(f"Entry: ${signal.suggested_entry:.2f}")
    print(f"Stop Loss: ${signal.stop_loss:.2f}")
    print(f"Take Profit: ${signal.take_profit:.2f}")
    print(f"Size: {signal.suggested_size:.4f}")
    print(f"Confidence: {signal.confidence:.1%}")
    print(f"Risk/Reward: {signal.risk_reward_ratio:.2f}")
```

### Trade Outcome Update (Continuous Learning)

```python
# After trade closes with actual return
actual_return = 0.025  # +2.5%
system.update_model_with_trade_outcome("BTC-USD", actual_return)

# Model automatically learns and adapts
```

### System Check

```python
# Run full initialization, warm-start, backtest, and live signal check
run_hyperliquid_system_check(["BTC-USD", "ETH-USD"])
```

## Output Structure

### TradeSignal Object

```python
@dataclass
class TradeSignal:
    timestamp: float              # Unix timestamp
    symbol: str                   # Trading pair
    signal: SignalStrength        # Signal strength (STRONG_BUY to STRONG_SELL)
    side: OrderSide              # BUY or SELL
    suggested_entry: float       # Current price / recommended entry
    suggested_size: float        # Position size in asset units
    stop_loss: float            # Stop loss price level
    take_profit: float          # Take profit price level
    confidence: float           # 0-1 model confidence
    reasoning: str              # Human-readable explanation
    risk_reward_ratio: float    # RR ratio (e.g., 2.5)
    model_metrics: Dict         # Model performance stats
```

## Configuration Parameters

### RiskManager

```python
risk_manager = RiskManager(
    max_position_size=1000,      # Maximum USD per position
    max_leverage=10.0,           # Maximum allowed leverage
    max_portfolio_risk=0.02      # 2% per trade
)
```

### OnlineFeatureEngine

```python
feature_engine = OnlineFeatureEngine(
    window_size=50  # Lookback window for statistics
)
```

### Model Architecture

- **Classifier**: 10 Adaptive Random Forest models, max_depth=10
- **Regressor**: 10 Adaptive Random Forest models, max_depth=8
- Both models use StandardScaler preprocessing

## API Reference

### HyperliquidOnlineTradingSystem

#### `__init__(symbols: List[str], account_balance: float)`
Initialize the trading system with symbols and account balance.

#### `warm_start(symbol: str, start_date: datetime, end_date: datetime) -> Dict`
Pre-train model on historical data. Returns model metrics.

#### `process_new_candle(symbol: str, candle: Dict) -> Optional[TradeSignal]`
Process new market data and generate trading signal.

#### `update_model_with_trade_outcome(symbol: str, actual_return: float)`
Update model with trade outcome for continuous learning.

#### `save_model(filepath: str)`
Persist trained model to disk using pickle.

### MarketDataHandler

#### `fetch_realtime_data(symbol: str) -> MarketData`
Get current mark price, funding rate, open interest, and 24h volume.

#### `fetch_historical_data(symbol: str, start_date: datetime, end_date: datetime, interval: str) -> pd.DataFrame`
Fetch historical candles. Interval options: "1h", "1d", "5d", "1wk", "1mo", "3mo".

#### `update_orderbook(symbol: str) -> None`
Fetch and store L2 order book snapshot.

### OnlineBacktester

#### `run_backtest(symbol: str, start_date: datetime, end_date: datetime, initial_balance: float) -> Tuple[Dict, List, List]`
Run walk-forward backtest. Returns (stats, trades, equity_curve).

## Model Performance Tracking

The system tracks:

```python
model_metrics = {
    'samples_learned': int,           # Total samples trained
    'overall_accuracy': float,        # Classification accuracy (0-1)
    'recent_accuracy': float,         # Last 100 samples accuracy
    'overall_mae': float,             # Mean absolute error (returns)
    'recent_mae': float               # Last 100 samples MAE
}
```

## Important Notes

### Prequential Evaluation
The backtest engine uses **prequential (walk-forward) evaluation**: the model is always tested on data it has never seen before, then learns from it. This eliminates look-ahead bias and provides realistic performance estimates.

### Online Learning Dynamics
- Models continuously adapt as market regimes change
- Older patterns are gradually forgotten (ideal for non-stationary markets)
- Each new trade outcome feeds back into the model
- Warm-start period is critical for initial performance

### Risk Management
- Position sizes automatically scale with confidence and volatility
- Stop-losses are dynamically set (default: 2x volatility below entry)
- Maximum portfolio risk per trade: 2% of account
- Signals < 55% confidence are filtered out

### Hyperliquid API Integration
- Uses POST endpoints: `metaAndAssetCtxs`, `candleSnapshot`, `l2Book`
- Symbol format: "BTC", "ETH" (without "-USD" suffix internally)
- Timestamps in milliseconds for candles, seconds for current data
- All prices and volumes returned as strings for precision

## Limitations

- Model predictions based on technical indicators and market microstructure only
- Warm-start requires sufficient historical data (recommend 30+ days)
- Backtests assume perfect execution (no slippage/fees modeled)
- Real-time signal generation depends on consistent market data flow
- Overfitting risk on warm-start period if not careful with parameters

## Disclaimer

This system is for educational and research purposes. Futures/derivatives trading involves substantial risk of loss. Past performance does not guarantee future results. Always validate signals independently, manage risk carefully, and only trade with capital you can afford to lose. No warranty is provided for accuracy or completeness of the system.

## Support & Logging

The system provides comprehensive logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

Logs include:
- Model warm-start progress
- Signal generation details
- Backtest results and equity curves
- Error messages and API issues

## Future Enhancements

- Multi-symbol portfolio optimization
- Funding rate arbitrage strategies
- Order flow imbalance detection
- Ensemble methods combining multiple models
- Real slippage and fee modeling in backtests