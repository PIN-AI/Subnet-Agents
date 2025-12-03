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

# --- Logic from agent3.py ---
from agent3 import (
    create_sample_portfolio,
    create_sample_tax_profile,
    TaxOptimizationEngine,
    TaxReportGenerator,
    PortfolioManager
)

class TaxOptimizerHandler(Handler):
    """
    Handles tasks for tax optimization.
    """
    async def execute(self, task: Task) -> Result:
        logging.info(f"Task {task.id}: Executing tax optimization analysis...")
        try:
            # Run the full agent logic
            positions = create_sample_portfolio()
            portfolio = PortfolioManager(positions)
            tax_profile = create_sample_tax_profile()

            engine = TaxOptimizationEngine(portfolio, tax_profile)
            engine.run_complete_analysis()

            report_generator = TaxReportGenerator()
            full_report = report_generator.generate_report(engine)

            logging.info(f"Task {task.id}: Processed successfully.")
            return Result(
                data=full_report.encode(),
                success=True
            )
        except Exception as e:
            logging.error(f"Task {task.id}: Failed to process: {e}")
            return Result(data=b"", success=False, error=str(e))


class TaxBiddingStrategy(BiddingStrategy):
    """Bids on 'tax-optimization' intents."""
    def __init__(self):
        logging.info("TaxBiddingStrategy initialized")

    def should_bid(self, intent: Intent) -> bool:
        logging.info(f"Evaluating intent {getattr(intent, 'id', '<unknown>')}")
        return intent.type == "tax-optimization"

    def calculate_bid(self, intent: Intent):
        return Bid(price=10, currency="PIN")


class TaxCallbacks(Callbacks):
    """Optional callbacks (kept empty for now)."""
    pass


async def main():
    logging.basicConfig(level=logging.INFO)

    # Signing configuration for validator client
    signing_config = SigningConfig(
        private_key_hex=os.getenv("PRIVATE_KEY")
    )

    validator_client = ValidatorClient(
        target=os.getenv("VALIDATOR_ADDRESS", "localhost:9090"),
        secure=False,
        signing_config=signing_config
    )

    # Build agent config
    config = (
        ConfigBuilder()
        .with_subnet_id(os.getenv("SUBNET_ID"))
        .with_agent_id("tax-optimizer-agent-001")
        .with_chain_address("0x80497604dd8De496FE60be7E41aEC9b28A58c02a")
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS", "localhost:8090"))
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS", "localhost:9090"))
        .with_capabilities("tax-optimization", "portfolio-analysis")
        .with_intent_types("tax-optimization")
        .with_private_key(os.getenv("PRIVATE_KEY"))
        .build()
    )

    agent = SDK(config)

    # Register components
    agent.register_handler(TaxOptimizerHandler())
    agent.register_bidding_strategy(TaxBiddingStrategy())
    agent.register_callbacks(TaxCallbacks())

    # Optional: submit an execution report batch to the validator (mirrors other agents)
    reports = [
        execution_report_pb2.ExecutionReport(
            assignment_id="assignment-1",
            intent_id="intent-tax-001",
            agent_id=config.agent_id if hasattr(config, "agent_id") else "tax-optimizer-agent-001",
            status=execution_report_pb2.ExecutionReport.SUCCESS,
            timestamp=int(time.time()),
        ),
    ]

    batch_req = service_pb2.ExecutionReportBatchRequest(
        reports=reports,
        partial_ok=False,
    )

    try:
        response = await validator_client.submit_execution_report_batch(batch_req)
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
