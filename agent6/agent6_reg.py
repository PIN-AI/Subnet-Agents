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
from subnet_sdk.proto.subnet import service_pb2, execution_report_pb2

from agent6 import PolymarketRedditAgent

logging.basicConfig(level=logging.INFO)

POLYMARKET_API_KEY = os.getenv("POLYMARKET_API_KEY","a")
REDDIT_ID = os.getenv("REDDIT_ID","a")
REDDIT_SECRET = os.getenv("REDDIT_SECRET","a")
USER_AGENT = os.getenv("REDDIT_USER_AGENT", "polymarket-agent/1.0")


class PolymarketHandler(Handler):
    """
    Handles tasks for Polymarket/Reddit analysis.
    """
    def __init__(self, poly_key, reddit_id, reddit_secret, user_agent):
        self.agent = PolymarketRedditAgent(
            openai_api_key=poly_key,
            reddit_client_id=reddit_id,
            reddit_client_secret=reddit_secret,
            reddit_user_agent=user_agent
        )
        logging.info("PolymarketHandler initialized.")

    async def execute(self, task: Task) -> Result:
        query = task.data.decode()
        logging.info(f"Task {task.id}: Executing Polymarket analysis for: {query}")
        try:
            trade_calls = self.agent.analyze_from_query(user_query=query)

            # Best-effort serialization of Pydantic / dataclass objects
            try:
                serialized = [getattr(call, "model_dump", lambda: call)() for call in trade_calls]
            except Exception:
                # fallback: attempt __dict__ on each element
                serialized = [getattr(call, "__dict__", str(call)) for call in trade_calls]

            trade_calls_json = json.dumps(serialized, indent=2)

            logging.info(f"Task {task.id}: Processed successfully.")
            return Result(
                data=trade_calls_json.encode(),
                success=True
            )
        except Exception as e:
            logging.error(f"Task {task.id}: Failed to process: {e}")
            return Result(data=b"", success=False, error=str(e))


class PolymarketBiddingStrategy(BiddingStrategy):
    """Bids on 'polymarket-analysis' intents."""
    def __init__(self):
        logging.info("PolymarketBiddingStrategy initialized")

    def should_bid(self, intent: Intent) -> bool:
        logging.info(f"Evaluating intent {getattr(intent, 'id', '<unknown>')}")
        return intent.type == "polymarket-analysis"

    def calculate_bid(self, intent: Intent):
        return Bid(price=10, currency="PIN")


class PolymarketCallbacks(Callbacks):
    """Optional callbacks placeholder for future use."""
    pass


async def main():
    logging.basicConfig(level=logging.INFO)

    if not all([POLYMARKET_API_KEY, REDDIT_ID, REDDIT_SECRET]):
        logging.error("Missing API keys for Polymarket/Reddit. Exiting.")
        return

    signing_config = SigningConfig(
        private_key_hex=os.getenv("PRIVATE_KEY", "1803db14a051184bd5fa6c23d8b98f7ed8dc35b643c16af0a7fd76149f48efdd")
    )

    validator_client = ValidatorClient(
        target=os.getenv("VALIDATOR_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:9090"),
        secure=False,
        signing_config=signing_config
    )

    # Build agent config
    config = (
        ConfigBuilder()
        .with_subnet_id("0x0000000000000000000000000000000000000000000000000000000000000015")
        .with_agent_id(os.getenv("AGENT_ID", "polymarket-reddit-agent-001"))
        .with_chain_address(os.getenv("CHAIN_ADDRESS", "0x80497604dd8De496FE60be7E41aEC9b28A58c02a"))
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:8090"))
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:9090"))
        .with_capabilities("polymarket-analysis", "reddit-sentiment")
        .with_intent_types("polymarket-analysis")
        .with_private_key(os.getenv("PRIVATE_KEY", "1803db14a051184bd5fa6c23d8b98f7ed8dc35b643c16af0a7fd76149f48efdd"))
        .build()
    )

    agent = SDK(config)

    # Register components
    agent.register_handler(PolymarketHandler(
        poly_key=POLYMARKET_API_KEY,
        reddit_id=REDDIT_ID,
        reddit_secret=REDDIT_SECRET,
        user_agent=USER_AGENT
    ))
    agent.register_bidding_strategy(PolymarketBiddingStrategy())
    agent.register_callbacks(PolymarketCallbacks())

    # Submit execution report (single submission like first prompt)
    report = execution_report_pb2.ExecutionReport(
        assignment_id="assignment-1",
        intent_id="intent-polymarket-001",
        agent_id=config.agent_id if hasattr(config, "agent_id") else os.getenv("AGENT_ID", "polymarket-reddit-agent-001"),
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
