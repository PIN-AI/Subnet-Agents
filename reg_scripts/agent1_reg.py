import asyncio
import logging
from subnet_sdk import (
    SDK, 
    ConfigBuilder, 
    Handler, 
    Task, 
    Result,
    BiddingStrategy,
    Intent,
    Bid            
)

from agents_a2a.agent1 import FinNews
import os

class FinancialNewsHandler(Handler):
    """
    This is your custom execution logic.
    It gets called when the agent receives a task.
    """
    async def execute(self, task: Task) -> Result:
        logging.info(f"Task {task.id}: Executing with data: {task.data}")
        try:
            fin = FinNews()
            resp_data = fin.fin_news_agent(task)
            
            logging.info(f"Task {task.id}: Processed successfully.")
            return Result(
                data=f"{resp_data}".encode(),
                success=True
            )
        except Exception as e:
            logging.error(f"Task {task.id}: Failed to process: {e}")
            return Result(data=b"", success=False, error=str(e))


class MyCustomBiddingStrategy(BiddingStrategy):
    """
    This is your custom bidding logic.
    It decides if and how much to bid on new intents.
    """
    def __init__(self):
        logging.info(f"CustomBiddingStrategy initialized")

    def should_bid(self, intent: Intent) -> bool:
        """
        Decide IF you want to bid on this intent.
        """
        logging.info(f"Evaluating intent {intent.id} of type {intent.type}")
        return True

    def calculate_bid(self, intent: Intent):
        """
        Calculate HOW MUCH you want to bid.
        This is called only if should_bid() returns True.
        """
        price = 10
        
        logging.info(f"Calculated bid for intent {intent.id}: Price {price}")
        return Bid(price=price,currency="PIN")

async def main():
    logging.basicConfig(level=logging.INFO)

    config = (
        ConfigBuilder()
        .with_subnet_id(os.getenv("SUBNET_ID")) #SubnetId where to run agent at
        .with_agent_id("financial-news-agent-001") #Agent ID
        
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS","localhost:8090")) #Matcher Address
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS","localhost:8090")) #Validator Address
        
        .with_capabilities("news-analyser", "financial-impact-predictor") #List of Capabilities of Your Agent

        .with_intent_types("news-analyser") #List of intent-types agent can access
        
        .with_private_key(os.getenv("PRIVATE_KEY")) 
        
        .build()
    )

    agent = SDK(config)
    
    agent.register_handler(FinancialNewsHandler())
    
    strategy = MyCustomBiddingStrategy()
    agent.register_bidding_strategy(strategy)
    
    # --- 3c. Start the agent ---
    logging.info(f"Starting agent: {agent.get_agent_id()} on subnet: {agent.get_subnet_id()}")
    await agent.start()

    # Run forever until stopped (e.g., with Ctrl+C)
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logging.info("Shutting down agent...")
        await agent.stop()
        logging.info("Agent stopped.")

if __name__ == "__main__":
    asyncio.run(main())