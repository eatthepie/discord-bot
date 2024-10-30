# test_connection.py
from web3 import Web3
from dotenv import load_dotenv
import os

def test_connection():
    load_dotenv()  # Load environment variables
    
    # Get node URL from environment
    node_url = os.getenv('ETH_NODE_URL')
    print(f"Using node URL: {node_url}")
    
    try:
        # Initialize Web3
        w3 = Web3(Web3.HTTPProvider(node_url))
        
        # Test connection
        is_connected = w3.is_connected()
        print(f"Connection successful: {is_connected}")
        
        if is_connected:
            # Get some basic info
            block_number = w3.eth.block_number
            print(f"Current block number: {block_number}")
            
            # Test contract connection
            contract_address = "0x043c9ae2764B5a7c2d685bc0262F8cF2f6D86008"
            code = w3.eth.get_code(contract_address)
            print(f"Contract exists: {len(code) > 0}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_connection()