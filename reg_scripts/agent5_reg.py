# file: register_agent_5.py
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

from agent5 import StockAnalysisAgent

logging.basicConfig(level=logging.INFO)


OPENAI_API_KEY = os.getenv("OPENAI_API")

class StockAnalysisHandler(Handler):
    """
    Handles tasks for stock analysis.
    """
    def __init__(self, api_key):
        self.agent = StockAnalysisAgent(openai_api_key=api_key)
        logging.info("StockAnalysisHandler initialized.")

    async def execute(self, task: Task) -> Result:
        query = task.data.decode()
        logging.info(f"Task {task.id}: Executing stock analysis for: {query}")
        try:
            # Call the agent's main function
            analysis = self.agent.analyze(query)
            
            try:
                analysis_dict = analysis.__dict__
                serializable_analysis = {
                    "query": analysis.query.raw_query,
                    "ticker": analysis.query.ticker_symbol,
                    "prediction_current": analysis.prediction.current_price,
                    "prediction_future": analysis.prediction.predicted_price,
                    "recommendation": analysis.recommendation.value,
                    "reasoning": analysis.reasoning
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
    if not OPENAI_API_KEY:
        logging.error("OPENAI_API_KEY not set. Exiting.")
        return

    config = (
        ConfigBuilder()
        .with_subnet_id(os.getenv("SUBNET_ID")) #SubnetId where to run agent at
        .with_agent_id("financial-news-agent-001") #Agent ID
        
        .with_matcher_addr(os.getenv("MATCHER_ADDRESS","localhost:8090")) #Matcher Address
        .with_validator_addr(os.getenv("VALIDATOR_ADDRESS","localhost:8090")) #Validator Address
        .with_private_key(os.getenv("PRIVATE_KEY"))  # <-- Your Private Key

        .with_capabilities("stock-analysis", "price-prediction")
        .with_intent_types("stock-analysis") # For bidding
        
        .build()
    )

    agent = SDK(config)
    agent.register_handler(StockAnalysisHandler(api_key=OPENAI_API_KEY))
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