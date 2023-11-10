from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv()
infura_api_key = os.getenv('APIKEY')

if not infura_api_key:
    raise ValueError("The 'APIKEY' environment variable is not set.")

infura_url = f'https://mainnet.infura.io/v3/{infura_api_key}'
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    print("Connected to Ethereum network!")
else:
    print("Failed to connect to Ethereum network.")

# Handle new block
def handle_block(block_number):
    block = web3.eth.get_block(block_number, full_transactions=True)
    for tx in block.transactions:
        # Check if 'to' address is None, indicating contract creation
        if tx['to'] is None: # Comment out this line to listen for all events
            tx_hash = tx['hash'].hex()
            etherscan_link = f"https://etherscan.io/tx/{tx_hash}"
            print(f"New contract created with hash: [{tx_hash}]({etherscan_link})")

# Subscribe to new blocks
def main():
    block_filter = web3.eth.filter('latest')
    while True:
        for block_number in block_filter.get_new_entries():
            handle_block(block_number)

if __name__ == "__main__":
    main()
