import asyncio
import logging
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
    MatcherClient,
    ValidatorClient,
    SigningConfig           
)
from subnet_sdk.proto.subnet import service_pb2, execution_report_pb2

from agent1 import FinNews


class FinancialNewsHandler(Handler):
    async def execute(self, task: Task) -> Result:
        logging.info(f"Task {task.id}: Executing with data: {task.data}")
        try:
            fin = FinNews()
            resp_data = fin.fin_news_agent(task)
            return Result(data=f"{resp_data}".encode(), success=True)
        except Exception as e:
            logging.error(f"Task {task.id}: Failed to process: {e}")
            return Result(data=b"", success=False, error=str(e))


class MyCustomBiddingStrategy(BiddingStrategy):
    def __init__(self):
        logging.info("CustomBiddingStrategy initialized")

    def should_bid(self, intent: Intent) -> bool:
        logging.info(f"Evaluating intent {intent.id}")
        return True

    def calculate_bid(self, intent: Intent):
        return Bid(price=10, currency="PIN",metadata={"capabilities":"news-analyser, financial-impact-predictor"})


class MyCallbacks(Callbacks):
    pass


async def main():
    logging.basicConfig(level=logging.INFO)

    signing_config = SigningConfig(
        private_key_hex=os.getenv("PRIVATE_KEY","1803db14a051184bd5fa6c23d8b98f7ed8dc35b643c16af0a7fd76149f48efdd")
    )

    validator_client = ValidatorClient(
        target=os.getenv("VALIDATOR_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:9090"),
        secure=False,
        signing_config=signing_config
    )

    config = (
        ConfigBuilder()
        .with_subnet_id(os.getenv("SUBNET_ID", "0x0000000000000000000000000000000000000000000000000000000000000015"))
        .with_agent_id("financial-news-agent-001")
        .with_chain_address("0x80497604dd8De496FE60be7E41aEC9b28A58c02a")
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS","ec2-54-157-130-202.compute-1.amazonaws.com:8090"))
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS","ec2-54-157-130-202.compute-1.amazonaws.com:9090"))
        .with_capabilities("news-analyser", "financial-impact-predictor")
        .with_intent_types("news-analyser")
        .with_private_key(os.getenv("PRIVATE_KEY","1803db14a051184bd5fa6c23d8b98f7ed8dc35b643c16af0a7fd76149f48efdd"))
        .build()
    )

    agent = SDK(config)

    agent.register_handler(FinancialNewsHandler())
    agent.register_bidding_strategy(MyCustomBiddingStrategy())
    agent.register_callbacks(MyCallbacks())


    report = execution_report_pb2.ExecutionReport(
            assignment_id="assignment-1",
            intent_id="intent-123",
            agent_id="agent-1",
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

