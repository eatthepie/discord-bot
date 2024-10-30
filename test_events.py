# test_events.py
from web3 import Web3
from contract_abi import CONTRACT_ABI
import os
from dotenv import load_dotenv

load_dotenv()

def test_event_subscriptions():
    w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_NODE_URL')))
    contract = w3.eth.contract(
        address='0x043c9ae2764B5a7c2d685bc0262F8cF2f6D86008',
        abi=CONTRACT_ABI
    )
    
    # Get past events as a test
    block_number = w3.eth.block_number
    start_block = block_number - 1000  # Last 1000 blocks
    
    for event_name in ['TicketPurchased', 'DrawInitiated', 'RandomSet', 'VDFProofSubmitted', 'GamePrizePayoutInfo']:
        event = getattr(contract.events, event_name)
        print(f"\nTesting {event_name} events:")
        try:
            events = event.get_logs(fromBlock=start_block)
            print(f"Found {len(events)} events")
            if events:
                print("Sample event:", dict(events[0]))
        except Exception as e:
            print(f"Error getting {event_name} events:", e)

if __name__ == "__main__":
    test_event_subscriptions()