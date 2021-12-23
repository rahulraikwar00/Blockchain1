# ``TESTCOIN``
## Python implementation of a blockchain.

![](https://img.shields.io/github/issues/rahulraikwar00/Blockchain1) ![](https://img.shields.io/github/stars/rahulraikwar00/Blockchain1) ![](https://img.shields.io/github/forks/rahulraikwar00/Blockchain1)
![](https://img.shields.io/github/license/rahulraikwar00/Blockchain1)
![](https://img.shields.io/twitter/url?label=Rahul%20Raikwar&style=social&url=https%3A%2F%2Ftwitter.com%2Frahulraikwar00)

![img](https://imgur.com/a/W8HdIrf)

## Description

The Testcoin implementation is focused almost exclusively in the hashed ledger feature. It does include some advanced feature like a distributed nodes and a consensus protocol via proof of work. which is just a simple function not a complex algorithm.
<!-- Here you'll also find that the idea of the "transaction" is abstracted to a more general concept of "`message`" that can contain any type of data. -->

The goal of this project is to explain and to make clearer how is a blockchain structured at the very core. It's not built with the intention to replicate an advanced blockchain like Bitcoin or Ethereum.
<!-- 
The following blockchain implemented in the simple_chain.py file is composed of 3 classes. The `Message()` class, the `Block()` class and the `Chain()`. -->

<!-- A `message` is the basic data container. It is sealed when added to a block and has 2 hashes that identify it: the payload hash and the block hash.
Each message is linked to the previous message via hash pointers (the `prev_hash` attribute). The `validate` message method will ensure the integrity of each message, but will not check if the hash pointers are correct. This is left to the `validate` method in the `Block()` class.

A `block` can contain 1,...,n messages that are linked sequentially one after the other. When a `block` is added to the `chain`, it's sealed and validated to
ensure that the messages are correctly ordered and the hash pointers match. Once the block is sealed and hashed, it is validated by checking the expected vs the actual.

A `chain` can contain 1,...,m blocks that are linked sequentially one after another. The chain integrity can be validated at any time calling the `validate` method, which will call each block's validate method and will raise an `InvalidBlockchain` exception. -->


# Blockchain in Python from scratch

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5e92f10381a14b48914346300782a949)](https://www.codacy.com/app/jparicka/blockchain?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jparicka/blockchain&amp;utm_campaign=Badge_Grade)

Understanding Blockchain isn't easy. At least it wasn't for me. I had to go through number of frustrations due to too few funcional examples of how this technology works. And I like learning by doing so if you do the same, allow me to guide you and by the end you will have a functioning Blockchain with a solid idea of how they work.

### Before you get started..

Remember that a Blockchain is an immutable, sequential chain of records called Blocks. They can contain transactions, files or any data you like, really. But the important thing is that they’re chained together using hashes.

### What is needed?

Make sure that you have Python 3.6+ installed (along with pip) and you will also need Flask and Requests library.

```sh
$ pip3 install -r requirements
```

You will also need an HTTP client like Postman or curl. But anything will do.

# Step 1: Building a Blockchain

So what does a block look like?

Each block has an index, timestamp, transactions, proof (more on that later) and a hash of the previous transaction.

Here is an example of what a single Block looks like:


# MYCODE
```python
```

### Represenging a Blockchain

We'll create a Blockchain class whose constructor creates a list to store our Blockchain and another to store transactions.  Here is how the Class will look like:

```python
class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    @staticmethod
    def hash(block):
        pass

    def new_block(self):
        pass

    @property
    def last_block(self):
        return self.chain[-1]
```
This Blockchain class is responsible for managing the chain. It will store transactions and have helper functions.

The new_block method will create a new block and adds it on the chain and returns the last block in the chain.

The last_block method will return the last block in the chain.

Each block contains the hash and the hash of the previous block. This is what gives blockchains it's immutability - i.e. if anyone attack this, all subsequent blocks will be corrupt.

It's the core idea of blockchains. :)


### Adding transactions to the block

We will need some way of adding transactions to the block.
#MYCODE
```python

```

The new_transaction returns index of the block which will be added to current_transactions and is next one to be mined..

### Creating new blocks

In addition to creating the genesis block in our constructor, we will also need to flesh out methods for the new_block(), add_new_transaction() and hash().

#MYCODE
```python

```

Once our block is initiated, we need to feed it with the genesis block (a block with no predecessors). We will also need to add "a proof of work" to our genesis block which is the result of mining.

At this point, we're nearly done representing our Blockchain.

So lets talk about how the new blocks are created, forged and mined. :)


### Understanding Proof of Work

A proof of work algorithm are how new Blocks are created or mined on the Blockchain.

The goal is to discover a number that solves a problem.

The number must be difficult and resources consuming to find but super quick and easy to verify.

This is the core idea of Proof of Work.  :)


So lets work out some stupid-shit math problem that we are going to require to be solved in order for a block to be mined.

Lets say that hash of some integer ```x``` multiplied by another ```y``` must always end in 0.  So, as an example, the ```hash(x * y) = 4b4f4b4f54...0```.

#MYCODE
```python

```

In the Bitcoin world, the Proof of Work algorithm is called Hashcash. And it's not any different from the example above.  It's the very algorithm that miners race to solve in order to create a new block.  The difficulty is of course determined by the number of the characters searched for in the string. In our example we simplified it by defining that the resultant hash must end in 0 to make the whole thing in our case quicker and less resource intensive but this is how it works really.

The miners are rewarded for finding a solution by receiving a coin. In a transaction. There are many opinions on effectiness of this but this is how it works. And it really is that simple and this way the network is able to easily verify their solution. :)

