from dotenv import load_dotenv
from web3 import Web3
import json
import math
import os
import requests
import sys
import time

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

lake = '0xc67abda25d0421fe9dc1afd64183b179a426a256'
lake = Web3.toChecksumAddress(lake)
abi = json.loads(open(path + '/lake.json').read())
lake = w3.eth.contract(address = lake, abi = abi)

pearl = '0x52A7F40BB6e9BD9183071cdBdd3A977D713F2e34'
pearl = Web3.toChecksumAddress(pearl)
abi = json.loads(open(path + '/pearl.json').read())
pearl = w3.eth.contract(address = pearl, abi = abi)
pearl = pearl.functions.balanceOf(me).call()

name = '180-sfhand'
base = 1
tout = 10

if len(sys.argv) == 2:
    base = float(sys.argv[1])

if len(sys.argv) == 3:
    name = sys.argv[2]

note = notes[name]
note = Web3.toChecksumAddress(note)

amount = w3.fromWei(pearl, 'ether')
count = math.floor(float(amount) / float(base))

if pearl == 0:
    print('[WARN]', 'No PEARLs available to be locked')

    sys.exit()

print('[INFO]', 'Current:', amount, 'PEARLs')
print('[INFO]', 'Limit:', base, 'PEARLs per note')
print('[INFO]', 'Number of Notes:', count)
print('[INFO]', 'Note:', names[name])
print('[INFO]', 'Locking PEARLs to a new note...')

for index in range(count):
    nonce = w3.eth.getTransactionCount(me)

    tx = {
        'nonce': nonce,
        'gas': 400000,
        'maxPriorityFeePerGas': price,
        'maxFeePerGas': price,
        'from': me,
        'type': '0x2'
    }

    current = w3.toWei(base, 'ether')

    tx = lake.functions.lock(note, current).buildTransaction(tx)

    signed = w3.eth.account.signTransaction(tx, key)

    hash = w3.eth.sendRawTransaction(signed.rawTransaction)

    print('[PASS]', w3.toHex(hash))

    time.sleep(tout)