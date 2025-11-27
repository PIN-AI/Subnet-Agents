# file: register_agent_6.py
import asyncio
import logging
import json
import os
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


from agent6 import PolymarketRedditAgent

logging.basicConfig(level=logging.INFO)

POLYMARKET_API_KEY = os.getenv("POLYMARKET_API_KEY")
REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
USER_AGENT = "polymarket-agent/1.0"


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
            
            trade_calls_json = json.dumps(
                [call.model_dump() for call in trade_calls], 
                indent=2
            )

            logging.info(f"Task {task.id}: Processed successfully.")
            return Result(
                data=trade_calls_json.encode(),
                success=True
            )
        except Exception as e:
            logging.error(f"Task {task.id}: Failed to process: {e}")
            return Result(data=b"", success=False, error=str(e))

class SimpleBiddingStrategy(BiddingStrategy):
    """A simple strategy that bids 100 on 'corporate-analysis' intents."""
    def __init__(self):
        logging.info(f"CustomBiddingStrategy initialized")

    def should_bid(self, intent: Intent) -> bool:
        return intent.type == "corporate-analysis"

    def calculate_bid(self, intent: Intent):
        price = 10
        return Bid(price=price,currency="PIN")


async def main():
    if not all([POLYMARKET_API_KEY, REDDIT_ID, REDDIT_SECRET]):
        logging.error("Missing API keys for Polymarket/Reddit. Exiting.")
        return

    config = (
        ConfigBuilder()
        .with_subnet_id(os.getenv("SUBNET_ID")) #SubnetId where to run agent at
        .with_agent_id("financial-news-agent-001") #Agent ID
        
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS","localhost:8090")) #Matcher Address
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS","localhost:8090")) #Validator Address
        .with_private_key(os.getenv("PRIVATE_KEY"))  # <-- Your Private Key

        .with_capabilities("polymarket-analysis", "reddit-sentiment")
        .with_intent_types("polymarket-analysis") # For bidding

        .build()
    )

    agent = SDK(config)
    agent.register_handler(PolymarketHandler(
        poly_key=POLYMARKET_API_KEY,
        reddit_id=REDDIT_ID,
        reddit_secret=REDDIT_SECRET,
        user_agent=USER_AGENT
    ))
    agent.register_bidding_strategy(SimpleBiddingStrategy())
    
    logging.info(f"Starting agent: {agent.get_agent_id()}")
    await agent.start()

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logging.info("Shutting down agent...")
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())