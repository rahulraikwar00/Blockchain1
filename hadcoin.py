
# Create a Crytocurrency
from _typeshed import Self
from ctypes import addressof
import datetime
import hashlib
import json
from typing import ChainMap
# from os import MFD_HUGE_SHIFT
# from typing_extensions import TypeGuard
from flask import Flask, jsonify, request
import requests
from werkzeug.wrappers import response
from uuid import uuid4
from urllib.parse import urlparse
# building blockchain


class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1, 'timestamp': str(
            datetime.datetime.now()), 'proof': proof, 'previous_hash': previous_hash, 'transactions': self.transactions}
        self.transactions.clear()
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_vaild(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transactions(self, sender, receiver, amount):
        self.transactions.append(
            {'sender': sender, 'receiver': receiver, 'amount': amount})

        previous_block = self.get_previous_block()
        return previous_block['index']+1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_vaild(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

# creating a web flask app


app = Flask(__name__)

# Creating an addresss for the node on port 5000

node_address = str(uuid4().replace('-', ''))

# creating a Blockchain
blockchain = Blockchain()


# mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    # print("called")
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transactions(
        sender=node_address, receiver='Rahul', amount=10)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'congratualtions you ust mine a Block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200
# Getting the full Blockchain


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'lenghth': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    res = blockchain.chain
    is_valid = blockchain.is_chain_vaild(res)
    if is_valid:
        response = {'message': 'Blockchain is valid'}
    else:
        response = {'message': 'Blockchain is invalid'}
    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_key = ['sender', 'receiver', 'amount']
    if not (key in json for key in transaction_key):
        return 'Some elements of the transaction are missing', 400

    index = blockchain.add_transaction(
        json['sender'], json['receiver'], json['amount'])
    response = {
        'message': f'This transaction will be added to the Block {index}'}
    return jsonify(response), 201

# Connecting the node in blockchain


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node', 401
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': 'All the nodes are connected and The hadcoin now Blockchain contain the following nodes',
        'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had diffrent chains so the Chain was replaced by longest one',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good, The chain is the largest one',
                    'new_chain': blockchain.chain}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)

