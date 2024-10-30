# historical_monitor.py
import os
from web3 import Web3
import requests
import time
from datetime import datetime
import json
from eth_utils import to_checksum_address
from dotenv import load_dotenv
from contract_abi import CONTRACT_ABI

class HistoricalLotteryMonitor:
    def __init__(self, start_block=None, end_block=None, chunk_size=1000):
        load_dotenv()
        
        node_url = os.getenv('ETH_NODE_URL')
        if not node_url:
            raise ValueError("ETH_NODE_URL environment variable is not set")
            
        self.w3 = Web3(Web3.HTTPProvider(node_url))
        
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to Ethereum node at {node_url}")
            
        self.contract = self.w3.eth.contract(
            address=to_checksum_address('0x043c9ae2764B5a7c2d685bc0262F8cF2f6D86008'),
            abi=CONTRACT_ABI
        )
        
        self.tickets_webhook = os.getenv('TICKETS_WEBHOOK_URL')
        self.events_webhook = os.getenv('EVENTS_WEBHOOK_URL')
        
        if not self.tickets_webhook or not self.events_webhook:
            raise ValueError("Webhook URLs are not properly set in environment variables")
        
        self.start_block = start_block or self.w3.eth.block_number - 1000
        self.end_block = end_block or self.w3.eth.block_number
        self.chunk_size = chunk_size
        
        print(f"Will scan blocks from {self.start_block} to {self.end_block} in chunks of {self.chunk_size}")

    def process_chunk(self, start_block, end_block):
        events_config = {
            'TicketPurchased': (self.contract.events.TicketPurchased, self.handle_ticket_purchased, "Ticket Purchase"),
            'DrawInitiated': (self.contract.events.DrawInitiated, self.handle_draw_initiated, "Draw Initiation"),
            'RandomSet': (self.contract.events.RandomSet, self.handle_random_set, "Random Set"),
            'VDFProofSubmitted': (self.contract.events.VDFProofSubmitted, self.handle_vdf_proof, "VDF Proof"),
            'GamePrizePayoutInfo': (self.contract.events.GamePrizePayoutInfo, self.handle_prize_info, "Prize Info")
        }

        print(f"\nProcessing blocks {start_block} to {end_block}")
        for event_name, (event_obj, handler, description) in events_config.items():
            try:
                events = event_obj.get_logs(fromBlock=start_block, toBlock=end_block)
                if events:
                    print(f"Found {len(events)} {event_name} events")
                    for event in events:
                        block_number = event['blockNumber']
                        print(f"Processing {event_name} from block {block_number}")
                        handler(event)
                        # Add small delay to avoid Discord rate limits
                        time.sleep(1)
            except Exception as e:
                print(f"Error processing {event_name} events in chunk: {e}")

    def process_historical_events(self):
        current_block = self.start_block
        
        while current_block < self.end_block:
            chunk_end = min(current_block + self.chunk_size, self.end_block)
            try:
                self.process_chunk(current_block, chunk_end)
            except Exception as e:
                print(f"Error processing chunk {current_block} to {chunk_end}: {e}")
            
            current_block = chunk_end + 1
            # Add delay between chunks
            time.sleep(2)
    def format_eth(self, wei_amount):
        eth_amount = self.w3.from_wei(wei_amount, 'ether')
        return f"{eth_amount:.4f} ETH"

    def get_etherscan_link(self, address):
        return f"[{address[:6]}...{address[-4:]}](https://etherscan.io/address/{address})"

    def send_webhook(self, webhook_url, embed):
        """Send Discord webhook with retry logic"""
        payload = {"embeds": [embed]}
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(webhook_url, json=payload)
                if response.status_code == 429:  # Rate limited
                    retry_after = response.json().get('retry_after', 5)
                    print(f"Rate limited, waiting {retry_after}ms")
                    time.sleep(retry_after / 1000)
                    continue
                response.raise_for_status()
                return True
            except Exception as e:
                print(f"Webhook error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                continue
        return False

    # Event handlers remain the same as in the original monitor
    def handle_ticket_purchased(self, event):
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
                {"name": "Etherball", "value": str(etherball), "inline": True},
                {"name": "Block", "value": str(event['blockNumber']), "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.send_webhook(self.tickets_webhook, embed)

    def handle_draw_initiated(self, event):
        embed = {
            "title": "🎲 Draw Initiated!",
            "color": 0x3498db,
            "fields": [
                {"name": "Game Number", "value": str(event['args']['gameNumber']), "inline": True},
                {"name": "Target Block", "value": str(event['args']['targetSetBlock']), "inline": True},
                {"name": "Block", "value": str(event['blockNumber']), "inline": True}
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
        """Process all events from last checked block"""
        try:
            current_block = self.w3.eth.block_number
            if current_block > self.last_processed_block:
                # Get events
                events = {
                    'TicketPurchased': self.contract.events.TicketPurchased.get_logs(fromBlock=self.last_processed_block + 1),
                    'DrawInitiated': self.contract.events.DrawInitiated.get_logs(fromBlock=self.last_processed_block + 1),
                    'RandomSet': self.contract.events.RandomSet.get_logs(fromBlock=self.last_processed_block + 1),
                    'VDFProofSubmitted': self.contract.events.VDFProofSubmitted.get_logs(fromBlock=self.last_processed_block + 1),
                    'GamePrizePayoutInfo': self.contract.events.GamePrizePayoutInfo.get_logs(fromBlock=self.last_processed_block + 1)
                }

                # Process events
                handlers = {
                    'TicketPurchased': self.handle_ticket_purchased,
                    'DrawInitiated': self.handle_draw_initiated,
                    'RandomSet': self.handle_random_set,
                    'VDFProofSubmitted': self.handle_vdf_proof,
                    'GamePrizePayoutInfo': self.handle_prize_info
                }

                for event_name, event_list in events.items():
                    for event in event_list:
                        handlers[event_name](event)

                self.last_processed_block = current_block
                
        except Exception as e:
            print(f"Error processing events: {e}")

    def run(self):
        """Main loop"""
        print(f"Starting monitoring from block {self.last_processed_block}")
        while True:
            self.process_events()
            time.sleep(12)  # Average Ethereum block time

if __name__ == "__main__":
    # Example: Process events from the last 1000 blocks
    # latest_block = Web3(Web3.HTTPProvider(os.getenv('ETH_NODE_URL'))).eth.block_number
    # start_block = latest_block - 1000

    # monitor = HistoricalLotteryMonitor(start_block=start_block, end_block=latest_block)
    # monitor.process_historical_events()

    # print(f"Processing events from block {start_block} to {latest_block}")

    # Example: Process specific range in chunks
    monitor = HistoricalLotteryMonitor(
        start_block=21072190,
        end_block=21079930,
        chunk_size=100  # Adjust this if still too large
    )
    monitor.process_historical_events()