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

temp = path + '/notes.json'

w3 = Web3(Web3.HTTPProvider(rpc))
me = Web3.toChecksumAddress(me)
count = 0
tout = 10

names = {}
names['014-sfhand'] = 'Safe-Hand 14-Day Note'
names['028-frhand'] = 'Furry-Hand 28-Day Note'
names['028-sfhand'] = 'Safe-Hand 28-Day Note'
names['090-sfhand'] = 'Safe-Hand 90-Day Note'
names['090-sthand'] = 'Stone-Hand 90-Day Note'
names['180-dmhand'] = 'Diamond-Hand 180-Day Note'
names['180-sfhand'] = 'Safe-Hand 180-Day Note'

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

def claim(address, vault):
    global count

    hash = None

    try:
        print('[INFO]', 'Getting current nonce...')

        nonce = get_nonce()

        print('[INFO]', 'Nonce:', nonce, 'Current:', count)

        link = 'https://api.debank.com/chain/'
        link += 'gas_price_dict_v2?chain=matic'
        data = requests.get(link).json()
        price = int(data['data']['fast']['price'])

        print('[INFO]', 'Claiming Note #' + str(vault), 'in', nonce, 'nonce...')

        tx = {
            'nonce': nonce,
            'gas': 150000,
            'maxPriorityFeePerGas': price,
            'maxFeePerGas': price,
            'from': me,
            'type': '0x2'
        }

        tx = lake.functions.claimReward(address, vault).buildTransaction(tx)

        signed = w3.eth.account.signTransaction(tx, key)

        hash = w3.eth.sendRawTransaction(signed.rawTransaction)

        count = nonce
    except Exception as e:
        print('[FAIL]', e)

        return claim(address, vault)

    return w3.toHex(hash)

def get_items(note):
    items = None

    try:
        items = note.functions.balanceOf(me).call()
    except ValueError as e:
        return get_items(note)

    return items

def get_nonce():
    global count

    nonce = None

    try:
        nonce = w3.eth.getTransactionCount(me)

        if int(nonce) == int(count):
            time.sleep(tout)

            return get_nonce()

        if int(nonce) < int(count):
            print('[WARN]', 'Nonce is below current...')

            count = nonce

            time.sleep(tout)

            return get_nonce()
    except ValueError as e:
        return get_nonce()

    return nonce

def get_pearl(address, vault):
    pearl = None

    try:
        pearl = lake.functions.reward(address, vault).call()
    except ValueError as e:
        return get_pearl(address, vault)

    return pearl

def get_vault(note, index):
    vault = None

    try:
        vault = note.functions.tokenOfOwnerByIndex(me, index).call()
    except ValueError as e:
        return get_vault(note, index)

    return int(vault)

for name, note in notes.items():
    detail = names[name]

    print('[INFO]', 'Getting', detail + '/s...')

    note = address = Web3.toChecksumAddress(note)
    file = open(path + '/notes/' + name + '.json')
    abi = json.loads(file.read())
    note = w3.eth.contract(address = note, abi = abi)

    items = get_items(note)
    vaults = []

    for index in range(items):
        vault = get_vault(note, index)
        pearl = get_pearl(address, vault)

        print('[INFO]', detail, '#' + str(vault))

        if pearl == 0:
            continue

        print('[INFO]', 'Claiming', w3.fromWei(pearl, 'ether'), 'PEARLs')

        hash = claim(address, vault)

        print('[PASS]', 'Claimed!', hash)
        print('[PASS]', 'Current:', count)

        time.sleep(tout)