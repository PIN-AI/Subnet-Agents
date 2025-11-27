# file: register_agent_2.py
import asyncio
import logging
import json
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
import os


from agents_a2a.agent2 import run_financial_analysis


logging.basicConfig(level=logging.INFO)

class CorporateAnalysisHandler(Handler):
    """
    Handles tasks for corporate financial analysis.
    """
    async def execute(self, task: Task) -> Result:
        query = task.data.decode()
        logging.info(f"Task {task.id}: Executing corporate analysis for: {query}")
        try:
            # Call the agent's main function
            report = run_financial_analysis(query)
            
            report_json = json.dumps(report, indent=2)

            logging.info(f"Task {task.id}: Processed successfully.")
            return Result(
                data=report_json.encode(),
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
    config = (
        ConfigBuilder()
        .with_subnet_id(os.getenv("SUBNET_ID")) #SubnetId where to run agent at
        .with_agent_id("financial-news-agent-001") #Agent ID
        
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS","localhost:8090")) #Matcher Address
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS","localhost:8090")) #Validator Address
        .with_private_key(os.getenv("PRIVATE_KEY"))  # <-- Your Private Key

        .with_capabilities("corporate-analysis", "financial-report")
        .with_intent_types("corporate-analysis") # For bidding

        .build()
    )

    agent = SDK(config)
    agent.register_handler(CorporateAnalysisHandler())
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