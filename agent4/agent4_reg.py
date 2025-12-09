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

from agent4 import FoodPlanner

logging.basicConfig(level=logging.INFO)



class FoodPlannerHandler(Handler):
    """
    Handles tasks for meal planning.
    """
    def __init__(self, api_key: str):
        self.planner = FoodPlanner(api_key)
        logging.info("FoodPlannerHandler initialized.")

    async def execute(self, task: Task) -> Result:
        query = task.data.decode()
        logging.info(f"Task {task.id}: Executing meal plan for: {query}")
        try:
            recommendation = self.planner.generate_meal_recommendation(query)

            recommendation_json = json.dumps(recommendation, indent=2)

            logging.info(f"Task {task.id}: Processed successfully.")
            return Result(
                data=recommendation_json.encode(),
                success=True
            )
        except Exception as e:
            logging.error(f"Task {task.id}: Failed to process: {e}")
            return Result(data=b"", success=False, error=str(e))


class MealBiddingStrategy(BiddingStrategy):
    """Bids on 'meal-planning' intents."""
    def __init__(self):
        logging.info("MealBiddingStrategy initialized")

    def should_bid(self, intent: Intent) -> bool:
        logging.info(f"Evaluating intent {getattr(intent, 'id', '<unknown>')}")
        return True

    def calculate_bid(self, intent: Intent):
        return Bid(price=10, currency="PIN",metadata={"capabilites":"meal-planning,restaurant-recommendation"})


class FoodCallbacks(Callbacks):
    """Optional callbacks placeholder for future use."""
    pass


async def main():
    logging.basicConfig(level=logging.INFO)

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
        .with_agent_id("food-planner-agent-001")
        .with_chain_address("0x80497604dd8De496FE60be7E41aEC9b28A58c02a")
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:8090"))
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS", "ec2-54-157-130-202.compute-1.amazonaws.com:9090"))
        .with_capabilities("meal-planning", "restaurant-recommendation")
        .with_intent_types("meal-planning")
        .with_private_key(os.getenv("PRIVATE_KEY", "1803db14a051184bd5fa6c23d8b98f7ed8dc35b643c16af0a7fd76149f48efdd"))
        .build()
    )

    agent = SDK(config)

    # Register components
    agent.register_handler(FoodPlannerHandler())
    agent.register_bidding_strategy(MealBiddingStrategy())
    agent.register_callbacks(FoodCallbacks())

    report = execution_report_pb2.ExecutionReport(
        assignment_id="assignment-1",
        intent_id="intent-meal-001",
        agent_id="food-planner-agent-001",
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
