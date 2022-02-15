# Clam Chowder

Clam Chowder is a Python-based script for [Otter Clam](https://www.otterclam.finance/) that claims the rewards from all PEARL notes of the specified address then lock the claimed rewards into a new PEARL note.

## Installation

Install `Clam Chowder` through [pip](https://pip.pypa.io/en/stable/):

``` bash
$ pip install -r requirements.txt
```

## Basic Usage

### Prerequisites

* Create a file named `.env` and supply the following variables:

```
OTTERCLAM_ADDRESS=
OTTERCLAM_PRIVATE=
```

Wherein the `OTTERCLAM_ADDRESS` is the wallet address that contains the Pearl notes and the `OTTERCLAM_PRIVATE` is the exported private key. To know on how to export a wallet's private key through Metamask, kindly check this [link](https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key).

**Warning**: __EXPORTING YOUR ACCOUNT COULD BE RISKY AS IT DISPLAYS YOUR PRIVATE KEY IN CLEAR TEXT__. Therefore, you should make sure no one else sees, or otherwise is able to capture a screenshot while you retrieve your private key, to avoid possible loss of your Ether/tokens. Many phishing campaigns would ask for your private key, which would help them gain access to your accounts. You should never share your private key with anyone.

### Claiming PEARLs

```
$ python claim.py
```

The code above will check of all the existing PEARL notes (e.g. 14-day Safe-hand, 28-day Furry-hand, etc.) and execute the `claim` function in the contract.

### Locking PEARLs to new note

```
$ python lock.py [type]
```

Executing the specified script will lock all of the amount of PEARLs available in the provided wallet address. If `[type]` is not specified, the default value will be `180-day Safe-hand` note.

#### Available PEARL notes for [type]

* `014-sfhand` - Safe-Hand 14-Day Note
* `028-sfhand` - Safe-Hand 28-Day Note
* `090-sfhand` - Safe-Hand 90-Day Note
* `180-sfhand` - Safe-Hand 180-Day Note
* `028-frhand` - Furry-Hand 28-Day Note
* `090-sthand` - Stone-Hand 90-Day Note
* `180-dmhand` - Diamond-Hand 180-Day Note