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

from agent2 import run_financial_analysis


class CorporateAnalysisHandler(Handler):
    """
    Handles tasks for corporate financial analysis.
    """
    async def execute(self, task: Task) -> Result:
        logging.info(f"Task {task.id}: Executing corporate analysis")

        try:
            query = task.data.decode()
            report = run_financial_analysis(query)

            encoded = json.dumps(report, indent=2).encode()

            return Result(data=encoded, success=True)

        except Exception as e:
            logging.error(f"Task {task.id}: Failed: {e}")
            return Result(data=b"", success=False, error=str(e))


class CorporateBiddingStrategy(BiddingStrategy):
    """Bids for corporate-analysis intents."""
    def __init__(self):
        logging.info("CorporateBiddingStrategy initialized")

    def should_bid(self, intent: Intent) -> bool:
        logging.info(f"Evaluating intent {intent.id}")
        return intent.type == "corporate-analysis"

    def calculate_bid(self, intent: Intent):
        return Bid(price=10, currency="PIN")


class CorporateCallbacks(Callbacks):
    """Optional callbacks (kept empty for now)."""
    pass


async def main():
    logging.basicConfig(level=logging.INFO)

    # Signing config
    signing_config = SigningConfig(
        private_key_hex=os.getenv("PRIVATE_KEY")
    )

    # Validator client
    validator_client = ValidatorClient(
        target=os.getenv("VALIDATOR_ADDRESS", "localhost:9090"),
        secure=False,
        signing_config=signing_config
    )

    # Build config
    config = (
        ConfigBuilder()
        .with_subnet_id("0x0000000000000000000000000000000000000000000000000000000000000015")
        .with_agent_id("corporate-analysis-agent-001")
        .with_chain_address("0x80497604dd8De496FE60be7E41aEC9b28A58c02a")
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS", "localhost:8090"))
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS", "localhost:9090"))
        .with_capabilities("corporate-analysis", "financial-report")
        .with_intent_types("corporate-analysis")
        .with_private_key(os.getenv("PRIVATE_KEY"))
        .build()
    )

    agent = SDK(config)

    # Register components
    agent.register_handler(CorporateAnalysisHandler())
    agent.register_bidding_strategy(CorporateBiddingStrategy())
    agent.register_callbacks(CorporateCallbacks())

    report = execution_report_pb2.ExecutionReport(
                assignment_id="assignment-1",
                intent_id="intent-xyz",
                agent_id="corporate-analysis-agent-001",
                status=execution_report_pb2.ExecutionReport.SUCCESS,
                timestamp=int(time.time()),
            )

    try:
        response = await validator_client.submit_execution_report_batch(report)
        print(f"Batch results: {response.success} succeeded, {response.failed} failed")
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
