import os
import time
from datetime import datetime
import json
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any, Optional

from web3 import Web3
from eth_utils import to_checksum_address
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from contract_abi import CONTRACT_ABI

# Load environment variables
load_dotenv()

# Constants
CONTRACT_ADDRESS = '0x043c9ae2764B5a7c2d685bc0262F8cF2f6D86008'
BLOCK_TIME = 12  # seconds
BLOCKS_PER_HOUR = 3600 // BLOCK_TIME

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebhookManager:
    def __init__(self, tickets_webhook: str, events_webhook: str):
        self.tickets_webhook = tickets_webhook
        self.events_webhook = events_webhook
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a session with retry mechanism for webhooks"""
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
        return session

    def send_webhook(self, webhook_url: str, embed: Dict[str, Any]) -> bool:
        """Send webhook with basic retry mechanism"""
        try:
            payload = {"embeds": [embed]}
            response = self.session.post(webhook_url, json=payload)
            response.raise_for_status()
            logger.info(f"Successfully sent webhook: {embed.get('title', 'No title')}")
            return True
        except Exception as e:
            logger.error(f"Failed to send webhook: {str(e)}")
            return False

class RateLimiter:
    def __init__(self, max_requests_per_day: int):
        self.max_requests_per_day = max_requests_per_day
        self.request_counter = 0
        self.request_counter_reset = datetime.now()

    def check_limit(self) -> bool:
        """Check if we're within our conservative rate limits"""
        now = datetime.now()
        
        if (now - self.request_counter_reset).days >= 1:
            self.request_counter = 0
            self.request_counter_reset = now
            
        if self.request_counter >= self.max_requests_per_day:
            wait_time = 24 - (now - self.request_counter_reset).seconds / 3600
            logger.warning(f"Approaching daily rate limit. Waiting {wait_time:.2f} hours...")
            return False
        return True

    def increment(self) -> None:
        """Increment the request counter"""
        self.request_counter += 1

