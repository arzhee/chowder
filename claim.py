from dotenv import load_dotenv
from web3 import Web3
import json
import os
import requests
import sys
import time

path = os.path.dirname(os.path.abspath(__file__))

rpc = 'https://polygon-rpc.com'

load_dotenv(dotenv_path = path + '/.env')
me = os.getenv('OTTERCLAM_ADDRESS')
key = os.getenv('OTTERCLAM_PRIVATE')

link = 'https://api.debank.com/chain/'
link += 'gas_price_dict_v2?chain=matic'
data = requests.get(link).json()
price = int(data['data']['fast']['price'])

w3 = Web3(Web3.HTTPProvider(rpc))
me = Web3.toChecksumAddress(me)

notes = {}
notes['014-sfhand'] = '0xC713af03353710EA37DF849237E32a936a63cBbd'
notes['028-frhand'] = '0x7C1a1C1e540E6c6F59F1748C3C2Edf39f8Cc06ee'
notes['028-sfhand'] = '0x03883Df947Af7C0BE2aCe9163489fa85A9947008'
notes['090-sfhand'] = '0x5a30229BFbe5A22343aE67D4C077c101768Fd757'
notes['090-sthand'] = '0xBe982E164402970da7C72083FB8D5FcdeF751DfA'
notes['180-dmhand'] = '0x831725bD8c8d2B9e75b872649f146F88e8A92b36'
notes['180-sfhand'] = '0x931f0857130bcd221D30C06d80aD98affe3Aa526'

lake = '0xc67abda25d0421fe9dc1afd64183b179a426a256'
lake = Web3.toChecksumAddress(lake)
abi = json.loads(open(path + '/lake.json').read())
lake = w3.eth.contract(address = lake, abi = abi)
epoch = lake.functions.epoch().call()

for name, note in notes.items():
    print(name, note)

    note = address = Web3.toChecksumAddress(note)
    file = open(path + '/notes/' + name + '.json')
    abi = json.loads(file.read())
    note = w3.eth.contract(address = note, abi = abi)

    items = note.functions.balanceOf(me).call()
    vaults = []

    for i in range(items):
        vault = note.functions.tokenOfOwnerByIndex(me, i).call()

        pearl = lake.functions.reward(address, vault).call()

        print('Note #' + str(vault), pearl, 'PEARLs')

        time.sleep(2)

        if pearl == 0:
            continue

        epochs = int(note.functions.endEpoch(vault).call()) - epoch

        print('Note #' + str(vault), epochs, 'epochs')

        time.sleep(2)

        if epochs == 0:
            continue

        nonce = w3.eth.getTransactionCount(me)

        tx = {
            'nonce': nonce,
            'gas': 150000,
            'maxPriorityFeePerGas': price,
            'maxFeePerGas': price,
            'from': me,
            'type': '0x2'
        }

        print('Note #' + str(vault), nonce)

        tx = lake.functions.claimReward(address, vault).buildTransaction(tx)

        signed = w3.eth.account.signTransaction(tx, key)

        hash = w3.eth.sendRawTransaction(signed.rawTransaction)

        print('Claimed!', w3.toHex(hash))

        time.sleep(2)

    time.sleep(2)