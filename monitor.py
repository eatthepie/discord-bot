import os
from web3 import Web3
import requests
import time
from datetime import datetime
import json
from eth_utils import to_checksum_address
import logging
from contract_abi import CONTRACT_ABI

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LotteryMonitor:
    def __init__(self):
        logger.info("Initializing LotteryMonitor...")
        
        self.node_url = os.getenv('ETH_NODE_URL')
        self.tickets_webhook = os.getenv('TICKETS_WEBHOOK_URL')
        self.events_webhook = os.getenv('EVENTS_WEBHOOK_URL')
        
        logger.info(f"ETH_NODE_URL configured: {'Yes' if self.node_url else 'No'}")
        logger.info(f"TICKETS_WEBHOOK configured: {'Yes' if self.tickets_webhook else 'No'}")
        logger.info(f"EVENTS_WEBHOOK configured: {'Yes' if self.events_webhook else 'No'}")
        
        if not all([self.node_url, self.tickets_webhook, self.events_webhook]):
            raise ValueError("Missing required environment variables")
            
        logger.info("Connecting to Ethereum node...")
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))
        
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to Ethereum node")
        
        logger.info("Successfully connected to Ethereum node")
        
        self.contract = self.w3.eth.contract(
            address=to_checksum_address('0x043c9ae2764B5a7c2d685bc0262F8cF2f6D86008'),
            abi=CONTRACT_ABI
        )
        
        self.last_processed_block = self.w3.eth.block_number
        logger.info(f"Starting from block {self.last_processed_block}")

    def format_eth(self, wei_amount):
        eth_amount = self.w3.from_wei(wei_amount, 'ether')
        return f"{eth_amount:.4f} ETH"

    def get_etherscan_link(self, address):
        return f"[{address[:6]}...{address[-4:]}](https://etherscan.io/address/{address})"

    def send_webhook(self, webhook_url, embed):
        try:
            payload = {"embeds": [embed]}
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            logger.info(f"Successfully sent webhook: {embed.get('title', 'No title')}")
            return True
        except Exception as e:
            logger.error(f"Failed to send webhook: {str(e)}")
            return False

    def get_events(self, event_name, from_block, to_block):
        """Helper function to get events with proper filter"""
        try:
            event = getattr(self.contract.events, event_name)
            event_filter = {
                'address': self.contract.address,
                'fromBlock': from_block,
                'toBlock': to_block
            }
            
            # Get the event signature
            if hasattr(event, 'event_abi'):
                event_signature_hex = self.w3.keccak(
                    text=f"{event.event_abi['name']}({','.join([arg['type'] for arg in event.event_abi['inputs']])})"
                ).hex()
                event_filter['topics'] = [event_signature_hex]
            
            logs = self.w3.eth.get_logs(event_filter)
            return [event.process_log(log) for log in logs]
        except Exception as e:
            logger.error(f"Error getting {event_name} events: {str(e)}")
            return []

    def handle_ticket_purchased(self, event):
        logger.info(f"Processing TicketPurchased event from block {event['blockNumber']}")
        player = event['args']['player']
        numbers = event['args']['numbers']
        etherball = event['args']['etherball']
        game_number = event['args']['gameNumber']

        embed = {
            "title": "🎫 New Ticket Purchased!",
            "color": 0x2ecc71,
            "fields": [
                {"name": "Player", "value": self.get_etherscan_link(player), "inline": False},
                {"name": "Game Number", "value": str(game_number), "inline": True},
                {"name": "Numbers", "value": f"{numbers[0]}-{numbers[1]}-{numbers[2]}", "inline": True},
                {"name": "Etherball", "value": str(etherball), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.send_webhook(self.tickets_webhook, embed)

    def handle_draw_initiated(self, event):
        """Handle DrawInitiated events"""
        embed = {
            "title": "🎲 Draw Initiated!",
            "color": 0x3498db,  # Blue
            "fields": [
                {"name": "Game Number", "value": str(event['args']['gameNumber']), "inline": True},
                {"name": "Target Block", "value": str(event['args']['targetSetBlock']), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.send_webhook(self.events_webhook, embed)

    def handle_random_set(self, event):
        """Handle RandomSet events"""
        embed = {
            "title": "🎲 RANDAO Value Set!",
            "color": 0x9b59b6,  # Purple
            "fields": [
                {"name": "Game Number", "value": str(event['args']['gameNumber']), "inline": True},
                {"name": "Random Value", "value": hex(event['args']['random']), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.send_webhook(self.events_webhook, embed)

    def handle_vdf_proof(self, event):
        """Handle VDFProofSubmitted events"""
        embed = {
            "title": "🔐 VDF Proof Submitted!",
            "color": 0xf1c40f,  # Gold
            "fields": [
                {"name": "Submitter", "value": self.get_etherscan_link(event['args']['submitter']), "inline": True},
                {"name": "Game Number", "value": str(event['args']['gameNumber']), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.send_webhook(self.events_webhook, embed)

    def handle_prize_info(self, event):
        """Handle GamePrizePayoutInfo events"""
        embed = {
            "title": "💰 Prize Pool Announced!",
            "color": 0xf1c40f,  # Gold
            "fields": [
                {"name": "Game Number", "value": str(event['args']['gameNumber']), "inline": False},
                {"name": "🥇 Gold Prize", "value": self.format_eth(event['args']['goldPrize']), "inline": True},
                {"name": "🥈 Silver Prize", "value": self.format_eth(event['args']['silverPrize']), "inline": True},
                {"name": "🥉 Bronze Prize", "value": self.format_eth(event['args']['bronzePrize']), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.send_webhook(self.events_webhook, embed)

    def process_events(self):
        """Process events from last checked block"""
        try:
            current_block = self.w3.eth.block_number
            if current_block > self.last_processed_block:
                logger.info(f"Processing blocks {self.last_processed_block + 1} to {current_block}")
                
                # Event types to monitor
                event_types = [
                    'TicketPurchased',
                    'DrawInitiated',
                    'RandomSet',
                    'VDFProofSubmitted',
                    'GamePrizePayoutInfo'
                ]

                for event_type in event_types:
                    events = self.get_events(event_type, self.last_processed_block + 1, current_block)
                    if events:
                        logger.info(f"Found {len(events)} {event_type} events")
                        for event in events:
                            if event_type == 'TicketPurchased':
                                self.handle_ticket_purchased(event)
                            elif event_type == 'DrawInitiated':
                                self.handle_draw_initiated(event)
                            elif event_type == 'RandomSet':
                                self.handle_random_set(event)
                            elif event_type == 'VDFProofSubmitted':
                                self.handle_vdf_proof(event)
                            elif event_type == 'GamePrizePayoutInfo':
                                self.handle_prize_info(event)

                self.last_processed_block = current_block
                
        except Exception as e:
            logger.error(f"Error processing events: {str(e)}", exc_info=True)

    def run(self):
        """Main loop"""
        logger.info("Starting main monitoring loop")
        while True:
            try:
                self.process_events()
                time.sleep(12)  # Average Ethereum block time
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}", exc_info=True)
                time.sleep(12)  # Still sleep on error

if __name__ == "__main__":
    try:
        monitor = LotteryMonitor()
        monitor.run()
    except Exception as e:
        logger.error(f"Failed to start monitor: {str(e)}", exc_info=True)
        raise