** Editor's note: 4b-4f-4b-4f-54 in the example above in hex translates to = "kokot" lol. :D


### Implementing Proof of Work

Let's implement a similar algorithm for our Blockchain. Our rule will be similar to the example above.

"Find a number p that when hashed with the previous block's solution a hash with 4 leading 0 is produced."

#MYCODE
```python

```

To adjust the difficulty of the algorithm, we could modify the number of leading zeors.  But strictly speaking 4 is sufficient enough.  Also, you may find out that adding an extra 0 makes a mammoth difference to the time required to find a solution.

Now, our Blockchain class is pretty much complete, let's begin to interact with the ledger using the HTTP requests.


# Step 2: Blockchain as an API

We'll use Python Flask framework.  It's a micro-framework and it's really easy to use so for our example it'll do nicely.

We'll create three simple API endpoints:

  - /transactions/new to create a new transaction block
  - /mine to tell our service to mine a new block
  - /chain to return the full Blockchain

### Setting up Flask

Our server will form a single node in our Blockchain.  So let's create some code.
#MYCODE
```python

```

### The transaction endpoint

This is what the request for the transaction will look like. It's what the user will send to the server.

```json
{
    "sender": "sender_address",
    "recipient": "recipient_address",
    "amount": 100
}
```

Since we already have the method for adding transactions to a block, the rest is easy and pretty straight forward.

```python
import hashlib
import json

from time import time
from uulib import uulib4
from flask import Flask, jsonify, request

...

@app.route('/transactions/new', methods=['POST'])
def new_transaction():

    values = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing values', 400

    # create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to the Block {index}.'}

    return jsonify(response, 200)
```

### The mining endpoint

Our mining endpoint is where the mining happens and it's actually very easy as all it has to do are three things:

1) Calculate proof of work

2) Reward the miner by adding a transaction granting miner 1 coin

3) Forge the new Block by adding it to the chain


So, let's add on the mining function on our API:

```python
import hashlib
import json

from time import time
from uulib import uulib4
from flask import Flask, jsonify, request

...

@app.route('/mine', methods=['GET'])
def mine():

    # first we have to run the proof of work algorithm to calculate the new proof..
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # we must receive reward for finding the proof
    blockchain.new_transaction(
        sender=0,
        recipient=node_identifier,
        amount=1,
    )

    # forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Forged new block.",
        'index': block['index'],
        'transactions': block['transaction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
```

At this point, we are done, and we can start interacting with out blockchain.  :)


# Step 3: Interacting with our Blockchain

You can use a plain old cURL or Postman to interact with our Blockchain API ovet the network.

Fire up the server:

```
$ python3 blockchain.py
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

So first off let's try mining a block by making a GET request to the "mine" http://localhost:5000/mine:

```json
[
  {
    "index": 1, 
    "message": "Forged new block.", 
    "previous_hash": "7cd122100c9ded644768ccdec2d9433043968352e37d23526f63eefc65cd89e6", 
    "proof": 35293, 
    "transactions": [
      {
        "data": 1, 
        "recipient": "6a01861c7b3f483eab90727e621b2b96", 
        "sender": 0
      }
    ]
  }, 
  200
]
```

Motherfucker, very good! :)

Now lets create a new transaction by making a POST request to http://localhost:5000/transaction/new with a body containing our transaction structure. Let's make this call using the cURL:

```
$ curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "d4ee26eee15148ee92c6cd394edd974e",
 "recipient": "recipient-address",
 "amount": 5
}' "http://localhost:5000/transactions/new"
```

I have restarted the server, mined two blocks, to give 3 in total.  So let's inspect the full chain by requesting http://localhost:5000/chain:

```json
{
  "chain": [
    {
      "index": 1,
      "previous_hash": 1,
      "proof": 100,
      "timestamp": 1506280650.770839,
      "transactions": []
    },
    {
      "index": 2,
      "previous_hash": "c099bc...bfb7",
      "proof": 35293,
      "timestamp": 1506280664.717925,
      "transactions": [
        {
          "amount": 1,
          "recipient": "8bbcb347e0631231...e152b",
          "sender": "0"
        }
      ]
    },
    {
      "index": 3,
      "previous_hash": "eff91a...10f2",
      "proof": 35089,
      "timestamp": 1506280666.1086972,
      "transactions": [
        {
          "amount": 1,
          "recipient": "9e2e234e12e0631231...e152b",
          "sender": "0"
        }
      ]
    }
  ],
  "length": 3
}
```

## Contribute
Hey there! New ideas are welcome: open/close issues, fork the repo and share your code with a Pull Request.

Clone this project to your computer:

```bash
$ git clone https://github.com/rahulraiwkar00/blockchain1
```
