from web3 import Web3
import json
from wallets import work_wallet_address, work_wallet_key

my_address = work_wallet_address
private_key = work_wallet_key
w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/aaa43cac77af4b51997508b731348839'))
token_address = '0xfad6367E97217cC51b4cd838Cc086831f81d38C2'
amount = 100 * 10**6
with open('USDT_abi.json') as f:
    abi = json.load(f)

token_contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=abi)
tx = token_contract.functions.approve(my_address, amount).build_transaction({
    'from': my_address,
    'gas': 200000,
    'gasPrice': w3.to_wei('4000', 'gwei'),
    'nonce': w3.eth.get_transaction_count(my_address)
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print('Tx hash:', Web3.to_hex(tx_hash))

