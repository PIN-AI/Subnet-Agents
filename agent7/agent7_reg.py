import asyncio
import logging
import json
import time
import os

from subnet_sdk import (
    SDK,
    ConfigBuilder,
    Handler,
    Task,
    Result,
    BiddingStrategy,
    Intent,
    Bid,
    Callbacks,
    ValidatorClient,
    SigningConfig
)

from subnet_sdk.proto.subnet import execution_report_pb2

# Import your large trading system module
from agent7 import (
    HyperliquidOnlineTradingSystem,
    OnlineBacktester,
    MarketDataHandler,
    OnlineFeatureEngine,
    OnlineTradingModel,
    RiskManager,
    OnlineStrategyEngine,
    MonitoringSystem
)

logging.basicConfig(level=logging.INFO)


class HyperliquidHandler(Handler):
    """
    Handles tasks for Hyperliquid online trading simulation.
    """
    def __init__(self):
        self.system = None
        logging.info("HyperliquidHandler initialized.")

    async def execute(self, task: Task) -> Result:
        try:
            query = task.data.decode()
            data = json.loads(query)
            symbols = data.get("symbols", ["BTC-USD"])
            balance = data.get("balance", 10000)

            logging.info(f"Task {task.id}: Running Hyperliquid system for {symbols}")

            # Initialize system
            self.system = HyperliquidOnlineTradingSystem(symbols, account_balance=balance)

            # Perform warm start
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)

            metrics = {}
            for sym in symbols:
                metrics[sym] = self.system.warm_start(sym, start_date, end_date)

            # Backtest only last 7 days
            backtester = OnlineBacktester(self.system)
            bt_start = end_date - timedelta(days=7)
            backtest_results = {}
            for sym in symbols:
                backtest_results[sym] = backtester.run_backtest(sym, bt_start, end_date)

            output = {
                "warm_start_metrics": metrics,
                "backtest_results": backtest_results
            }

            encoded = json.dumps(output, indent=2).encode()

            logging.info(f"Task {task.id}: Completed successfully.")
            return Result(data=encoded, success=True)

        except Exception as e:
            logging.error(f"Task {task.id}: Failed: {e}")
            return Result(data=b"", success=False, error=str(e))


class HyperliquidBiddingStrategy(BiddingStrategy):
    def __init__(self):
        logging.info("HyperliquidBiddingStrategy initialized")

    def should_bid(self, intent: Intent) -> bool:
        return True

    def calculate_bid(self, intent: Intent):
        return Bid(price=10, currency="PIN",metadata={"capabilities":"hyperliquid-trading,online-ml-signals"})


class HyperliquidCallbacks(Callbacks):
    pass


async def main():
    logging.basicConfig(level=logging.INFO)

    # Signing config
    signing_config = SigningConfig(
        private_key_hex=os.getenv("PRIVATE_KEY", "1803db14a051184bd5fa6c23d8b98f7ed8dc35b643c16af0a7fd76149f48efdd")
    )

    validator_client = ValidatorClient(
        target=os.getenv("VALIDATOR_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:9090"),
        secure=False,
        signing_config=signing_config
    )

    config = (
        ConfigBuilder()
        .with_subnet_id(os.getenv("SUBNET_ID", "0x0000000000000000000000000000000000000000000000000000000000000015"))
        .with_agent_id("hyperliquid-agent-007")
        .with_chain_address("0x80497604dd8De496FE60be7E41aEC9b28A58c02a")
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:8090"))
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:9090"))
        .with_capabilities("hyperliquid-trading", "online-ml-signals")
        .with_intent_types("hyperliquid-trading")
        .with_private_key(os.getenv("PRIVATE_KEY", "1803db14a051184bd5fa6c23d8b98f7ed8dc35b643c16af0a7fd76149f48efdd"))
        .build()
    )

    agent = SDK(config)

    # Register handler + bidding + callbacks
    agent.register_handler(HyperliquidHandler())
    agent.register_bidding_strategy(HyperliquidBiddingStrategy())
    agent.register_callbacks(HyperliquidCallbacks())

    # Submit single execution report (matches your first prompt exactly)
    report = execution_report_pb2.ExecutionReport(
        assignment_id="assignment-1",
        intent_id="intent-hyperliquid-001",
        agent_id="hyperliquid-agent-007",
        status=execution_report_pb2.ExecutionReport.SUCCESS,
        timestamp=int(time.time()),
    )

    try:
        response = await validator_client.submit_execution_report(report)
    finally:
        await validator_client.close()

    logging.info(f"Starting agent: {agent.get_agent_id()} on subnet: {agent.get_subnet_id()}")
    await agent.start()

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logging.info("Shutting down agent...")
        await agent.stop()
        logging.info("Agent stopped.")


if __name__ == "__main__":
    asyncio.run(main())
