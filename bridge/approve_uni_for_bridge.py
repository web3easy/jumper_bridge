import json
from web3 import Web3
from eth_utils import to_bytes
from wallets import work_wallet_address, work_wallet_key

my_address = work_wallet_address
private_key = work_wallet_key
w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/aaa43cac77af4b51997508b731348839'))
token_address = '0x41E5E6045f91B61AACC99edca0967D518fB44CFB'
amount = 1000000000000000000

with open('UNI_abi.json') as f:
    abi = json.load(f)

uni_contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=abi)
spender = Web3.to_checksum_address('0x1231deb6f5749ef6ce6943a275a1d3e7486f4eae')
approve_amount = amount

nonce = w3.eth.get_transaction_count(my_address)
gas_price = w3.eth.gas_price
approve_tx = uni_contract.functions.approve(spender, approve_amount).build_transaction({
    'nonce': nonce,
    'gas': 1000000,
    'gasPrice': w3.to_wei('4000', 'gwei'),
})

signed_approve_tx = w3.eth.account.sign_transaction(approve_tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
print('Approve transaction sent. Hash:', Web3.to_hex(tx_hash))
