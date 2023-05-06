import json
from web3 import Web3
from eth_utils import to_bytes
import uuid
import secrets
from wallets import work_wallet_address, work_wallet_key

my_address = work_wallet_address
private_key = work_wallet_key
w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/aaa43cac77af4b51997508b731348839'))
token_address = '0x41E5E6045f91B61AACC99edca0967D518fB44CFB'
amount = 1000000000000000000

with open('UNI_abi.json') as f:
    abi = json.load(f)

uni_contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=abi)

with open('contract_jumper_abi.json') as f:
    abi = json.load(f)

bridge_contract_address = '0x1231deb6f5749ef6ce6943a275a1d3e7486f4eae'
bridge_contract = w3.eth.contract(address=Web3.to_checksum_address(bridge_contract_address), abi=abi)
transfer_for_id = secrets.token_hex(32)

transfer_id = to_bytes(hexstr=transfer_for_id)
bridge_data = (
    transfer_id,
    'hop',
    'testnet.jumper.exchange',
    Web3.to_checksum_address('0x0000000000000000000000000000000000000000'),
    Web3.to_checksum_address(token_address),
    Web3.to_checksum_address(my_address),
    amount,
    59140,
    False,
    False,
)
hop_data = (
    0,
    amount * 99 // 100,
    w3.eth.get_block('latest')['timestamp'] + 600,
    amount * 99 // 100,
    w3.eth.get_block('latest')['timestamp'] + 600,
    Web3.to_checksum_address('0xB47dE784aB8702eC35c5eAb225D6f6cE476DdD28'),
    0,
    100000000000000
)

nonce = w3.eth.get_transaction_count(my_address)
gas_price = w3.eth.gas_price
tx = bridge_contract.functions.startBridgeTokensViaHop(bridge_data, hop_data).build_transaction({
    'nonce': nonce,
    'gas': 1000000,
    'gasPrice': w3.to_wei('4000', 'gwei'),
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print('Transaction sent. Hash:', Web3.to_hex(tx_hash))
