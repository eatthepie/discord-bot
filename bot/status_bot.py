import os
import asyncio
import discord
# import ssl # For local testing
# import certifi # For local testing
from web3 import Web3
from discord.ext import tasks
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure SSL context
# ssl_context = ssl.create_default_context(cafile=certifi.where()) # For local testing

# Load environment variables
load_dotenv()

# Configuration
ETH_NODE_URL = os.getenv('ETH_NODE_URL')
CONTRACT_ADDRESS = '0x043c9ae2764B5a7c2d685bc0262F8cF2f6D86008'
GAME_BOT_TOKEN = os.getenv('GAME_BOT_TOKEN')
PRIZE_BOT_TOKEN = os.getenv('PRIZE_BOT_TOKEN')
UPDATE_INTERVAL = 900  # 15 minutes in seconds

# Verify tokens exist
if not GAME_BOT_TOKEN or not PRIZE_BOT_TOKEN:
    raise ValueError("Missing bot tokens in .env file")

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))

# Contract ABI
CONTRACT_ABI = [
    {
        "inputs": [],
        "name": "currentGameNumber",
        "outputs": [{"type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"type": "uint256"}],
        "name": "gamePrizePool",
        "outputs": [{"type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Initialize contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

class StatusBot(discord.Client):
    def __init__(self, update_func, bot_type):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.update_func = update_func
        self.bot_type = bot_type
        self.last_value = None

    async def setup_hook(self):
        self.status_update.start()
        logger.info(f"{self.bot_type} Bot: Setup completed")

    @tasks.loop(seconds=UPDATE_INTERVAL)
    async def status_update(self):
        try:
            new_value = await self.update_func()
            
            if new_value != self.last_value:
                self.last_value = new_value
                for guild in self.guilds:
                    try:
                        await guild.me.edit(nick=new_value)
                        logger.info(f"{self.bot_type} Bot: Updated nickname to: {new_value} in {guild.name}")
                    except discord.errors.Forbidden:
                        logger.error(f"{self.bot_type} Bot: Missing permissions in {guild.name}")
                    except Exception as e:
                        logger.error(f"{self.bot_type} Bot: Error in {guild.name}: {str(e)}")
        except Exception as e:
            logger.error(f"{self.bot_type} Bot: Update error: {str(e)}")

    @status_update.before_loop
    async def before_status_update(self):
        await self.wait_until_ready()
        logger.info(f"{self.bot_type} Bot: Ready!")

async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)

async def get_game_number():
    """Query current game number from smart contract"""
    try:
        game_number = await run_in_executor(
            contract.functions.currentGameNumber().call
        )
        return f"Game #{game_number}"
    except Exception as e:
        logger.error(f"Error getting game number: {str(e)}")
        return "Game #Error"

async def get_prize_pool():
    """Query current prize pool from smart contract"""
    try:
        current_game = await run_in_executor(
            contract.functions.currentGameNumber().call
        )
        prize_pool_wei = await run_in_executor(
            contract.functions.gamePrizePool(current_game).call
        )
        prize_pool_eth = w3.from_wei(prize_pool_wei, 'ether')
        return f"Prize: {prize_pool_eth:.2f} ETH"
    except Exception as e:
        logger.error(f"Error getting prize pool: {str(e)}")
        return "Prize: Error"

async def main():
    try:
        game_bot = StatusBot(
            update_func=get_game_number,
            bot_type="Game"
        )
        
        prize_bot = StatusBot(
            update_func=get_prize_pool,
            bot_type="Prize"
        )

        await asyncio.gather(
            game_bot.start(GAME_BOT_TOKEN),
            prize_bot.start(PRIZE_BOT_TOKEN)
        )
    except Exception as e:
        logger.error(f"Error running bots: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received shutdown signal, closing bots...")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")