class EventHandler:
    def __init__(self, w3: Web3, webhook_manager: WebhookManager):
        self.w3 = w3
        self.webhook_manager = webhook_manager

    def get_etherscan_link(self, address: str) -> str:
        return f"[{address[:6]}...{address[-4:]}](https://etherscan.io/address/{address})"

    def format_eth(self, wei_amount: int) -> str:
        eth_amount = self.w3.from_wei(wei_amount, 'ether')
        return f"{eth_amount:.4f} ETH"

    def handle_ticket_purchased(self, event: Dict[str, Any]) -> None:
        player = event['args']['player']
        numbers = event['args']['numbers']
        etherball = event['args']['etherball']
        game_number = event['args']['gameNumber']
        tx_hash = event['transactionHash'].hex()
        tx_link = f"[View Transaction](https://etherscan.io/tx/{tx_hash})"

        embed = {
            "title": "🎟️ New Ticket Purchased!",
            "color": 0x2ecc71,
            "fields": [
                {"name": "Player", "value": self.get_etherscan_link(player), "inline": False},
                {"name": "Transaction", "value": tx_link, "inline": False},
                {"name": "Game Number", "value": str(game_number), "inline": True},
                {"name": "Numbers", "value": f"{numbers[0]}-{numbers[1]}-{numbers[2]}-{etherball}", "inline": True}
            ]
        }

        self.webhook_manager.send_webhook(self.webhook_manager.tickets_webhook, embed)

    def handle_draw_initiated(self, event: Dict[str, Any]) -> None:
        tx_hash = event['transactionHash'].hex()
        tx_link = f"[View Transaction](https://etherscan.io/tx/{tx_hash})"

        embed = {
            "title": "🎲 Draw Initiated!",
            "color": 0x3498db,
            "fields": [
                {"name": "Transaction", "value": tx_link, "inline": False},
                {"name": "Game Number", "value": str(event['args']['gameNumber']), "inline": True},
                {"name": "Target Block", "value": str(event['args']['targetSetBlock']), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.webhook_manager.send_webhook(self.webhook_manager.events_webhook, embed)

    def handle_random_set(self, event: Dict[str, Any]) -> None:
        tx_hash = event['transactionHash'].hex()
        tx_link = f"[View Transaction](https://etherscan.io/tx/{tx_hash})"

        embed = {
            "title": "🎲 RANDAO Value Set!",
            "color": 0x9b59b6,
            "fields": [
                {"name": "Transaction", "value": tx_link, "inline": False},
                {"name": "Game Number", "value": str(event['args']['gameNumber']), "inline": True},
                {"name": "Random Value", "value": hex(event['args']['random']), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.webhook_manager.send_webhook(self.webhook_manager.events_webhook, embed)

    def handle_vdf_proof_submitted(self, event: Dict[str, Any]) -> None:
        tx_hash = event['transactionHash'].hex()
        tx_link = f"[View Transaction](https://etherscan.io/tx/{tx_hash})"

        embed = {
            "title": "🔐 VDF Proof Submitted!",
            "color": 0xf1c40f,
            "fields": [
                {"name": "Transaction", "value": tx_link, "inline": False},
                {"name": "Submitter", "value": self.get_etherscan_link(event['args']['submitter']), "inline": True},
                {"name": "Game Number", "value": str(event['args']['gameNumber']), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.webhook_manager.send_webhook(self.webhook_manager.events_webhook, embed)

    def handle_game_prize_payout_info(self, event: Dict[str, Any]) -> None:
        tx_hash = event['transactionHash'].hex()
        tx_link = f"[View Transaction](https://etherscan.io/tx/{tx_hash})"

        embed = {
            "title": "💰 Prize Pool Announced!",
            "color": 0xf1c40f,
            "fields": [
                {"name": "Transaction", "value": tx_link, "inline": False},
                {"name": "Game Number", "value": str(event['args']['gameNumber']), "inline": False},
                {"name": "🥇 Gold Prize", "value": self.format_eth(event['args']['goldPrize']), "inline": True},
                {"name": "🥈 Silver Prize", "value": self.format_eth(event['args']['silverPrize']), "inline": True},
                {"name": "🥉 Bronze Prize", "value": self.format_eth(event['args']['bronzePrize']), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.webhook_manager.send_webhook(self.webhook_manager.events_webhook, embed)

class LotteryMonitor:
    def __init__(self):
        logger.info("Initializing LotteryMonitor...")
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.w3 = self._initialize_web3()
        self.contract = self._initialize_contract()
        self.webhook_manager = WebhookManager(
            self.config['tickets_webhook'],
            self.config['events_webhook']
        )
        self.rate_limiter = RateLimiter(max_requests_per_day=1000)
        self.event_handler = EventHandler(self.w3, self.webhook_manager)
        
        # Initialize state
        self.last_processed_block = self._get_safe_starting_block()
        logger.info(f"Starting from block {self.last_processed_block}")

    def _load_config(self) -> Dict[str, str]:
        """Load and validate configuration from environment variables"""
        config = {
            'node_url': os.getenv('ETH_NODE_URL'),
            'tickets_webhook': os.getenv('TICKETS_WEBHOOK_URL'),
            'events_webhook': os.getenv('EVENTS_WEBHOOK_URL')
        }
        
        if not all(config.values()):
            raise ValueError("Missing required environment variables")
            
        return config

    def _initialize_web3(self) -> Web3:
        """Initialize Web3 connection"""
        w3 = Web3(Web3.HTTPProvider(self.config['node_url']))
        if not w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")
        logger.info("Successfully connected to Ethereum node")
        return w3

    def _initialize_contract(self) -> Any:
        """Initialize the contract instance"""
        return self.w3.eth.contract(
            address=to_checksum_address(CONTRACT_ADDRESS),
            abi=CONTRACT_ABI
        )

    def _get_safe_starting_block(self) -> int:
        """Get a safe starting block number"""
        try:
            current_block = self.w3.eth.block_number
            return max(current_block - BLOCKS_PER_HOUR, 0)
        except Exception as e:
            logger.error(f"Error getting current block: {str(e)}")
            return 0

    def get_events(self, event_name: str, from_block: int, to_block: int) -> List[Dict[str, Any]]:
        """Get events with rate limiting"""
        if not self.rate_limiter.check_limit():
            return []
            
        try:
            event = getattr(self.contract.events, event_name)
            event_filter = {
                'address': self.contract.address,
                'fromBlock': from_block,
                'toBlock': to_block
            }
            
            if hasattr(event, 'event_abi'):
                event_signature_hex = self.w3.keccak(
                    text=f"{event.event_abi['name']}({','.join([arg['type'] for arg in event.event_abi['inputs']])})"
                ).hex()
                event_filter['topics'] = [event_signature_hex]
            
            self.rate_limiter.increment()
            logs = self.w3.eth.get_logs(event_filter)
            return [event.process_log(log) for log in logs]
            
        except Exception as e:
            logger.error(f"Error getting {event_name} events: {str(e)}")
            return []

    def process_events(self) -> None:
        """Process events in batches"""
        try:
            if not self.rate_limiter.check_limit():
                logger.info("Rate limit approached, skipping this check")
                return

            current_block = self.w3.eth.block_number
            self.rate_limiter.increment()

            if current_block <= self.last_processed_block:
                return

            blocks_per_batch = 60  # ~1 minute worth of blocks
            start_block = self.last_processed_block + 1
            
            while start_block <= current_block:
                end_block = min(start_block + blocks_per_batch - 1, current_block)
                logger.info(f"Processing blocks {start_block} to {end_block}")

                event_types = {
                    'TicketPurchased': 'ticket_purchased',
                    'DrawInitiated': 'draw_initiated',
                    'RandomSet': 'random_set',
                    'VDFProofSubmitted': 'vdf_proof_submitted',
                    'GamePrizePayoutInfo': 'game_prize_payout_info'
                }

                for event_type, handler_name in event_types.items():
                    events = self.get_events(event_type, start_block, end_block)
                    if events:
                        logger.info(f"Found {len(events)} {event_type} events")
                        handler = getattr(self.event_handler, f"handle_{handler_name}")
                        for event in events:
                            handler(event)

                self.last_processed_block = end_block
                start_block = end_block + 1
                time.sleep(2)  # Add delay between batches

        except Exception as e:
            logger.error(f"Error processing events: {str(e)}", exc_info=True)

    def run(self) -> None:
        """Main monitoring loop"""
        logger.info("Starting main monitoring loop")
        check_interval = 600  # 10 minutes
        
        while True:
            try:
                start_time = time.time()
                self.process_events()
                
                elapsed = time.time() - start_time
                sleep_time = max(check_interval - elapsed, 0)
                
                logger.info(f"Processed events. Next check in {sleep_time/60:.1f} minutes")
                time.sleep(sleep_time)
                
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}", exc_info=True)
                time.sleep(check_interval)

def main():
    try:
        monitor = LotteryMonitor()
        monitor.run()
    except Exception as e:
        logger.error(f"Failed to start monitor: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()