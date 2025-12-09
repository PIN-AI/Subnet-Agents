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

from agent5 import StockAnalysisAgent

logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API")


class StockAnalysisHandler(Handler):
    """
    Handles tasks for stock analysis.
    """
    def __init__(self, api_key: str):
        self.agent = StockAnalysisAgent(openai_api_key=api_key)
        logging.info("StockAnalysisHandler initialized.")

    async def execute(self, task: Task) -> Result:
        query = task.data.decode()
        logging.info(f"Task {task.id}: Executing stock analysis for: {query}")
        try:
            analysis = self.agent.analyze(query)

            # Best-effort serialization to JSON
            try:
                analysis_dict = getattr(analysis, "__dict__", None) or {}
                serializable_analysis = {
                    "query": getattr(getattr(analysis, "query", None), "raw_query", None),
                    "ticker": getattr(getattr(analysis, "query", None), "ticker_symbol", None),
                    "prediction_current": getattr(getattr(analysis, "prediction", None), "current_price", None),
                    "prediction_future": getattr(getattr(analysis, "prediction", None), "predicted_price", None),
                    "recommendation": getattr(getattr(analysis, "recommendation", None), "value", None),
                    "reasoning": getattr(analysis, "reasoning", None)
                }
                analysis_json = json.dumps(serializable_analysis, indent=2)
            except Exception as serialize_error:
                logging.error(f"Failed to serialize analysis: {serialize_error}")
                analysis_json = json.dumps({"error": "Failed to serialize analysis object"})

            logging.info(f"Task {task.id}: Processed successfully.")
            return Result(
                data=analysis_json.encode(),
                success=True
            )
        except Exception as e:
            logging.error(f"Task {task.id}: Failed to process: {e}")
            return Result(data=b"", success=False, error=str(e))


class StockBiddingStrategy(BiddingStrategy):
    """Bids on 'stock-analysis' intents."""
    def __init__(self):
        logging.info("StockBiddingStrategy initialized")

    def should_bid(self, intent: Intent) -> bool:
        logging.info(f"Evaluating intent {getattr(intent, 'id', '<unknown>')}")
        return True

    def calculate_bid(self, intent: Intent):
        return Bid(price=10, currency="PIN",metadata={"capabilities":"stock-analysis,price-prediction"})


class StockCallbacks(Callbacks):
    """Optional callbacks placeholder for future use."""
    pass


async def main():
    logging.basicConfig(level=logging.INFO)

    if not OPENAI_API_KEY:
        logging.error("OPENAI_API_KEY not set. Exiting.")
        return

    # Signing configuration for validator client
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
        .with_agent_id("stock-analysis-agent-001")
        .with_chain_address(os.getenv("CHAIN_ADDRESS", "0x80497604dd8De496FE60be7E41aEC9b28A58c02a"))
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:8090"))
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:9090"))
        .with_capabilities("stock-analysis", "price-prediction")
        .with_intent_types("stock-analysis")
        .with_private_key(os.getenv("PRIVATE_KEY", "1803db14a051184bd5fa6c23d8b98f7ed8dc35b643c16af0a7fd76149f48efdd"))
        .build()
    )

    agent = SDK(config)

    # Register components
    agent.register_handler(StockAnalysisHandler(api_key=OPENAI_API_KEY))
    agent.register_bidding_strategy(StockBiddingStrategy())
    agent.register_callbacks(StockCallbacks())

    # Submit report (single submission — matching first prompt)
    report = execution_report_pb2.ExecutionReport(
        assignment_id="assignment-1",
        intent_id="intent-stock-001",
        agent_id="stock-analysis-agent-001",
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
