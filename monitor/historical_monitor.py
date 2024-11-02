# run this with python historical-monitor.py --start-block [START_BLOCK] --end-block [END_BLOCK]

import os
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any, Optional, Tuple

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
BATCH_SIZE = 1000  # Number of blocks to process in each batch

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
        
        # Add counters for monitoring
        self.webhook_counts = {
            'tickets': 0,
            'events': 0
        }

    def _create_session(self) -> requests.Session:
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
        try:
            payload = {"embeds": [embed]}
            response = self.session.post(webhook_url, json=payload)
            response.raise_for_status()
            
            # Update counters
            if webhook_url == self.tickets_webhook:
                self.webhook_counts['tickets'] += 1
            else:
                self.webhook_counts['events'] += 1
                
            logger.info(f"Successfully sent webhook: {embed.get('title', 'No title')}")
            return True
        except Exception as e:
            logger.error(f"Failed to send webhook: {str(e)}")
            return False

    def get_stats(self) -> Dict[str, int]:
        return self.webhook_counts

class EventHandler:
    def __init__(self, w3: Web3, webhook_manager: WebhookManager):
        self.w3 = w3
        self.webhook_manager = webhook_manager
        self.event_counts: Dict[str, int] = {
            'TicketPurchased': 0,
            'DrawInitiated': 0,
            'RandomSet': 0,
            'VDFProofSubmitted': 0,
            'GamePrizePayoutInfo': 0
        }

    def get_etherscan_link(self, address: str) -> str:
        return f"[{address[:6]}...{address[-4:]}](https://etherscan.io/address/{address})"

    def format_eth(self, wei_amount: int) -> str:
        eth_amount = self.w3.from_wei(wei_amount, 'ether')
        return f"{eth_amount:.4f} ETH"

    def handle_ticket_purchased(self, event: Dict[str, Any]) -> None:
        self.event_counts['TicketPurchased'] += 1
        player = event['args']['player']
        numbers = event['args']['numbers']
        etherball = event['args']['etherball']
        game_number = event['args']['gameNumber']
        tx_hash = event['transactionHash'].hex()
        block_number = event['blockNumber']
        tx_link = f"[View Transaction](https://etherscan.io/tx/{tx_hash})"

        embed = {
            "title": f"🎟️ Historical Ticket Purchase (Block {block_number})",
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

    def get_stats(self) -> Dict[str, int]:
        return self.event_counts

class HistoricalMonitor:
    def __init__(self, start_block: int, end_block: int):
        logger.info("Initializing HistoricalMonitor...")
        
        # Store block range
        self.start_block = start_block
        self.end_block = end_block
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.w3 = self._initialize_web3()
        self.contract = self._initialize_contract()
        self.webhook_manager = WebhookManager(
            self.config['tickets_webhook'],
            self.config['events_webhook']
        )
        self.event_handler = EventHandler(self.w3, self.webhook_manager)
        
        # Initialize statistics
        self.blocks_processed = 0
        self.start_time = datetime.now()

    def _load_config(self) -> Dict[str, str]:
        config = {
            'node_url': os.getenv('ETH_NODE_URL'),
            'tickets_webhook': os.getenv('TICKETS_WEBHOOK_URL'),
            'events_webhook': os.getenv('EVENTS_WEBHOOK_URL')
        }
        
        if not all(config.values()):
            raise ValueError("Missing required environment variables")
            
        return config

    def _initialize_web3(self) -> Web3:
        w3 = Web3(Web3.HTTPProvider(self.config['node_url']))
        if not w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")
        logger.info("Successfully connected to Ethereum node")
        return w3

    def _initialize_contract(self) -> Any:
        return self.w3.eth.contract(
            address=to_checksum_address(CONTRACT_ADDRESS),
            abi=CONTRACT_ABI
        )

    def get_events(self, event_name: str, from_block: int, to_block: int) -> List[Dict[str, Any]]:
        try:
            event = getattr(self.contract.events, event_name)
            
            # Get all logs for the specified block range
            logs = self.w3.eth.get_logs({
                'address': self.contract.address,
                'fromBlock': from_block,
                'toBlock': to_block
            })
            
            # Process logs
            processed_events = []
            for log in logs:
                try:
                    # Try to process each log
                    processed_event = event().process_receipt({
                        'logs': [log]
                    })
                    if processed_event:
                        processed_events.extend(processed_event)
                except Exception as e:
                    # Skip logs that don't match this event
                    continue
                    
            return processed_events
                
        except Exception as e:
            logger.error(f"Error getting {event_name} events: {str(e)}")
            return []

    def print_progress(self, current_block: int) -> None:
        self.blocks_processed = current_block - self.start_block + 1
        progress = (self.blocks_processed / (self.end_block - self.start_block + 1)) * 100
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        blocks_per_second = self.blocks_processed / elapsed_time if elapsed_time > 0 else 0
        
        logger.info(
            f"Progress: {progress:.2f}% | "
            f"Blocks: {self.blocks_processed}/{self.end_block - self.start_block + 1} | "
            f"Speed: {blocks_per_second:.2f} blocks/s"
        )

    def print_final_stats(self) -> None:
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        event_stats = self.event_handler.get_stats()
        webhook_stats = self.webhook_manager.get_stats()
        
        logger.info("\n=== Final Statistics ===")
        logger.info(f"Total blocks processed: {self.blocks_processed}")
        logger.info(f"Total time: {elapsed_time:.2f} seconds")
        logger.info(f"Average speed: {self.blocks_processed / elapsed_time:.2f} blocks/s")
        logger.info("\nEvents found:")
        for event_type, count in event_stats.items():
            logger.info(f"  {event_type}: {count}")
        logger.info("\nWebhooks sent:")
        for webhook_type, count in webhook_stats.items():
            logger.info(f"  {webhook_type}: {count}")

    def process_events(self) -> None:
        current_block = self.start_block
        
        while current_block <= self.end_block:
            batch_end = min(current_block + BATCH_SIZE - 1, self.end_block)
            logger.info(f"Processing blocks {current_block} to {batch_end}")

            event_types = {
                'TicketPurchased': 'ticket_purchased',
                'DrawInitiated': 'draw_initiated',
                'RandomSet': 'random_set',
                'VDFProofSubmitted': 'vdf_proof_submitted',
                'GamePrizePayoutInfo': 'game_prize_payout_info'
            }

            for event_type, handler_name in event_types.items():
                events = self.get_events(event_type, current_block, batch_end)
                if events:
                    logger.info(f"Found {len(events)} {event_type} events")
                    handler = getattr(self.event_handler, f"handle_{handler_name}")
                    for event in events:
                        handler(event)

            self.print_progress(batch_end)
            current_block = batch_end + 1
            time.sleep(1)  # Rate limiting

        self.print_final_stats()

def main():
    parser = argparse.ArgumentParser(description='Process historical lottery events')
    parser.add_argument('--start-block', type=int, required=True, help='Starting block number')
    parser.add_argument('--end-block', type=int, required=True, help='Ending block number')
    args = parser.parse_args()

    try:
        monitor = HistoricalMonitor(args.start_block, args.end_block)
        monitor.process_events()
    except Exception as e:
        logger.error(f"Failed to process historical events: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()