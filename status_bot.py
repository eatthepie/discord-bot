import os
import asyncio
import discord
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

# Load environment variables
load_dotenv()

# Configuration
ETH_NODE_URL = os.getenv('ETH_NODE_URL')
CONTRACT_ADDRESS = '0x043c9ae2764B5a7c2d685bc0262F8cF2f6D86008'
GAME_BOT_TOKEN = os.getenv('GAME_BOT_TOKEN')
PRIZE_BOT_TOKEN = os.getenv('PRIZE_BOT_TOKEN')
UPDATE_INTERVAL = 900  # 15 minutes in seconds

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))

# Updated Contract ABI to match your actual contract
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
    def __init__(self, update_func, bot_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_func = update_func
        self.bot_type = bot_type
        self.status_update.start()
        self.last_value = None

    async def setup_hook(self):
        pass

    @tasks.loop(seconds=UPDATE_INTERVAL)
    async def status_update(self):
        try:
            new_value = await self.update_func()
            
            # Only update if value has changed
            if new_value != self.last_value:
                self.last_value = new_value
                new_name = new_value
                
                for guild in self.guilds:
                    try:
                        await guild.me.edit(nick=new_name)
                        logger.info(f"{self.bot_type} Bot: Updated nickname to: {new_name} in {guild.name}")
                    except discord.errors.Forbidden:
                        logger.error(f"{self.bot_type} Bot: Failed to update nickname in {guild.name} - Missing permissions")
                    except Exception as e:
                        logger.error(f"{self.bot_type} Bot: Error updating nickname in {guild.name}: {str(e)}")
            else:
                logger.info(f"{self.bot_type} Bot: No update needed, value unchanged")
                
        except Exception as e:
            logger.error(f"{self.bot_type} Bot: Error in status update: {str(e)}")

    @status_update.before_loop
    async def before_status_update(self):
        await self.wait_until_ready()
        logger.info(f"{self.bot_type} Bot: Ready and waiting for first update")

async def get_game_number():
    """Query current game number from smart contract"""
    try:
        game_number = await asyncio.to_thread(
            contract.functions.currentGameNumber().call
        )
        return f"Game #{game_number}"
    except Exception as e:
        logger.error(f"Error getting game number: {str(e)}")
        return "Game #Error"

async def get_prize_pool():
    """Query current prize pool from smart contract"""
    try:
        # First get current game number
        current_game = await asyncio.to_thread(
            contract.functions.currentGameNumber().call
        )
        
        # Then get prize pool for current game
        prize_pool_wei = await asyncio.to_thread(
            contract.functions.gamePrizePool(current_game).call
        )
        
        prize_pool_eth = w3.from_wei(prize_pool_wei, 'ether')
        return f"Prize: {prize_pool_eth:.2f} ETH"
    except Exception as e:
        logger.error(f"Error getting prize pool: {str(e)}")
        return "Prize: Error"

async def validate_connection():
    """Validate Web3 connection and contract before starting bots"""
    try:
        if not w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")
        
        # Test contract calls
        await get_game_number()
        await get_prize_pool()
        
        logger.info("Successfully validated Web3 connection and contract calls")
        return True
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        return False

async def main():
    # Validate connection before starting bots
    if not await validate_connection():
        logger.error("Failed to validate connection. Exiting...")
        return

    # Create bot instances with their respective update functions
    game_bot = StatusBot(
        update_func=get_game_number,
        bot_type="Game",
        intents=discord.Intents.default()
    )
    
    prize_bot = StatusBot(
        update_func=get_prize_pool,
        bot_type="Prize",
        intents=discord.Intents.default()
    )

    try:
        # Run both bots concurrently
        await asyncio.gather(
            game_bot.start(GAME_BOT_TOKEN),
            prize_bot.start(PRIZE_BOT_TOKEN)
        )
    except Exception as e:
        logger.error(f"Error running bots: {str(e)}")
    finally:
        # Cleanup
        if not game_bot.is_closed():
            await game_bot.close()
        if not prize_bot.is_closed():
            await prize_bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received shutdown signal, closing bots...")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")